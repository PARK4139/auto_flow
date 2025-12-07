
import sqlite3
import logging
from pathlib import Path
from pk_internal_tools.pk_objects.pk_directories import d_pk_cache
from pk_internal_tools.pk_functions.get_hash import get_hash

class PkLoop:
    """
    Manages a loop counter for a specific loop_id using a SQLite database.
    """
    def __init__(self, loop_id: str):
        """
        Initializes the PkLoop instance.

        Args:
            loop_id (str): A unique identifier for the loop counter.
        """
        self.loop_id = loop_id
        self.loop_cnt = 0
        self._db_path = d_pk_cache / "loop_cnt.sqlite"
        self.init_loop_cnt() # Initialize on creation

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(self._db_path)
            return conn
        except sqlite3.Error as e:
            logging.error("Database connection error in PkLoop for loop_id '%s': %s", self.loop_id, e)
            return None

    def init_loop_cnt(self):
        """
        Initializes or resets the loop count for this instance's loop_id to 0.
        """
        conn = self._connect()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loop_counts (
                    loop_id TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
            ''')
            cursor.execute("INSERT OR REPLACE INTO loop_counts (loop_id, count) VALUES (?, 0)", (self.loop_id,))
            conn.commit()
            self.loop_cnt = 0
            logging.info("PkLoop count for '%s' initialized to 0.", self.loop_id)
            return True
        except sqlite3.Error as e:
            logging.error("Database error in PkLoop.init_loop_cnt for loop_id '%s': %s", self.loop_id, e)
            return False
        finally:
            if conn:
                conn.close()

    def get_loop_cnt(self) -> int:
        """
        Reads the loop count for this instance's loop_id from the database.
        If not found, it initializes the count to 0.
        """
        conn = self._connect()
        if not conn:
            return 0 # Return a default value if connection fails

        try:
            cursor = conn.cursor()
            # Ensure table exists before trying to select
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loop_counts (
                    loop_id TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
            ''')
            cursor.execute("SELECT count FROM loop_counts WHERE loop_id = ?", (self.loop_id,))
            row = cursor.fetchone()

            if row:
                self.loop_cnt = row[0]
                logging.debug("PkLoop count for '%s' retrieved: %d", self.loop_id, self.loop_cnt)
            else:
                logging.warning("No loop count found for '%s'. Initializing to 0.", self.loop_id)
                self.init_loop_cnt() # This will set self.loop_cnt to 0
            
            return self.loop_cnt

        except sqlite3.Error as e:
            logging.error("Database error in PkLoop.get_loop_cnt for loop_id '%s': %s. Returning 0.", self.loop_id, e)
            self.init_loop_cnt() # Try to recover by initializing
            return 0
        finally:
            if conn:
                conn.close()

    def set_loop_cnt(self, count: int):
        """
        Saves the given count value for this instance's loop_id to the database.
        """
        conn = self._connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO loop_counts (loop_id, count) VALUES (?, ?)", (self.loop_id, count))
            conn.commit()
            self.loop_cnt = count
            logging.info("PkLoop count for '%s' set to %d.", self.loop_id, count)
            return True
        except sqlite3.Error as e:
            logging.error("Database error in PkLoop.set_loop_cnt for loop_id '%s': %s", self.loop_id, e)
            return False
        finally:
            if conn:
                conn.close()

    def __repr__(self):
        return f"PkLoop(loop_id='{self.loop_id}', loop_cnt={self.loop_cnt})"
