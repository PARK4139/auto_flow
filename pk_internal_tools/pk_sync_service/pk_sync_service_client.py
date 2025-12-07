import logging
import time
import os
import sys
import base64
import hashlib
import asyncio
import uuid
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent, FileMovedEvent
import websockets
import json

# Assuming pk_sync_definitions.py is in the same directory
from .pk_sync_definitions import (
    SyncEvent, EventType,
    AUTH_TOKEN, DEFAULT_WATCH_DIR_CLIENT, IGNORE_PATTERNS,
    SERVER_HOST, SERVER_PORT
)
# Using lazy import for ensure_spoken as it's a project-specific utility
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken

# --- Configuration ---
WATCH_DIRECTORY = Path(DEFAULT_WATCH_DIR_CLIENT).resolve()
SERVER_URI = f"ws://{SERVER_HOST}:{SERVER_PORT}/ws/sync/"
CLIENT_ID = str(uuid.uuid4())

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_hash(path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    if not path.exists() or path.is_dir():
        return ""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

class SyncClient:
    def __init__(self, watch_dir: Path, server_uri: str, client_id: str):
        self.watch_dir = watch_dir
        self.server_uri = f"{server_uri}{client_id}"
        self.client_id = client_id
        self.ws: websockets.WebSocketClientProtocol = None
        self.local_state = {} # {relative_path: {"hash": str, "timestamp": float}}
        self.observer = Observer()
        self.event_handler = self._create_event_handler()
        self._is_applying_server_change = asyncio.Lock()
        self._pending_locks = {}

    def _create_event_handler(self):
        """Creates the watchdog event handler."""
        class Handler(FileSystemEventHandler):
            def __init__(self, client):
                self.client = client

            def on_created(self, event):
                if event.is_directory:
                    return
                asyncio.run_coroutine_threadsafe(
                    self.client.handle_local_change(Path(event.src_path)),
                    asyncio.get_event_loop()
                )

            def on_modified(self, event):
                if event.is_directory:
                    return
                asyncio.run_coroutine_threadsafe(
                    self.client.handle_local_change(Path(event.src_path)),
                    asyncio.get_event_loop()
                )

            def on_deleted(self, event):
                if event.is_directory:
                    return
                asyncio.run_coroutine_threadsafe(
                    self.client.handle_local_delete(Path(event.src_path)),
                    asyncio.get_event_loop()
                )

            def on_moved(self, event):
                if event.is_directory:
                    return
                asyncio.run_coroutine_threadsafe(
                    self.client.handle_local_move(Path(event.src_path), Path(event.dest_path)),
                    asyncio.get_event_loop()
                )
        return Handler(self)

    def _scan_local_directory(self):
        """Scans the watch directory and populates the initial local state."""
        logging.info("Scanning local directory for initial state...")
        for root, _, files in os.walk(self.watch_dir):
            for name in files:
                full_path = Path(root) / name
                relative_path = str(full_path.relative_to(self.watch_dir))
                if not is_ignored(relative_path):
                    self.local_state[relative_path] = {
                        "hash": get_file_hash(full_path),
                        "timestamp": full_path.stat().st_mtime
                    }
        logging.info(f"Initial local scan found {len(self.local_state)} files.")

    async def handle_local_change(self, path: Path):
        """Handle a file change detected by watchdog."""
        async with self._is_applying_server_change: # Prevents handling local changes while applying server changes
            relative_path = str(path.relative_to(self.watch_dir))
            if is_ignored(relative_path):
                return

            new_hash = get_file_hash(path)
            if self.local_state.get(relative_path, {}).get("hash") == new_hash:
                return # No actual content change

            logging.info(f"Local change detected: {relative_path}")
            # Request a lock before sending the change
            lock_request_event = SyncEvent(
                event_type=EventType.REQUEST_LOCK,
                client_id=self.client_id,
                relative_path=relative_path
            )
            await self.ws.send(lock_request_event.json())
            # Store the change to be sent after lock is granted
            self._pending_locks[relative_path] = {"path": path, "hash": new_hash}

    async def handle_local_delete(self, path: Path):
        """Handle a file deletion detected by watchdog."""
        async with self._is_applying_server_change:
            relative_path = str(path.relative_to(self.watch_dir))
            if is_ignored(relative_path):
                return

            logging.info(f"Local file deleted: {relative_path}")
            delete_event = SyncEvent(
                event_type=EventType.FILE_DELETED,
                client_id=self.client_id,
                relative_path=relative_path
            )
            await self.ws.send(delete_event.json())
            self.local_state.pop(relative_path, None)

    async def handle_local_move(self, src_path: Path, dest_path: Path):
        """Handle a file move/rename detected by watchdog."""
        async with self._is_applying_server_change:
            old_relative_path = str(src_path.relative_to(self.watch_dir))
            new_relative_path = str(dest_path.relative_to(self.watch_dir))

            if is_ignored(old_relative_path) and is_ignored(new_relative_path):
                return

            logging.info(f"Local file moved: {old_relative_path} -> {new_relative_path}")
            
            # Update local state first
            new_hash = get_file_hash(dest_path)
            new_timestamp = dest_path.stat().st_mtime
            self.local_state.pop(old_relative_path, None)
            self.local_state[new_relative_path] = {"hash": new_hash, "timestamp": new_timestamp}

            move_event = SyncEvent(
                event_type=EventType.FILE_MOVED,
                client_id=self.client_id,
                relative_path=old_relative_path,
                new_relative_path=new_relative_path,
                file_hash=new_hash,
                timestamp=new_timestamp
            )
            await self.ws.send(move_event.json())

    async def handle_server_message(self, message: str):
        """Process messages received from the server."""
        event = SyncEvent.parse_raw(message)

        if event.event_type == EventType.INITIAL_SYNC_STATE:
            logging.info("Received initial sync state from server. Starting sync process...")
            server_state = event.server_state or {}
            server_files = set(server_state.keys())
            local_files = set(self.local_state.keys())

            # 1. Files to delete locally
            files_to_delete = local_files - server_files
            for rel_path in files_to_delete:
                full_path = self.watch_dir / rel_path
                try:
                    async with self._is_applying_server_change:
                        full_path.unlink()
                        del self.local_state[rel_path]
                    logging.info(f"Deleted local file (not on server): {rel_path}")
                except OSError as e:
                    logging.error(f"Error deleting local file {rel_path}: {e}")
            
            # 2. Files to download from server
            for rel_path, s_meta in server_state.items():
                l_meta = self.local_state.get(rel_path)
                if not l_meta or l_meta.get("hash") != s_meta.get("hash"):
                    logging.info(f"File '{rel_path}' is missing or outdated. Requesting download.")
                    await self.ws.send(SyncEvent(
                        event_type=EventType.REQUEST_FILE_DOWNLOAD,
                        client_id=self.client_id,
                        relative_path=rel_path
                    ).json())

            logging.info("Initial sync process finished.")

        elif event.event_type == EventType.LOCK_GRANTED:
            logging.info(f"Lock granted for {event.relative_path}")
            if event.relative_path in self._pending_locks:
                change_info = self._pending_locks.pop(event.relative_path)
                path = change_info["path"]
                
                with open(path, "rb") as f:
                    content_b64 = base64.b64encode(f.read()).decode('utf-8')
                
                change_event = SyncEvent(
                    event_type=EventType.CLIENT_CHANGE,
                    client_id=self.client_id,
                    relative_path=event.relative_path,
                    content=content_b64,
                    file_hash=change_info["hash"],
                    timestamp=path.stat().st_mtime
                )
                await self.ws.send(change_event.json())
                self.local_state[event.relative_path] = {"hash": change_info["hash"], "timestamp": path.stat().st_mtime}

        elif event.event_type == EventType.LOCK_DENIED:
            logging.warning(f"Lock denied for {event.relative_path}. Reason: {event.message}")
            ensure_spoken(f"파일 수정을 할 수 없습니다. {event.relative_path} 파일은 현재 다른 사용자가 수정중입니다.")
            self._pending_locks.pop(event.relative_path, None)

        elif event.event_type == EventType.SERVER_UPDATE:
            logging.info(f"Received server update for {event.relative_path}")
            async with self._is_applying_server_change:
                full_path = self.watch_dir / event.relative_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                content_bytes = base64.b64decode(event.content)
                with open(full_path, "wb") as f:
                    f.write(content_bytes)
                
                self.local_state[event.relative_path] = {"hash": event.file_hash, "timestamp": event.timestamp}

        elif event.event_type == EventType.FILE_DELETED:
            logging.info(f"Received server delete for {event.relative_path}")
            async with self._is_applying_server_change:
                full_path = self.watch_dir / event.relative_path
                if full_path.exists():
                    try:
                        full_path.unlink()
                        self.local_state.pop(event.relative_path, None)
                        logging.info(f"Deleted local file: {event.relative_path}")
                    except OSError as e:
                        logging.error(f"Error deleting local file {event.relative_path}: {e}")
        
        elif event.event_type == EventType.FILE_MOVED:
            logging.info(f"Received server move for {event.relative_path} -> {event.new_relative_path}")
            async with self._is_applying_server_change:
                old_full_path = self.watch_dir / event.relative_path
                new_full_path = self.watch_dir / event.new_relative_path
                if old_full_path.exists():
                    try:
                        new_full_path.parent.mkdir(parents=True, exist_ok=True)
                        old_full_path.rename(new_full_path)
                        
                        # Update local state
                        self.local_state.pop(event.relative_path, None)
                        self.local_state[event.new_relative_path] = {"hash": event.file_hash, "timestamp": event.timestamp}
                        logging.info(f"Moved local file to {event.new_relative_path}")
                    except OSError as e:
                        logging.error(f"Error moving local file to {event.new_relative_path}: {e}")
                elif not new_full_path.exists():
                    # If old path doesn't exist, it might be a move of a new file from another client.
                    # Request a download.
                    logging.info(f"File '{event.new_relative_path}' is new from a move. Requesting download.")
                    await self.ws.send(SyncEvent(
                        event_type=EventType.REQUEST_FILE_DOWNLOAD,
                        client_id=self.client_id,
                        relative_path=event.new_relative_path
                    ).json())

    async def run(self):
        """Main loop to connect to the server and handle sync."""
        self.watch_dir.mkdir(parents=True, exist_ok=True)
        self.observer.schedule(self.event_handler, str(self.watch_dir), recursive=True)
        self.observer.start()
        logging.info(f"Client {self.client_id} started watching {self.watch_dir}")

        while True:
            try:
                async with websockets.connect(self.server_uri) as websocket:
                    self.ws = websocket
                    logging.info("Connected to sync server. Authenticating...")

                    # --- Authentication Step ---
                    await websocket.send(AUTH_TOKEN)
                    try:
                        response_str = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                        response_event = SyncEvent.parse_raw(response_str)
                        if response_event.event_type == EventType.AUTH_SUCCESS:
                            logging.info("Authentication successful.")
                        else:
                            logging.error(f"Authentication failed. Server sent: {response_event.event_type}")
                            await asyncio.sleep(5)
                            continue # Reconnect
                    except asyncio.TimeoutError:
                        logging.error("Authentication timed out. No response from server.")
                        await asyncio.sleep(5)
                        continue # Reconnect
                    # --- End Authentication Step ---
                    
                    # --- Initial Sync Step ---
                    self._scan_local_directory()
                    await websocket.send(SyncEvent(
                        event_type=EventType.REQUEST_INITIAL_SYNC,
                        client_id=self.client_id,
                        relative_path="" # Not applicable
                    ).json())
                    logging.info("Requested initial sync state from server.")
                    # --- End Initial Sync Step ---
                    
                    # Listen for messages
                    async for message in websocket:
                        await self.handle_server_message(message)

            except (websockets.exceptions.ConnectionClosedError, OSError) as e:
                logging.warning(f"Connection lost: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                break
        
        self.observer.stop()
        self.observer.join()

def ensure_pk_sync_service_client_started():
    client = SyncClient(WATCH_DIRECTORY, SERVER_URI, CLIENT_ID)
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        logging.info("Client shutting down.")

if __name__ == "__main__":
    ensure_pk_sync_service_client_started()