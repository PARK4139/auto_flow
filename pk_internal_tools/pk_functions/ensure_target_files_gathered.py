import logging
import sqlite3
from pathlib import Path
import os
import shutil
import datetime

from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN, d_pk_cache
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

MAX_DUPLICATE_ATTEMPTS = 100  # 중복 파일명을 허용하는 최대 시도 횟수
DB_FILE = Path(d_pk_cache) / "files_gathered.db"

def _get_db_instance():
    db = PkSqlite3(db_path=DB_FILE)
    # DB 안정성을 위한 PRAGMA 설정
    db.pk_db_connection.execute("PRAGMA journal_mode=WAL;")
    db.pk_db_connection.execute("PRAGMA synchronous=NORMAL;")
    return db

def ensure_target_files_gathered(d_working):
    db = _get_db_instance()
    db.ensure_table_exists(
        table_name='files',
        columns={
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'original_path': 'TEXT NOT NULL UNIQUE',
            'file_name': 'TEXT NOT NULL',
            'file_extension': 'TEXT',
            'file_size': 'INTEGER',
            'status': "TEXT NOT NULL DEFAULT 'pending'",
            'destination_path': 'TEXT',
            'error_message': 'TEXT',
            'created_at': "TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))",
            'updated_at': "TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))"
        }
    )

    d_working = Path(d_working)

    if not os.path.exists(d_working):
        logging.error(f"d_working 경로가 존재하지 않습니다: {d_working}")
        return

    # n. 하위 모든 파일 수집 (DB에 저장)
    logging.info(f"'{d_working}' 디렉토리에서 파일 스캔 및 DB에 저장 시작...")
    for root, _, files in os.walk(d_working):
        for f in files:
            full_path = Path(os.path.join(root, f))
            if full_path.is_file():
                try:
                    db.execute(
                        """
                        INSERT INTO files (original_path, file_name, file_extension, file_size)
                        VALUES (?, ?, ?, ?) 
                        """,
                        (str(full_path), full_path.name, full_path.suffix, full_path.stat().st_size)
                    )
                    db.commit()
                except sqlite3.IntegrityError:
                    logging.debug(f"파일이 이미 DB에 존재합니다 (original_path): {full_path}")
                except Exception as e:
                    logging.error(f"DB에 파일 정보 저장 중 오류 발생: {full_path} - {e}")
                    db.pk_db_connection.rollback()
    logging.info(f"파일 스캔 및 DB 저장 완료.")

    # n. 파일 이동 (DB 기반)
    logging.info(f"DB에 저장된 파일을 '{d_working}' 최상위로 이동 시작...")
    files_to_move = db.query("SELECT * FROM files WHERE status = 'pending'")
    for file_info in files_to_move:
        file_id = file_info['id']
        original_path = Path(file_info['original_path'])
        filename = file_info['file_name']
        base, ext = os.path.splitext(filename)
        
        dst_path = Path(d_working) / filename # 초기 목적지 경로

        attempt = 0
        current_dst_path = dst_path # 중복 처리 시 변경될 목적지 경로

        while attempt < MAX_DUPLICATE_ATTEMPTS:
            if original_path.resolve() == current_dst_path.resolve():
                logging.info(f"파일이 이미 목적지에 있습니다. 건너뜁니다: {original_path}")
                db.execute(
                    "UPDATE files SET status = 'skipped', updated_at = datetime('now', 'localtime') WHERE id = ?",
                    (file_id,)
                )
                db.commit()
                break

            if not current_dst_path.exists():
                try:
                    shutil.move(str(original_path), str(current_dst_path))
                    logging.info(f"파일 이동 완료: {original_path} -> {current_dst_path}")
                    db.execute(
                        "UPDATE files SET status = 'moved', destination_path = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                        (str(current_dst_path), file_id)
                    )
                    db.commit()
                    break
                except PermissionError:
                    error_msg = f"[PERMISSION ERROR] 파일 이동 실패 (열려있을 수 있음): {original_path}"
                    logging.error(error_msg)
                    db.execute(
                        "UPDATE files SET status = 'error', error_message = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                        (error_msg, file_id)
                    )
                    db.commit()
                    break
                except Exception as e:
                    error_msg = f"파일 이동 실패: {original_path} -> {current_dst_path} | {e}"
                    logging.error(error_msg)
                    db.execute(
                        "UPDATE files SET status = 'error', error_message = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                        (error_msg, file_id)
                    )
                    db.commit()
                    break
            else:
                now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
                new_filename = f"{base}_DUPLICATED_{now}_{attempt}{ext}"
                current_dst_path = Path(d_working) / new_filename
                attempt += 1
        else: # while 루프가 MAX_DUPLICATE_ATTEMPTS에 도달했을 때
            error_msg = f"파일 이동 실패: 중복 파일명 처리 시도 횟수 초과 ({MAX_DUPLICATE_ATTEMPTS}). {original_path}"
            logging.error(error_msg)
            db.execute(
                "UPDATE files SET status = 'error', error_message = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                (error_msg, file_id)
            )
            db.commit()
    logging.info(f"DB 기반 파일 이동 완료.")

    # n. 하위 디렉토리 중 빈 디렉토리만 재귀적으로 제거
    for root, dirs, _ in os.walk(d_working, topdown=False):
        for dir_name in dirs:
            full_dir = os.path.join(root, dir_name)
            try:
                if not any(entry for entry in os.scandir(full_dir) if not entry.name.startswith('.')):
                    rel_path = os.path.relpath(full_dir, start=d_working)
                    new_dir_path = os.path.join(D_PK_RECYCLE_BIN, rel_path)

                    if os.path.exists(new_dir_path):
                        base = os.path.basename(rel_path)
                        now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
                        new_dir_path = os.path.join(D_PK_RECYCLE_BIN, f"{base}_DUPLICATED_{now}")

                    os.makedirs(os.path.dirname(new_dir_path), exist_ok=True)
                    shutil.move(full_dir, new_dir_path)
                    logging.info(f"빈 디렉토리 이동됨: {full_dir} → {new_dir_path}")
            except Exception as e:
                logging.error(f"디렉토리 확인 중 오류 발생: {full_dir} - {e}")

    logging.info(f"모든 파일은 d_working 최상위로 이동 완료: {d_working}")
    logging.info(f"비어 있는 디렉토리는 {D_PK_RECYCLE_BIN} 으로 이동 완료")

    db.close() # DB 연결 닫기
