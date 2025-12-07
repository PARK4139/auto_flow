import json
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_directories import D_TTL_CACHE


# logging.basicConfig(level=logging.DEBUG) # 임시 추가 (제거)

class PathEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Path):
            return str(o)
        return super().default(o)


class PkTTLCache:
    """이 유틸은  데코레이터 스타일 + 직접 get/set 형태 모두 지원"""

    def __init__(self, ttl_seconds: int = 5, maxsize: int = 128, db_path=None):
        from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
        from pathlib import Path

        if db_path:
            self.db_path = db_path
            print(f"DEBUG: PkTTLCache initialized with custom db_path: {self.db_path}")  # print 문 추가
        else:
            self.db_path = D_TTL_CACHE / "ensure_pk_ttl_cached.sqlite"
            print(f"DEBUG: PkTTLCache initialized with default db_path: {self.db_path}")  # print 문 추가

        if self.db_path != ":memory:":
            db_path_obj = Path(self.db_path)
            if not db_path_obj.exists():
                ensure_pnx_made(db_path_obj, mode='f')

        self.ttl = ttl_seconds
        self.maxsize = maxsize
        self._ensure_table()

    def _ensure_table(self):
        import sqlite3

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                         CREATE TABLE IF NOT EXISTS pk_ttl_cache
                         (
                             cache_key
                             TEXT
                             PRIMARY
                             KEY,
                             cache_value
                             TEXT,
                             timestamp
                             REAL
                         )
                         ''')
            conn.commit()

    def _count(self, conn):
        return conn.execute('SELECT COUNT(*) FROM pk_ttl_cache').fetchone()[0]

    def count(self):
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            return self._count(conn)

    def _enforce_maxsize(self, conn):
        import logging
        count = self._count(conn)
        if count > self.maxsize:
            to_remove = count - self.maxsize
            logging.debug(f"Maxsize ({self.maxsize}) exceeded. Evicting {to_remove} oldest items.")
            conn.execute('''
                         DELETE
                         FROM pk_ttl_cache
                         WHERE cache_key IN (SELECT cache_key
                                             FROM pk_ttl_cache
                                             ORDER BY timestamp ASC
                             LIMIT ?
                             )
                         ''', (to_remove,))
            conn.commit()

    def set(self, key: str, value):
        import json
        import sqlite3
        import time
        import logging

        now = time.time()
        if hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
            serializable_value = value.to_dict()
        else:
            serializable_value = value

        value_str = json.dumps(serializable_value, cls=PathEncoder)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO pk_ttl_cache (cache_key, cache_value, timestamp)
                VALUES (?, ?, ?)
            ''', (key, value_str, now))
            self._enforce_maxsize(conn)
            current_count = self._count(conn)
            logging.debug(f"Cache set. Current size: {current_count}/{self.maxsize}")

    def get(self, key: str):
        import json
        import sqlite3
        import time
        import logging  # Import logging

        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute('''
                               SELECT cache_value, timestamp
                               FROM pk_ttl_cache
                               WHERE cache_key = ?
                               ''', (key,)).fetchone()

            if row:
                value_str, ts = row
                if now - ts < self.ttl:
                    # logging.debug(f"Hit for key '{key}'.")
                    logging.debug(f"Hit for key")
                    return json.loads(value_str)  # 문자열 → 리스트 복원
                else:
                    self.invalidate(key)
                    # logging.debug(f"Cache '{key}' expired and invalidated.")  # Log expiration
                    logging.debug(f"Cache expired and invalidated.")  # Log expiration
            # logging.debug(f"Miss for key '{key}'.")  # Log cache miss
            logging.debug(f"Miss for key")  # Log cache miss
        return None

    def invalidate(self, key: str):
        import sqlite3

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM pk_ttl_cache WHERE cache_key = ?', (key,))
            conn.commit()

    def clear(self):
        import sqlite3

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM pk_ttl_cache')
            conn.commit()

    def decorator(self):
        import logging

        def wrapper_factory(func):
            from functools import wraps

            @wraps(func)
            def wrapped(*args, **kwargs):
                key = f"{func.__module__}.{func.__name__}:{str((args, tuple(sorted(kwargs.items()))))}"
                cached_result = self.get(key)
                if cached_result is not None:
                    logging.debug(f"cached used function name={func.__name__}")
                    # logging.debug(f"데코레이터가 반환하는 캐시된 값: {cached_result}")  #
                    logging.debug(f"cache count={len(cached_result)}")  #
                    logging.debug(f"Current size after hit={self.count()}/{self.maxsize}")  # Log current size after hit
                    return cached_result
                result = func(*args, **kwargs)
                self.set(key, result)
                logging.debug(f"new cache value={result}")  #
                logging.debug(f"Current size after miss and set={self.count()}/{self.maxsize}")  # Log current size after miss and set
                return result

            return wrapped

        return wrapper_factory


@ensure_seconds_measured
def ensure_pk_ttl_cached(ttl_seconds=5, maxsize=64, db_path=None):
    # TODO : # TODO : get_filtered_media_files 의 결과가 None or "" 처럼 파일이 없는 경우 라면 캐시가 초기화되도록 수정. 반드시 목록 1개라도 있도록 하기 위함.
    # maxsize= 128
    return PkTTLCache(ttl_seconds=ttl_seconds, maxsize=maxsize, db_path=db_path).decorator()
