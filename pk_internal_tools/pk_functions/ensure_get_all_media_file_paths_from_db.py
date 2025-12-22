import logging
import sqlite3
import traceback
from pathlib import Path
from typing import List, Optional
import re # Added for REGEXP function

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_media_files_db_updated_for_path import ensure_media_files_db_updated_for_path
from pk_internal_tools.pk_functions.ensure_media_files_db_updated_from_all_drives import ensure_media_files_db_updated_from_all_drives
from pk_internal_tools.pk_objects.pk_files import F_MEDIA_FILES_SQLITE
from pk_internal_tools.pk_functions._pk_target_db_utils import get_db_path, ensure_target_file_system_scanned




def _is_valid_media_files_db(db_path: Path) -> bool:
    """
    media_files.sqlite 데이터베이스 파일이 존재하고
    'media_files' 테이블이 포함되어 있는지 확인합니다.
    """
    if not db_path.exists():
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media_files';")
        table_exists = cursor.fetchone() is not None
        conn.close()
        return table_exists
    except sqlite3.Error as e:
        logging.error(f"DB 유효성 검사 중 오류 발생: {e}")
        return False
    except Exception as e:
        logging.error(f"예상치 못한 오류 발생 (DB 유효성 검사): {e}")
        return False


def ensure_get_all_media_file_paths_from_db(
    ignore_file_name_parts: Optional[List[str]] = None,
    ignore_regex_patterns: Optional[List[str]] = None
) -> List[str]:
    """
    media_files.sqlite 데이터베이스에서 모든 미디어 파일 경로를 조회하여 반환합니다.
    DB가 없거나 유효하지 않으면 사용자에게 경로를 입력받아 DB를 생성하도록 유도합니다.
    """
    db_path = get_db_path("모두") # "모두" DB에서 조회하도록 변경
    logging.debug(f"DB 경로: {db_path}")

    # db_path.exists()와 파일 크기로 DB 존재 및 유효성 확인
    if not db_path.exists() or Path(db_path).stat().st_size == 0:
        logging.warning(f"타겟 데이터베이스가 존재하지 않거나 비어 있습니다: {db_path}")
        logging.info("DB 생성을 위해 파일 시스템 전체 스캔을 시작합니다.")
        # DB가 없으면 ensure_target_file_system_scanned 함수를 호출하여 DB를 생성
        ensure_target_file_system_scanned()
        # 스캔 후 재귀적으로 함수를 다시 호출하여 DB에서 경로를 가져옵니다.
        # 이 시점에는 DB가 생성되었을 것이므로 무한 재귀에 빠지지 않음
        return ensure_get_all_media_file_paths_from_db(
            ignore_file_name_parts=ignore_file_name_parts,
            ignore_regex_patterns=ignore_regex_patterns
        )

    file_paths: List[str] = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        where_clauses = []
        params = []

        if ignore_file_name_parts:
            for part in ignore_file_name_parts:
                where_clauses.append("path NOT LIKE ?")
                params.append(f"%{part}%")

        if ignore_regex_patterns:
            # SQLite does not have a native REGEXP operator by default.
            # It usually requires a custom function to be registered.
            # We will try to register a simple REGEXP function if not already present.
            def _sqlite_regexp(pattern, item):
                import re
                return 1 if re.search(pattern, item) else 0
            
            conn.create_function("REGEXP", 2, _sqlite_regexp)

            for pattern in ignore_regex_patterns:
                where_clauses.append("path NOT REGEXP ?")
                params.append(pattern)

        sql_query = "SELECT path FROM targets"
        if where_clauses:
            sql_query += " WHERE " + " AND ".join(where_clauses)
        sql_query += ";"
        
        logging.debug(f"DB Query: {sql_query}, Params: {params}")

        cursor.execute(sql_query, params)
        results = cursor.fetchall()

        file_paths = [row[0] for row in results]

        conn.close()
        logging.info(f"'{db_path}'에서 {len(file_paths)}개의 미디어 파일 경로 조회 성공.")
        return file_paths

    except sqlite3.Error as e:
        logging.error(f"데이터베이스 오류 발생: {e}")
        return []
    except Exception as e:
        ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
        logging.error(f"예상치 못한 오류 발생: {traceback.format_exc()}")
        return []


if __name__ == '__main__':
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    paths = ensure_get_all_media_file_paths_from_db()
    if paths:
        logging.info("미디어 파일 경로 예시:")
        for p in paths[:5]:  # 상위 5개만 출력
            logging.info(f"{p}")
    else:
        logging.info("미디어 파일 경로를 가져올 수 없습니다.")
