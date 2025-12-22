import logging
from pathlib import Path
from typing import List
import re

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_files import F_MEDIA_FILES_SQLITE
from .sync_media_files_to_db import sync_media_files_to_db, ensure_media_files_table_exists


def get_files_from_db(d_working: Path, allowed_extensions: List[str],
                      name_parts_to_ignore: List[str], regex_patterns_to_ignore: List[str],
                      with_sync: bool = False) -> List[Path]:
    """
    Queries the DB for filtered media files.
    If with_sync is True, it synchronizes the directory with the DB before querying.
    """
    if with_sync:
        logging.info(f"Sync option enabled. Starting sync for {d_working} before querying.")
        sync_media_files_to_db(d_working, allowed_extensions)
        logging.info("Sync completed.")

    db = PkSqlite3(db_path=F_MEDIA_FILES_SQLITE)
    ensure_media_files_table_exists(db)  # Ensure table exists before querying

    logging.debug(f"Querying DB for filtered media files in {d_working}")

    # Build WHERE clause for filtering
    where_clauses = ["d_working = ?"]
    params = [str(d_working)]

    # Add allowed extensions filter using LIKE for each extension
    if allowed_extensions:
        ext_clauses = []
        for ext in allowed_extensions:
            ext_clauses.append("LOWER(name) LIKE ?")
            # Ensure the extension starts with a dot for the LIKE clause
            dot_ext = ext if ext.startswith('.') else '.' + ext
            params.append(f"%{dot_ext.lower()}")
        where_clauses.append(f"({' OR '.join(ext_clauses)})")

    # Add name parts to ignore (case-insensitive)
    for part in name_parts_to_ignore:
        where_clauses.append(f"LOWER(name) NOT LIKE ?")
        params.append(f"%{part.lower()}%")

    query = f"SELECT path FROM media_files WHERE {' AND '.join(where_clauses)}"

    try:
        db_paths = db.query(query, tuple(params))
        logging.debug(f"SQL query returned {len(db_paths)} files before Python regex filtering.")
    except Exception as e:
        logging.error(f"Failed to query media files DB. Has it been synced at least once? Error: {e}")
        return []

    # Filter by regex patterns in Python
    final_paths = []
    if not regex_patterns_to_ignore:
        final_paths = [Path(record["path"]) for record in db_paths]
    else:
        import re
        for record in db_paths:
            file_path = Path(record["path"])
            file_name = file_path.name.lower()
            should_ignore_regex = False
            for pattern in regex_patterns_to_ignore:
                if re.search(pattern, file_name):
                    should_ignore_regex = True
                    break
            if not should_ignore_regex:
                final_paths.append(file_path)

    logging.info(f"Found {len(final_paths)} filtered media files from DB for d_working='{d_working}'.")
    return final_paths
