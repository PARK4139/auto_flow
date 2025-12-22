import logging
import os
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict

from pk_internal_tools.pk_functions.get_drives_connected import get_drives_connected
from pk_internal_tools.pk_functions.get_windows_os_system_path_sql_like_patterns import get_windows_os_system_path_sql_like_patterns
from pk_internal_tools.pk_objects.pk_directories import D_PK_CACHE


@contextmanager
def get_sqlite3_connection(db_path: Path):
    """
    SQLite 데이터베이스 연결을 제공하는 컨텍스트 관리자입니다.

    Args:
        db_path (Path): 데이터베이스 파일의 경로입니다.

    Yields:
        sqlite3.Connection: 데이터베이스 연결 객체입니다.

    Raises:
        sqlite3.Error: 데이터베이스 연결 중 오류가 발생할 경우 발생합니다.
    """
    try:
        conn = sqlite3.connect(db_path, timeout=10)
        yield conn
    except sqlite3.Error as e:
        logging.error(f"Database error at {db_path}: {e}")
        raise
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def get_db_path(target_type: str) -> Path:
    """
    주어진 타겟 타입에 대한 SQLite 데이터베이스 파일의 경로를 반환합니다.

    Args:
        target_type (str): 타겟의 유형 ("파일", "디렉토리", "모두")입니다.

    Returns:
        Path: 데이터베이스 파일의 경로입니다.
    """
    db_dir = Path(D_PK_CACHE) / "pk_pnx_dbs_scanned"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_map = {
        "파일": "drives_scanned_file_only.sqlite",
        "디렉토리": "drives_scanned_directory_only.sqlite",
        "모두": "drives_scanned_both_file_directory.sqlite",
    }
    return db_dir / db_map[target_type]


def init_db(db_path: Path):
    """
    지정된 경로에 데이터베이스 테이블을 초기화합니다.

    Args:
        db_path (Path): 초기화할 데이터베이스 파일의 경로입니다.
    """
    with get_sqlite3_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS targets (path TEXT PRIMARY KEY, type TEXT, last_scanned REAL)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON targets(type)")
        conn.commit()


def handle_walk_error(e):
    """
    os.walk 중 발생하는 오류를 처리하고 로깅합니다.

    Args:
        e (OSError): os.walk에서 발생한 오류 객체입니다.
    """
    logging.warning(f"os.walk 접근 오류: {e.file_name} - {e.strerror}")


def backup_existing_dbs(db_paths: Dict[str, Path]):
    """
    기존 데이터베이스 파일들을 백업합니다.

    Args:
        db_paths (Dict[str, Path]): 백업할 데이터베이스 파일 경로들의 딕셔너리입니다.
    """
    backup_dir = db_paths["모두"].parent / "backup"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for db_type, db_path in db_paths.items():
        if db_path.exists():
            try:
                size_mb = db_path.stat().st_size / (1024 * 1024)
                logging.info(f"기존 '{db_type}' DB 파일을 백업합니다. (크기: {size_mb:.2f} MB)")
                backup_file_name = f"{db_path.stem}_backup_{timestamp}{db_path.suffix}"
                backup_path = backup_dir / backup_file_name
                shutil.copy2(db_path, backup_path)
                logging.info(f"백업 완료: {backup_path}")
            except Exception as e:
                logging.error(f"DB 파일 백업 중 오류 발생 ({db_path}): {e}")


def ensure_target_file_system_scanned():
    """
    연결된 모든 드라이브를 스캔하여 파일 및 디렉토리 정보를 SQLite DB에 저장합니다.
    기존 DB 데이터는 삭제되고 현재 스캔된 데이터로 대체됩니다.
    """
    db_paths = {tt: get_db_path(tt) for tt in ["파일", "디렉토리", "모두"]}
    backup_existing_dbs(db_paths)
    for db_path in db_paths.values(): init_db(db_path)
    scan_roots = get_drives_connected()
    logging.info(f"전체 스캔을 시작합니다. 대상 드라이브: {scan_roots}")
    if not scan_roots:
        logging.warning("스캔할 드라이브를 찾을 수 없습니다. 'get_drives_connected()' 함수를 확인하세요.")
        return # 스캔할 드라이브가 없으면 함수 종료

    files_to_insert, dirs_to_insert = [], []
    scan_time = datetime.now().timestamp()
    system_filters = get_windows_os_system_path_sql_like_patterns() # 루프 밖으로 이동하여 불필요한 반복 호출 방지
    excluded_dir_names = [f.replace('%', '').lower() for f in system_filters]

    for scan_root in scan_roots:
        logging.info(f"드라이브 스캔 중: {scan_root}")

        walk_path = scan_root
        if os.name == 'nt':
            walk_path = f"\\\\?\\{scan_root}"
        logging.debug(f"대상 walk_path: {walk_path}")

        try:
            for root, dirs, files in os.walk(walk_path, onerror=handle_walk_error):
                # Exclude system directories from scanning
                dirs[:] = [d for d in dirs if d.lower() not in excluded_dir_names]
                logging.debug(f"현재 디렉토리: {root}, 필터링 후 하위 디렉토리: {dirs}, 파일 수: {len(files)}")

                for d in dirs:
                    dirs_to_insert.append((os.path.join(root, d), "directory", scan_time))
                for f in files:
                    files_to_insert.append((os.path.join(root, f), "file", scan_time))
        except Exception as e:
            logging.error(f"드라이브 스캔 중 예외 발생: {scan_root} - {e}", exc_info=True) # 트레이스백 추가
    logging.info(f"총 {len(files_to_insert)}개의 파일과 {len(dirs_to_insert)}개의 디렉토리를 찾았습니다. DB에 저장합니다...")

    # 파일 DB 저장
    logging.debug(f"파일 DB ({db_paths['파일']})에 {len(files_to_insert)}개 항목 삽입 시도.")
    with get_sqlite3_connection(db_paths["파일"]) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM targets")
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert)
        conn.commit()
    logging.debug(f"파일 DB 저장 완료. 현재 DB 항목 수: {cursor.rowcount if hasattr(cursor, 'rowcount') else 'N/A'}")

    # 디렉토리 DB 저장
    logging.debug(f"디렉토리 DB ({db_paths['디렉토리']})에 {len(dirs_to_insert)}개 항목 삽입 시도.")
    with get_sqlite3_connection(db_paths["디렉토리"]) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM targets")
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", dirs_to_insert)
        conn.commit()
    logging.debug(f"디렉토리 DB 저장 완료. 현재 DB 항목 수: {cursor.rowcount if hasattr(cursor, 'rowcount') else 'N/A'}")

    # 모두 DB 저장
    logging.debug(f"모두 DB ({db_paths['모두']})에 {len(files_to_insert) + len(dirs_to_insert)}개 항목 삽입 시도.")
    with get_sqlite3_connection(db_paths["모두"]) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM targets")
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert + dirs_to_insert)
        conn.commit()
    logging.debug(f"모두 DB 저장 완료. 현재 DB 항목 수: {cursor.rowcount if hasattr(cursor, 'rowcount') else 'N/A'}")

    logging.info("전체 스캔 및 DB 저장이 완료되었습니다.")
