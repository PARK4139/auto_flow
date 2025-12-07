import logging
import sqlite3
import traceback
from pathlib import Path
from typing import List

from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_objects.pk_files import F_MEDIA_FILES_SQLITE


import logging
import sqlite3
import traceback
from pathlib import Path
from typing import List

from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_objects.pk_files import F_MEDIA_FILES_SQLITE
from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_media_files_db_updated_for_path import ensure_media_files_db_updated_for_path
from pk_internal_tools.pk_functions.ensure_media_files_db_updated_from_all_drives import ensure_media_files_db_updated_from_all_drives


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


def ensure_get_all_media_file_paths_from_db() -> List[str]:
    """
    media_files.sqlite 데이터베이스에서 모든 미디어 파일 경로를 조회하여 반환합니다.
    DB가 없거나 유효하지 않으면 사용자에게 경로를 입력받아 DB를 생성하도록 유도합니다.
    """
    db_path = Path(F_MEDIA_FILES_SQLITE)
    logging.debug(f"DB 경로: {db_path}")

    if not _is_valid_media_files_db(db_path):
        logging.warning(f"미디어 파일 데이터베이스가 존재하지 않거나 유효하지 않습니다: {db_path}")

        # 부모 디렉토리 생성 (없을 경우)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        func_n = get_caller_name()
        
        scan_mode_options = ["부분 스캔 (특정 폴더)", "전체 스캔 (모든 드라이브)"]
        selected_scan_mode = ensure_value_completed_2025_11_11(
            key_name="db_creation_scan_mode_selection",
            func_n=func_n,
            options=scan_mode_options,
            guide_text="스캔 모드를 선택하세요 (DB 생성용):"
        )

        if not selected_scan_mode:
            logging.info("DB 생성을 위한 스캔 모드 선택이 취소되었습니다.")
            return []

        if selected_scan_mode == "부분 스캔 (특정 폴더)":
            path_to_scan_partially = ensure_value_completed_2025_11_11(
                key_name="path_to_scan_partially",
                func_n=func_n,
                guide_text="DB를 생성하기 위해 스캔할 폴더의 경로를 입력하세요 (취소하려면 빈 값으로 Enter):",
                options=[] # 사용자가 직접 입력
            )

            if not path_to_scan_partially:
                logging.info("부분 스캔 경로 입력이 취소되었습니다.")
                return []

            scan_path = Path(path_to_scan_partially)
            if not scan_path.is_dir():
                logging.error(f"입력한 경로가 유효한 디렉토리가 아닙니다: {scan_path}")
                return []
                
            logging.info(f"'{scan_path}' 경로의 미디어 파일을 스캔하여 DB를 생성합니다.")
            ensure_media_files_db_updated_for_path(scan_path) # 디렉토리 경로 전달
            
        elif selected_scan_mode == "전체 스캔 (모든 드라이브)":
            logging.info("시스템의 모든 드라이브를 스캔하여 DB를 생성합니다.")
            ensure_media_files_db_updated_from_all_drives()
            
        else:
            logging.info("DB 생성을 위한 스캔 모드 선택이 유효하지 않습니다.")
            return []

        # 재귀적으로 함수를 다시 호출하여 DB에서 경로를 가져옵니다.
        return ensure_get_all_media_file_paths_from_db()

    file_paths: List[str] = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT path FROM media_files;")
        results = cursor.fetchall()

        file_paths = [row[0] for row in results]

        conn.close()
        logging.info(f"'{db_path}'에서 {len(file_paths)}개의 미디어 파일 경로 조회 성공.")
        return file_paths

    except sqlite3.Error as e:
        logging.error(f"데이터베이스 오류 발생: {e}")
        return []
    except Exception:
        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        logging.error(f"예상치 못한 오류 발생: {traceback.format_exc()}")
        return []


if __name__ == '__main__':
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    paths = ensure_get_all_media_file_paths_from_db()
    if paths:
        logging.info("미디어 파일 경로 예시:")
        for p in paths[:5]:  # 상위 5개만 출력
            logging.info(f"- {p}")
    else:
        logging.info("미디어 파일 경로를 가져올 수 없습니다.")
