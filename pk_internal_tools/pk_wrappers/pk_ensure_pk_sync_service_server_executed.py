import logging
import uvicorn
import asyncio
import json
import base64
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from typing import Dict

from pk_internal_tools.pk_objects.pk_sync_definitions import (
    SyncEvent, EventType, AUTH_TOKEN, DEFAULT_SYNC_ROOT_SERVER, IGNORE_PATTERNS,
    SERVER_HOST, SERVER_PORT
)

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

# --- Server State ---
SYNC_ROOT = Path(DEFAULT_SYNC_ROOT_SERVER).resolve()
STATE_FILE = SYNC_ROOT / ".sync_state.json"

class ConnectionManager:
    """Manages active WebSocket connections."""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logging.info(f"Client connected: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        logging.info(f"Client disconnected: {client_id}")

    async def broadcast(self, message: SyncEvent, exclude_client_id: str):
        """Send a message to all clients except the excluded one."""
        for client_id, connection in self.active_connections.items():
            if client_id != exclude_client_id:
                await connection.send_text(message.json())
                logging.info(f"Broadcasted '{message.event_type}' for '{message.relative_path}' to {client_id}")

class StateManager:
    """Manages file states (hashes, timestamps) and locks."""
    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.file_states: Dict[str, dict] = {}  # {relative_path: {"hash": str, "timestamp": float}}
        self.file_locks: Dict[str, str] = {}  # {relative_path: client_id}
        self.load_state()

    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                    self.file_states = state.get("file_states", {})
                    # Do not persist locks on startup
                    self.file_locks = {}
                logging.info(f"Successfully loaded state from {self.state_file}")
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Could not load state file {self.state_file}. Starting fresh. Error: {e}")
        else:
            logging.info("No state file found. Starting with a fresh state.")

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump({"file_states": self.file_states}, f, indent=4)
            logging.info(f"Successfully saved state to {self.state_file}")
        except IOError as e:
            logging.error(f"Could not save state file {self.state_file}. Error: {e}")

    def get_lock_holder(self, path: str) -> str | None:
        return self.file_locks.get(path)

    def acquire_lock(self, path: str, client_id: str) -> bool:
        if self.get_lock_holder(path) is None:
            self.file_locks[path] = client_id
            return True
        return False

    def release_lock(self, path: str, client_id: str) -> bool:
        if self.get_lock_holder(path) == client_id:
            del self.file_locks[path]
            return True
        return False
        
    def release_all_locks_for_client(self, client_id: str):
        locks_to_release = [path for path, holder_id in self.file_locks.items() if holder_id == client_id]
        for path in locks_to_release:
            del self.file_locks[path]
        logging.info(f"Released {len(locks_to_release)} locks for client {client_id}")

    def delete_file_state(self, path: str):
        """Deletes the state for a given file path."""
        if path in self.file_states:
            del self.file_states[path]
            logging.info(f"Deleted state for file: {path}")

    def move_file_state(self, old_path: str, new_path: str, new_hash: str, new_timestamp: float):
        """Moves the state from an old path to a new path."""
        if old_path in self.file_states:
            del self.file_states[old_path]
        self.file_states[new_path] = {"hash": new_hash, "timestamp": new_timestamp}
        logging.info(f"Moved state from {old_path} to {new_path}")


# --- FastAPI App and Managers ---
app = FastAPI()
manager = ConnectionManager()
state_manager = StateManager(STATE_FILE)

def is_ignored(path_str: str) -> bool:
    """Check if a path matches any of the glob ignore patterns."""
    path_obj = Path(path_str)
    return any(path_obj.match(pattern) for pattern in IGNORE_PATTERNS)

@app.websocket("/ws/sync/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        # --- Authentication Step ---
        try:
            auth_token = await asyncio.wait_for(websocket.receive_text(), timeout=10.0)
            if auth_token != AUTH_TOKEN:
                logging.warning(f"Client {client_id} failed authentication. Closing connection.")
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                raise WebSocketDisconnect("Authentication failed")

            # Send auth success message
            await websocket.send_text(SyncEvent(
                event_type=EventType.AUTH_SUCCESS,
                relative_path="",
                message="Authentication successful."
            ).json())
            logging.info(f"Client {client_id} authenticated successfully.")

        except asyncio.TimeoutError:
            logging.warning(f"Client {client_id} did not send auth token in time. Closing connection.")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise WebSocketDisconnect("Authentication timeout")
        # --- End Authentication Step ---

        while True:
            data = await websocket.receive_text()
            event = SyncEvent.parse_raw(data)

            if event.event_type == EventType.REQUEST_INITIAL_SYNC:
                await websocket.send_text(SyncEvent(
                    event_type=EventType.INITIAL_SYNC_STATE,
                    server_state=state_manager.file_states
                ).json())
                logging.info(f"Sent initial state to {client_id}")

            elif event.event_type == EventType.REQUEST_FILE_DOWNLOAD:
                full_path = SYNC_ROOT / event.relative_path
                if full_path.exists() and not is_ignored(str(full_path)):
                    with open(full_path, "rb") as f:
                        content_b64 = base64.b64encode(f.read()).decode('utf-8')
                    
                    file_state = state_manager.file_states.get(event.relative_path, {})
                    response_event = SyncEvent(
                        event_type=EventType.SERVER_UPDATE, # Re-use for sending file content
                        relative_path=event.relative_path,
                        content=content_b64,
                        file_hash=file_state.get("hash"),
                        timestamp=file_state.get("timestamp")
                    )
                    await websocket.send_text(response_event.json())
                    logging.info(f"Sent file {event.relative_path} to {client_id}")

            elif event.event_type == EventType.REQUEST_LOCK:
                if state_manager.acquire_lock(event.relative_path, client_id):
                    await websocket.send_text(SyncEvent(event_type=EventType.LOCK_GRANTED, relative_path=event.relative_path).json())
                else:
                    holder = state_manager.get_lock_holder(event.relative_path)
                    await websocket.send_text(SyncEvent(
                        event_type=EventType.LOCK_DENIED,
                        relative_path=event.relative_path,
                        message=f"File is locked by {holder}"
                    ).json())

            elif event.event_type == EventType.RELEASE_LOCK:
                state_manager.release_lock(event.relative_path, client_id)

            elif event.event_type == EventType.CLIENT_CHANGE:
                # Basic conflict detection: last write wins based on timestamp
                server_timestamp = state_manager.file_states.get(event.relative_path, {}).get("timestamp", 0)
                if event.timestamp < server_timestamp:
                    logging.warning(f"Conflict detected for {event.relative_path}. Server has newer version.")
                    continue

                # Process the change
                full_path = SYNC_ROOT / event.relative_path
                if event.content is not None:
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    content_bytes = base64.b64decode(event.content)
                    with open(full_path, "wb") as f:
                        f.write(content_bytes)
                
                # Update state
                state_manager.file_states[event.relative_path] = {"hash": event.file_hash, "timestamp": event.timestamp}
                
                # Broadcast to other clients
                await manager.broadcast(event, exclude_client_id=client_id)
            
            elif event.event_type == EventType.FILE_DELETED:
                full_path = SYNC_ROOT / event.relative_path
                if full_path.exists():
                    try:
                        full_path.unlink()
                        logging.info(f"Deleted file on server: {full_path}")
                    except OSError as e:
                        logging.error(f"Error deleting file {full_path}: {e}")
                
                state_manager.delete_file_state(event.relative_path)
                await manager.broadcast(event, exclude_client_id=client_id)

            elif event.event_type == EventType.FILE_MOVED:
                old_full_path = SYNC_ROOT / event.relative_path
                new_full_path = SYNC_ROOT / event.new_relative_path
                
                if old_full_path.exists():
                    try:
                        new_full_path.parent.mkdir(parents=True, exist_ok=True)
                        old_full_path.rename(new_full_path)
                        logging.info(f"Moved file from {old_full_path} to {new_full_path}")
                    except OSError as e:
                        logging.error(f"Error moving file from {old_full_path} to {new_full_path}: {e}")

                state_manager.move_file_state(
                    event.relative_path, 
                    event.new_relative_path, 
                    event.file_hash, 
                    event.timestamp
                )
                await manager.broadcast(event, exclude_client_id=client_id)


    except WebSocketDisconnect:
        manager.disconnect(client_id)
        state_manager.release_all_locks_for_client(client_id)
    except Exception as e:
        logging.error(f"An error occurred with client {client_id}: {e}")
        manager.disconnect(client_id)
        state_manager.release_all_locks_for_client(client_id)


@app.on_event("startup")
async def startup_event():
    logging.info("Starting up Sync Server...")
    SYNC_ROOT.mkdir(parents=True, exist_ok=True)
    logging.info(f"Sync root directory '{SYNC_ROOT}' is ready.")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down Sync Server...")
    state_manager.save_state()
    logging.info("Server state saved.")

if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)