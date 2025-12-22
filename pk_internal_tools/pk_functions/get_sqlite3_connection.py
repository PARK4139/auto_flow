"""
--- DB 관리 ---
"""

from contextlib import contextmanager
from pathlib import Path


@contextmanager
def get_sqlite3_connection(db_path: Path):
    import logging
    import sqlite3

    try:
        conn = sqlite3.connect(db_path, timeout=10)
        yield conn
    except sqlite3.Error as e:
        logging.error(f"Database error at {db_path}: {e}")
        raise
    finally:
        if 'conn' in locals() and conn:
            conn.close()
