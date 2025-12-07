import sqlite3
import logging
from pathlib import Path
import time
from typing import List, Tuple
import os

from pk_internal_tools.pk_objects.pk_files import F_MEDIA_FILES_SQLITE
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_objects.pk_file_extensions import FILE_EXTENSIONS
import traceback

# media_files 테이블 생성 쿼리 (만약 존재하지 않는다면)
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS media_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    size INTEGER NOT NULL,
    mtime REAL NOT NULL,
    ctime REAL NOT NULL,
    d_working TEXT NOT NULL
);
"""

# INSERT 또는 UPDATE 쿼리
UPSERT_SQL = """
INSERT INTO media_files (path, name, size, mtime, ctime, d_working)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT(path) DO UPDATE SET
    name = EXCLUDED.name,
    size = EXCLUDED.st_size,
    mtime = EXCLUDED.st_mtime,
    ctime = EXCLUDED.st_ctime,
    d_working = EXCLUDED.d_working;
"""

def ensure_media_files_db_updated_from_all_drives():
    """
    시스템의 모든 사용 가능한 드라이브를 스캔하고 media_files.sqlite 데이터베이스를 업데이트합니다.
    미디어 파일(비디오, 오디오)만 데이터베이스에 추가/업데이트합니다.
    """
    db_path = Path(F_MEDIA_FILES_SQLITE)
    db_path.parent.mkdir(parents=True, exist_ok=True) # DB 파일의 부모 디렉토리가 없으면 생성

    # 미디어 파일 확장자 목록 가져오기
    media_extensions = FILE_EXTENSIONS['videos'].union(FILE_EXTENSIONS['audios'])

    total_scanned_count = 0
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_SQL) # 테이블 생성 (존재하지 않으면)
        conn.commit()

        # Windows 드라이브 문자 탐색 (C:, D: 등)
        drives = [f'{d}:\\' for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f'{d}:\\')]
        
        logging.info(f"전체 드라이브 스캔 시작. 대상 드라이브: {drives}")

        for drive_path_str in drives:
            current_drive_path = Path(drive_path_str)
            if not current_drive_path.is_dir():
                logging.warning(f"드라이브를 찾을 수 없거나 접근할 수 없습니다: {current_drive_path}. 건너뜁니다.")
                continue
            
            logging.info(f"'{current_drive_path}' 드라이브 스캔 시작...")
            
            # TODO: `node_modules`, `.git` 등 제외 로직 추가 필요
            # 현재는 모든 파일을 재귀적으로 탐색하지만, 성능과 권한 문제를 고려하여
            # 특정 디렉토리를 건너뛰는 명시적인 로직을 추가하는 것이 좋습니다.
            
            for file_path in current_drive_path.rglob('*'): # 재귀적으로 모든 파일 탐색
                try:
                    if file_path.is_file():
                        # 파일 확장자 필터링
                        if file_path.suffix.lower() in media_extensions:
                            try:
                                stat = file_path.stat()
                                data = (
                                    str(file_path),
                                    file_path.name,
                                    stat.st_size,
                                    stat.st_mtime,
                                    stat.st_ctime,
                                    str(current_drive_path) # d_working은 스캔 시작 경로로 설정
                                )
                                cursor.execute(UPSERT_SQL, data)
                                total_scanned_count += 1
                            except OSError as e:
                                logging.warning(f"파일 정보 접근 오류: {file_path} - {e}")
                            except Exception as e:
                                logging.error(f"파일 처리 중 예상치 못한 오류: {file_path} - {e}")
                except OSError as e:
                    logging.warning(f"경로 접근 오류 발생, 건너뜀: {file_path} - {e}")
                except Exception as e:
                    logging.error(f"예상치 못한 오류 발생, 건너뜀: {file_path} - {e}")
            
            conn.commit() # 각 드라이브 스캔 후 커밋
            logging.info(f"'{current_drive_path}' 드라이브 스캔 완료.")
        
        conn.close()
        logging.info(f"전체 드라이브 스캔 완료. 총 {total_scanned_count}개 파일 업데이트.")

    except sqlite3.Error as e:
        logging.error(f"데이터베이스 오류 발생: {e}")
    except Exception:
        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        logging.error(f"예상치 못한 오류 발생: {traceback.format_exc()}")

if __name__ == '__main__':
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    ensure_media_files_db_updated_from_all_drives()
