from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict
import uuid

# --- Configuration ---
DEFAULT_SYNC_ROOT_SERVER = "C:/pk_sync_target"
DEFAULT_WATCH_DIR_CLIENT = "C:/pk_sync_source"
AUTH_TOKEN = "your-super-secret-token"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8088

# --- Ignore Patterns ---
IGNORE_PATTERNS = [
    ".git/", "__pycache__/", "*.pyc", ".venv", ".idea/", ".vscode/",
    ".DS_Store", "Thumbs.db", "pk_logs/", "pk_cache/",
    "pk_sync_service/"
]

# --- Event Types ---
class EventType(str, Enum):
    # Client to Server
    REQUEST_INITIAL_SYNC = "request_initial_sync"
    CLIENT_CHANGE = "client_change" # For created or modified files
    FILE_DELETED = "file_deleted"
    FILE_MOVED = "file_moved"
    REQUEST_LOCK = "request_lock"
    RELEASE_LOCK = "release_lock"
    REQUEST_FILE_DOWNLOAD = "request_file_download"

    # Server to Client
    AUTH_SUCCESS = "auth_success"
    INITIAL_SYNC_STATE = "initial_sync_state"
    SERVER_UPDATE = "server_update" # For created or modified files
    LOCK_GRANTED = "lock_granted"
    LOCK_DENIED = "lock_denied"
    CONFLICT_DETECTED = "conflict_detected"
    ERROR = "error"

# --- Pydantic Models ---
class FileLockInfo(BaseModel):
    """Information about a file lock."""
    relative_path: str
    client_id: str

class SyncEvent(BaseModel):
    """
    Represents a file system event for WebSocket communication.
    Can be sent from client to server or server to client.
    """
    event_type: EventType
    client_id: str = ""
    relative_path: str
    content: Optional[str] = None  # Base64 encoded content
    file_hash: Optional[str] = None
    timestamp: Optional[float] = None
    new_relative_path: Optional[str] = None
    lock_info: Optional[FileLockInfo] = None
    server_state: Optional[Dict[str, dict]] = None # For initial sync
    message: Optional[str] = None # For errors or notifications
