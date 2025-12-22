import logging
import sqlite3
from pathlib import Path
import os
import shutil
import datetime
import time 
import re

from pk_internal_tools.pk_objects.pk_directories import D_PK_RECYCLE_BIN, D_PK_CACHE
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

MAX_DUPLICATE_ATTEMPTS = 100  # 중복 파일명을 허용하는 최대 시도 횟수
DB_FILE = Path(D_PK_CACHE) / "files_gathered.db"

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
    def _onerror_callback(err):
        logging.error(f"os.walk 오류 발생: {err}")

    for root, _, files in os.walk(d_working, onerror=_onerror_callback):
        for f in files:
            full_path = Path(os.path.join(root, f))
            if full_path.is_file():
                try:
                    # INSERT ... ON CONFLICT 로직으로 변경
                    # DB에 파일이 이미 존재하면 (original_path UNIQUE), 'pending' 상태로 리셋하여 다시 이동 대상으로 만듭니다.
                    db.execute(
                        """
                        INSERT INTO files (original_path, file_name, file_extension, file_size, status, destination_path, error_message)
                        VALUES (?, ?, ?, ?, 'pending', NULL, NULL)
                        ON CONFLICT(original_path) DO UPDATE SET
                            status = 'pending',
                            updated_at = datetime('now', 'localtime'),
                            destination_path = NULL,
                            error_message = NULL,
                            file_name = excluded.file_name,
                            file_extension = excluded.file_extension,
                            file_size = excluded.file_size;
                        """,
                        (str(full_path), full_path.name, full_path.suffix, full_path.stat().st_size)
                    )
                    db.commit()
                except Exception as e:
                    logging.error(f"DB에 파일 정보 저장/업데이트 중 오류 발생: {full_path} - {e}")
                    db.pk_db_connection.rollback()
    logging.info(f"파일 스캔 및 DB 저장 완료.")
    db.close() # 파일 스캔 직후 DB 연결 닫기

    # n. 파일 이동 (DB 기반)
    logging.info(f"DB에 저장된 파일을 '{d_working}' 최상위로 이동 시작...")
    # db 인스턴스를 새로 얻습니다. (파일 스캔 시 닫았으므로)
    db = _get_db_instance() # DB 연결 다시 열기
    time.sleep(0.5) # 파일 스캔 후 파일 핸들이 해제될 시간을 줍니다.
    files_to_move = db.query("SELECT * FROM files WHERE status = 'pending'")
    for file_info in files_to_move:
        file_id = file_info['id']
        original_path = Path(file_info['original_path'])
        
        # 원본 파일이 존재하지 않는 경우, 에러 처리
        if not original_path.exists():
            error_msg = f"원본 파일이 존재하지 않습니다: {original_path}"
            logging.error(error_msg)
            db.execute(
                "UPDATE files SET status = 'error', error_message = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                (error_msg, file_id)
            )
            db.commit()
            continue

        file_name = file_info['file_name']
        
        # 파일이 이미 목적지에 있는 경우 건너뛰기
        destination_path = Path(d_working) / file_name
        if original_path.resolve() == destination_path.resolve():
            logging.info(f"파일이 이미 목적지에 있습니다. 건너뜁니다: {original_path}")
            db.execute(
                "UPDATE files SET status = 'skipped', updated_at = datetime('now', 'localtime') WHERE id = ?",
                (file_id,)
            )
            db.commit()
            continue

        # 중복 파일명 처리
        attempt = 0
        base, ext = os.path.splitext(file_name)
        
        # 사용자 요청: 기존 중복 패턴이 있으면 제거하고 새로 붙임
        base = re.sub(r'_DUPLICATED_\d{4}_\d{2}_\d{2}_\d{6}_\d+$', '', base)
        
        # 정리된 base로 목적지 경로 다시 설정
        destination_path = Path(d_working) / (base + ext)

        while destination_path.exists() and attempt < MAX_DUPLICATE_ATTEMPTS:
            # 원본 스크립트의 타임스탬프 형식 유지
            now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
            new_file_name = f"{base}_DUPLICATED_{now}_{attempt}{ext}"
            destination_path = Path(d_working) / new_file_name
            attempt += 1
        
        if destination_path.exists():
            error_msg = f"파일 이동 실패: 중복 파일명 처리 시도 횟수 초과 ({MAX_DUPLICATE_ATTEMPTS}). {original_path}"
            logging.error(error_msg)
            db.execute(
                "UPDATE files SET status = 'error', error_message = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                (error_msg, file_id)
            )
            db.commit()
            continue
            
        # 파일 이동
        try:
            logging.debug(f"파일 이동 시도: {original_path} -> {destination_path}")
            shutil.move(str(original_path), str(destination_path))
            logging.info(f"파일 이동 완료: {original_path} -> {destination_path}")

            # DB 업데이트
            db.execute(
                "UPDATE files SET status = 'moved', destination_path = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                (str(destination_path), file_id)
            )
            db.commit()

        except Exception as e:
            error_msg = f"파일 이동 실패: {original_path} -> {destination_path} | {e}"
            logging.error(error_msg)
            db.execute(
                "UPDATE files SET status = 'error', error_message = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
                (error_msg, file_id)
            )
            db.commit()
    logging.info(f"DB 기반 파일 이동 완료.")

    # n. 하위 디렉토리 중 빈 디렉토리만 재귀적으로 제거
    logging.debug(f"빈 디렉토리 정리 시작. d_working: {d_working}")
    for root, dirs, _ in os.walk(d_working, topdown=False):
        for dir_name in dirs:
            full_dir = Path(os.path.join(root, dir_name))
            logging.debug(f"처리 중인 디렉토리: {full_dir}")
            try:
                is_empty = not any(entry for entry in os.scandir(full_dir) if not entry.name.startswith('.'))
                logging.debug(f"'{full_dir}'의 비어있음 여부 (is_empty): {is_empty}")
                if not is_empty: # 디렉토리가 비어 있지 않은 경우, 내용을 로깅하여 무엇이 남아있는지 확인
                    remaining_entries = [entry.name for entry in os.scandir(full_dir) if not entry.name.startswith('.')]
                    logging.debug(f"'{full_dir}'에 남아있는 엔트리 (dotfiles 제외): {remaining_entries}")
                if is_empty:
                    rel_path = full_dir.relative_to(d_working)
                    new_dir_path_base = D_PK_RECYCLE_BIN / rel_path

                    final_recycle_path = new_dir_path_base
                    attempt = 0
                    while final_recycle_path.exists():
                        now = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
                        final_recycle_path = D_PK_RECYCLE_BIN / f"{rel_path.name}_DUPLICATED_{now}_{attempt}"
                        attempt += 1
                        if attempt > MAX_DUPLICATE_ATTEMPTS:
                            logging.error(f"휴지통으로 디렉토리 이동 실패: 중복 처리 시도 횟수 초과 ({MAX_DUPLICATE_ATTEMPTS}). {full_dir}")
                            break # While 루프 중단

                    if not final_recycle_path.exists():
                        logging.debug(f"빈 디렉토리 이동 시도: {full_dir} -> {final_recycle_path}")
                        os.makedirs(final_recycle_path.parent, exist_ok=True)
                        shutil.move(str(full_dir), str(final_recycle_path))
                        logging.info(f"빈 디렉토리 이동됨: {full_dir} → {final_recycle_path}")
            except Exception as e:
                logging.error(f"디렉토리 확인 또는 이동 중 오류 발생: {full_dir} - {e}")

    logging.info(f"모든 파일은 d_working 최상위로 이동 완료: {d_working}")
    logging.info(f"비어 있는 디렉토리는 {D_PK_RECYCLE_BIN} 으로 이동 완료")

    db.close()  # DB 연결 닫기

    # .geminiignore 파일 읽기
    ignored_patterns = []
    geminiignore_path = d_working / ".geminiignore"
    if geminiignore_path.exists():
        with open(geminiignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignored_patterns.append(line)

    def _is_ignored(file_path: Path) -> bool:
        if file_path.name == ".geminiignore":
            return True
        for pattern in ignored_patterns:
            # Glob 패턴 매칭 (fnmatch 사용)
            if file_path.match(pattern) or Path(file_path.name).match(pattern):
                return True
        return False

    # 최종적으로 d_working의 최상위 레벨에 남아있는 파일 목록을 반환
    logging.debug(f"d_working 디렉토리의 현재 내용 (iterdir): {[str(p.relative_to(d_working)) for p in d_working.iterdir()]}")
    final_gathered_files = []
    for item in d_working.iterdir(): # d_working의 직접적인 자식만 확인
        logging.debug(f"처리 중인 항목: {item.name}, is_file: {item.is_file()}, _is_ignored: {_is_ignored(item)}")
        if item.is_file() and not _is_ignored(item):
            final_gathered_files.append(item)
            
    logging.debug(f"최종 수집된 파일 목록 (final_gathered_files): {[str(p.relative_to(d_working)) for p in final_gathered_files]}")
    return final_gathered_files
