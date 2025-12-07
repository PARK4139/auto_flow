import logging
import os
from pathlib import Path
from typing import List, Dict, Any

# Import the centralized DB path
from pk_internal_tools.pk_objects.pk_files import F_MEDIA_FILES_SQLITE
# Import the DB helper class
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


def ensure_media_files_table_exists(db: PkSqlite3):
    """Initializes the media files database table if it doesn't exist."""
    logging.info(f"Initializing media files DB at {db.f_pk_sqlite}")
    db.execute("""
        CREATE TABLE IF NOT EXISTS media_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            size INTEGER NOT NULL,
            mtime REAL NOT NULL,
            ctime REAL NOT NULL,
            d_working TEXT NOT NULL
        )
    """)
    db.commit()
    logging.info("Media files DB table initialized.")


def sync_media_files_to_db(d_working: Path, allowed_extensions: List[str]):
    """Synchronizes media files in a directory with the database."""
    logging.info(f"Starting DB sync for directory: {d_working}")
    logging.info(f"Allowed extensions: {allowed_extensions}") # Log allowed extensions
    db = PkSqlite3(db_path=F_MEDIA_FILES_SQLITE)
    ensure_media_files_table_exists(db) # Ensure table exists

    # n. Get current files from file system
    fs_files: Dict[str, Dict[str, Any]] = {}
    file_scan_count = 0
    for root, _, files in os.walk(d_working):
        for file_name in files:
            file_scan_count += 1
            logging.debug(f"Scanning file: {file_name}") # Log every file found
            file_path = Path(root) / file_name
            if file_path.suffix.lower() in allowed_extensions:
                try:
                    stat = file_path.stat()
                    fs_files[str(file_path)] = {
                        "path": str(file_path),
                        "name": file_name,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "ctime": stat.st_ctime,
                        "d_working": str(d_working)
                    }
                except FileNotFoundError:
                    logging.warning(f"File not found during scan: {file_path}")
                except Exception as e:
                    logging.error(f"Error getting stat for {file_path}: {e}")

    # n. Get existing files from DB for this d_working
    db_files: Dict[str, Dict[str, Any]] = {}
    db_records = db.query("SELECT path, name, size, mtime, ctime FROM media_files WHERE d_working = ?", (str(d_working),))
    for record in db_records:
        db_files[record["path"]] = {
            "path": record["path"],
            "name": record["name"],
            "size": record["size"],
            "mtime": record["mtime"],
            "ctime": record["ctime"]
        }

    # 3. Compare and synchronize
    to_add = []
    to_update = []
    to_delete = []

    # Check for deleted and updated files
    for db_path, db_data in db_files.items():
        if db_path not in fs_files:
            to_delete.append(db_path)
        else:
            fs_data = fs_files[db_path]
            if db_data["size"] != fs_data["size"] or db_data["mtime"] != fs_data["mtime"]:
                to_update.append(fs_data) # Update with new FS data

    # Check for new files
    for fs_path, fs_data in fs_files.items():
        if fs_path not in db_files:
            to_add.append(fs_data)

    # Perform DB operations
    if to_delete:
        logging.info(f"Deleting {len(to_delete)} files from DB.")
        db.executemany("DELETE FROM media_files WHERE path = ?", [(p,) for p in to_delete])
    if to_add:
        logging.info(f"Adding {len(to_add)} files to DB.")
        db.executemany("INSERT OR IGNORE INTO media_files (path, name, size, mtime, ctime, d_working) VALUES (?, ?, ?, ?, ?, ?)",
                       [(f["path"], f["name"], f["size"], f["mtime"], f["ctime"], f["d_working"]) for f in to_add])
    if to_update:
        logging.info(f"Updating {len(to_update)} files in DB.")
        db.executemany("UPDATE media_files SET name = ?, size = ?, mtime = ?, ctime = ? WHERE path = ?",
                       [(f["name"], f["size"], f["mtime"], f["ctime"], f["path"]) for f in to_update])

    db.commit()
    logging.info(f"DB sync completed for directory: {d_working}. Added: {len(to_add)}, Updated: {len(to_update)}, Deleted: {len(to_delete)}.")
