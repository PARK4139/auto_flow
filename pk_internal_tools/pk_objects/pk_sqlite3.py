import threading
from pathlib import Path


class PkSqlite3:
    from typing import Any
    from typing import Optional

    from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs): # *args, **kwargs는 __init__으로 전달
        import logging # logging 추가
        logging.debug(f"PkSqlite3.__new__ called with args={args}, kwargs={kwargs}")
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logging.debug("Creating new PkSqlite3 instance.")
                    cls._instance = super().__new__(cls) # *args, **kwargs 제거
        logging.debug(f"Returning PkSqlite3 instance: {cls._instance}")
        return cls._instance

    def __init__(self, db_path: Optional[Path] = None):
        from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE
        import sqlite3
        import logging # logging 추가
        from pathlib import Path # Path 추가

        logging.debug(f"PkSqlite3.__init__ called with db_path={db_path}")
        self.sqlite3 = sqlite3

        if db_path is None:
            self.f_pk_sqlite = F_pk_SQLITE
            logging.debug(f"기본 DB 경로 사용: {self.f_pk_sqlite}")
        else:
            self.f_pk_sqlite = db_path
            logging.debug(f"지정된 DB 경로 사용: {self.f_pk_sqlite}")

        self.ensure_pk_db(self.f_pk_sqlite)
        self.pk_db_connection = sqlite3.connect(str(self.f_pk_sqlite))  # Path 객체를 str로 변환
        self.ensure_pk_db_table()

    def ensure_pk_db(self, f_pk_sqlite):
        import os

        # sqlite3 는 file 기반이다. file 이 있어야 한다.
        if not os.path.exists(f_pk_sqlite):
            os.makedirs(os.path.dirname(f_pk_sqlite), exist_ok=True)

    def ensure_pk_db_table(self):
        cur = self.pk_db_connection.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS pk_table_state
                    (
                        id
                        TEXT
                        PRIMARY
                        KEY,
                        question
                        TEXT,
                        options_json
                        TEXT,
                        answer
                        TEXT
                    )
                    """)
        self.pk_db_connection.commit()

    def ensure_table_exists(self, table_name: str, columns: dict):
        """
        지정된 이름과 컬럼으로 테이블이 존재하는지 확인하고, 없으면 생성합니다.
        columns는 {'column_name': 'COLUMN_TYPE_CONSTRAINTS'} 형태의 딕셔너리입니다.
        예: {'url': 'TEXT UNIQUE', 'status': 'TEXT', 'created_at': 'TEXT'}
        """
        column_definitions = ", ".join([f"{name} {type_def}" for name, type_def in columns.items()])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        cur = self.pk_db_connection.cursor()
        cur.execute(create_table_sql)
        self.pk_db_connection.commit()

    def ensure_column_exists(self, table_name: str, column_name: str, column_type: str):
        """
        테이블에 특정 컬럼이 존재하는지 확인하고, 없으면 추가합니다.
        """
        cur = self.pk_db_connection.cursor()
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cur.fetchall()]
        if column_name not in columns:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            self.pk_db_connection.commit()

    def save_value_from_options(
            self,
            db_id: str,
            question: str,
            options: list[str],
    ) -> str:

        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        import json
        answer = ensure_value_completed(
            key_name=f'{question} ',
            options=options
        )

        cur = self.pk_db_connection.cursor()
        cur.execute("""
                    INSERT INTO pk_table_state (id, question, options_json, answer)
                    VALUES (?, ?, ?, ?) ON CONFLICT(id) DO
                    UPDATE SET
                        question=excluded.question,
                        options_json=excluded.options_json,
                        answer=excluded.answer
                    """, (db_id, question, json.dumps(options), answer))
        self.pk_db_connection.commit()
        return answer

    def save_value(
            self,
            db_id: str,
            value: list[str],
    ) -> str:

        answer = value
        cur = self.pk_db_connection.cursor()
        cur.execute("""
                    INSERT INTO pk_table_state (id, answer)
                    VALUES (?, ?) ON CONFLICT(id) DO
                    UPDATE SET
                        answer=excluded.answer
                    """, (db_id, answer))
        self.pk_db_connection.commit()
        return answer

    def default_input_func(self, message: str, answer_options: list[str]) -> str:

        print(message)
        for i, opt in enumerate(answer_options):
            print(f"{i + 1}. {opt}")
        choice = input("선택: ")
        try:
            idx = int(choice.strip()) - 1
            return answer_options[idx]
        except Exception as e:
            return answer_options[0]

    def reset_values(self, db_id: str):

        # TODO : reset_key() 도 있으면 좋겠다

        # pk db 초기화
        cur = self.pk_db_connection.cursor()
        cur.execute("UPDATE pk_table_state SET answer = NULL WHERE id = ?", (db_id,))
        self.pk_db_connection.commit()
        import logging
        logging.debug(f"db_id({db_id}) is reset")

    def set_values(self, db_id: str, values: Any):
        """
        상태 값을 데이터베이스에 저장합니다.
        
        Args:
            db_id: 데이터베이스 ID
            values: 저장할 값 (str, list, dict 등 모든 타입 지원)
        """
        self._set_state_value_impl(db_id, values)

    def _set_state_value_legacy(self, db_id: str, values):
        """
        레거시: 문자열만 저장하는 방식 (더 이상 사용하지 않음)
        
        Deprecated: _set_state_value_impl을 사용하세요.
        """
        cur = self.pk_db_connection.cursor()

        # 먼저 해당 id가 존재하는지 확인
        cur.execute("SELECT COUNT(*) FROM pk_table_state WHERE id = ?", (db_id,))
        exists = cur.fetchone()[0] > 0

        if exists:
            cur.execute("UPDATE pk_table_state SET answer = ? WHERE id = ?", (values, db_id))
        else:
            cur.execute("INSERT INTO pk_table_state (id, answer) VALUES (?, ?)", (db_id, values))

        self.pk_db_connection.commit()

    def _set_state_value_impl(self, db_id: str, values: Any):
        """
        상태 값을 JSON으로 직렬화하여 데이터베이스에 저장합니다.
        
        Args:
            db_id: 데이터베이스 ID
            values: 저장할 값 (str, list, dict 등 모든 타입 지원, JSON으로 직렬화됨)
        """
        import json

        cur = self.pk_db_connection.cursor()

        # value를 JSON 문자열로 직렬화 (ensure_ascii=False → 한글 깨짐 방지)
        serialized_value = json.dumps(values, ensure_ascii=False)

        # 해당 id가 존재하는지 확인
        cur.execute("SELECT COUNT(*) FROM pk_table_state WHERE id = ?", (db_id,))
        exists = cur.fetchone()[0] > 0

        if exists:
            cur.execute("UPDATE pk_table_state SET answer = ? WHERE id = ?", (serialized_value, db_id))
        else:
            cur.execute("INSERT INTO pk_table_state (id, answer) VALUES (?, ?)", (db_id, serialized_value))

        self.pk_db_connection.commit()

    def get_state_value(self, db_id: str) -> Optional[Any]:
        """
        데이터베이스에서 상태 값을 가져옵니다.
        
        Args:
            db_id: 데이터베이스 ID
            
        Returns:
            저장된 값 (JSON 파싱 및 타입 변환됨), 없으면 None
        """
        return self._get_state_value_impl(db_id)

    def _get_state_value_impl(self, db_id: str) -> Optional[Any]:
        """
        데이터베이스에서 상태 값을 가져와서 JSON 파싱 및 타입 변환을 수행합니다.
        
        Args:
            db_id: 데이터베이스 ID
            
        Returns:
            저장된 값 (JSON 파싱 및 타입 변환됨), 없으면 None
        """
        import json
        import logging

        cur = self.pk_db_connection.cursor()
        cur.execute("SELECT answer FROM pk_table_state WHERE id = ?", (db_id,))
        row = cur.fetchone()
        raw_value = row[0] if row else None

        if raw_value is None:
            value = None
        else:
            try:
                value = json.loads(raw_value)
            except (json.JSONDecodeError, TypeError):
                # 문자열 보정 처리
                lowered = str(raw_value).strip().lower()
                if lowered == "true":
                    value = True
                elif lowered == "false":
                    value = False
                elif lowered in ("null", "none"):
                    value = None
                elif lowered.isdigit():
                    value = int(lowered)
                else:
                    value = raw_value  # fallback 그대로 반환
        logging.debug(f"get_state_value db_id={db_id}, value={value}, type={type(value)}, repr={repr(value)}")
        return value

    # 하위 호환성을 위한 별칭
    def get_values_2025(self, db_id: str) -> Optional[Any]:
        """Deprecated: get_state_value를 사용하세요."""
        return self.get_state_value(db_id)

    def get_values_2024(self, db_id: str) -> Optional[Any]:
        """Deprecated: _get_state_value_impl를 사용하세요."""
        return self._get_state_value_impl(db_id)

    def get_db_id(self, key_name, func_n) -> str:

        self.db_id = rf"{key_name}_via_{func_n}"
        return self.db_id

    def query(self, sql: str, params: tuple = ()) -> list:
        """Runs a SELECT query and returns all results as a list of dicts."""
        self.pk_db_connection.row_factory = self.sqlite3.Row
        cur = self.pk_db_connection.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [dict(row) for row in rows]

    def execute(self, sql: str, params: tuple = ()):
        """Runs an INSERT, UPDATE, or DELETE query."""
        cur = self.pk_db_connection.cursor()
        cur.execute(sql, params)

    def executemany(self, sql: str, params_list: list):
        """Runs a query with multiple sets of parameters."""
        cur = self.pk_db_connection.cursor()
        cur.executemany(sql, params_list)

    def commit(self):
        """Commits the current transaction."""
        self.pk_db_connection.commit()

    def close(self):

        self.pk_db_connection.close()
