# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict

from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

"""
대화형 다중 타겟 검색 및 스캔 도구
- 다중 선택: fzf의 `--multi` 옵션을 사용하여 여러 파일/디렉토리를 한 번에 선택.
- 스캔: 연결된 모든 드라이브를 스캔하여 파일/디렉토리/모두 DB 3종에 동시 저장.
- 조회: DB 조회 시 SQL 필터링을 적용하고, fzf에 직접 파이핑하여 효율성 증대.
"""


# --- DB 관리 (기존 ensure_target_found.py와 동일) ---
@contextmanager
def get_db_connection(db_path: Path):
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


def get_db_path(target_type: str) -> Path:
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_directories import d_pk_cache
    db_dir = Path(d_pk_cache) / "pk_pnx_dbs_scanned"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_map = {
        "파일": "drives_scanned_file_only.sqlite",
        "디렉토리": "drives_scanned_directory_only.sqlite",
        "모두": "drives_scanned_both_file_directory.sqlite",
    }
    return db_dir / db_map[target_type]


def init_db(db_path: Path):
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS targets (path TEXT PRIMARY KEY, type TEXT, last_scanned REAL)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON targets(type)")
        conn.commit()


def _handle_walk_error(e):
    import logging
    logging.warning(f"os.walk 접근 오류: {e.filename} - {e.strerror}")


def backup_existing_dbs(db_paths: Dict[str, Path]):
    import logging
    import shutil
    from datetime import datetime

    backup_dir = db_paths["모두"].parent / "backup"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for db_type, db_path in db_paths.items():
        if db_path.exists():
            try:
                size_mb = db_path.stat().st_size / (1024 * 1024)
                logging.info(f"기존 '{db_type}' DB 파일을 백업합니다. (크기: {size_mb:.2f} MB)")
                backup_filename = f"{db_path.stem}_backup_{timestamp}{db_path.suffix}"
                backup_path = backup_dir / backup_filename
                shutil.copy2(db_path, backup_path)
                logging.info(f"백업 완료: {backup_path}")
            except Exception as e:
                logging.error(f"DB 파일 백업 중 오류 발생 ({db_path}): {e}")


def ensure_target_file_system_scanned():
    import os
    import logging
    from datetime import datetime

    from pk_internal_tools.pk_functions.get_drives_connected import get_drives_connected
    db_paths = {tt: get_db_path(tt) for tt in ["파일", "디렉토리", "모두"]}
    backup_existing_dbs(db_paths)
    for db_path in db_paths.values(): init_db(db_path)
    scan_roots = get_drives_connected()
    logging.info(f"전체 스캔을 시작합니다. 대상 드라이브: {scan_roots}")
    files_to_insert, dirs_to_insert = [], []
    scan_time = datetime.now().timestamp()
    for scan_root in scan_roots:
        logging.info(f"드라이브 스캔 중: {scan_root}")
        walk_path = f"\\\\?\\{scan_root}" if os.name == 'nt' else scan_root
        try:
            for root, dirs, files in os.walk(walk_path, onerror=_handle_walk_error):
                system_filters = get_system_path_filters()
                excluded_dir_names = [f.replace('%', '').lower() for f in system_filters]
                dirs[:] = [d for d in dirs if d.lower() not in excluded_dir_names]
                for d in dirs:
                    dirs_to_insert.append((os.path.join(root, d), "directory", scan_time))
                for f in files:
                    files_to_insert.append((os.path.join(root, f), "file", scan_time))
        except Exception as e:
            logging.error(f"드라이브 스캔 중 예외 발생: {scan_root} - {e}")

    logging.info(f"총 {len(files_to_insert)}개의 파일과 {len(dirs_to_insert)}개의 디렉토리를 찾았습니다. DB에 저장합니다...")
    with get_db_connection(db_paths["파일"]) as conn:
        conn.execute("DELETE FROM targets")
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert)
        conn.commit()
    with get_db_connection(db_paths["디렉토리"]) as conn:
        conn.execute("DELETE FROM targets")
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", dirs_to_insert)
        conn.commit()
    with get_db_connection(db_paths["모두"]) as conn:
        conn.execute("DELETE FROM targets")
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert + dirs_to_insert)
        conn.commit()
    logging.info("전체 스캔 및 DB 저장이 완료되었습니다.")


# --- 조회 로직 (다중 선택 기능 추가) ---
def get_system_path_filters() -> List[str]:
    return ["%.git%", "%__pycache__%", "%node_modules%", "%.venv%", "%pk_system%", "%System Volume Information%", "%RECYCLE.BIN%", "%$RECYCLE.BIN%", "%Windows%", "%Program Files%", "%Program Files (x86)%", "%ProgramData%", "%Recovery%"]


def _perform_multi_query(db_path: Path, include_system: bool, display_format: str, target_type: str) -> List[str]:
    import logging
    import subprocess
    from pathlib import Path
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    logging.info(f"DB에서 타겟 목록을 조회합니다... (표시 형식: {display_format}, 다중 선택 가능)")
    if not db_path.exists():
        logging.error(f"DB 파일이 존재하지 않습니다: {db_path}. 먼저 스캔을 실행해주세요.")
        return []

    VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpg', '.mpeg')

    query = "SELECT path FROM targets"
    params = []
    where_clauses = []

    if not include_system:
        filters = get_system_path_filters()
        where_clauses.append("(" + " AND ".join(["path NOT LIKE ?"] * len(filters)) + ")")
        params.extend(filters)

    if target_type == "영상만":
        video_clauses = [f"path LIKE '%{ext}'" for ext in VIDEO_EXTENSIONS]
        where_clauses.append("(" + " OR ".join(video_clauses) + ")")

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY path ASC"

    try:
        fzf_cmd = [
            "fzf",
            "--multi",  # 다중 선택 활성화
            "--layout", "reverse",
            "--info", "inline",
            "--prompt", "검색어(다중선택: TAB)=",
            "--header", "실시간 검색 (여러 개 선택 후 Enter)",
            "--color=prompt:#ffffff,pointer:#4da6ff,hl:#3399ff,hl+:#3399ff,fg+:#3399ff",
        ]

        if display_format == "타겟명만":
            fzf_cmd.extend(["--delimiter", "\t", "--with-nth", "1"])

        popen_kwargs = {
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'text': True,
            'encoding': 'utf-8',
            'errors': 'ignore'
        }

        fzf_executable = subprocess.list2cmdline(fzf_cmd) if is_os_windows() else fzf_cmd
        if is_os_windows(): popen_kwargs['shell'] = True

        with get_db_connection(db_path) as conn, subprocess.Popen(fzf_executable, **popen_kwargs) as fzf_proc:
            cursor = conn.cursor()
            for row in cursor.execute(query, params):
                try:
                    path_str = row[0]
                    display_and_search_str = f"{Path(path_str).name}\t{path_str}" if display_format == "타겟명만" else path_str
                    fzf_proc.stdin.write(display_and_search_str + "\n")
                except (IOError, BrokenPipeError):
                    break
            if fzf_proc.stdin:
                fzf_proc.stdin.close()

            stdout_data, stderr_data = fzf_proc.communicate()

            if fzf_proc.returncode == 0 and stdout_data:
                selected_lines = stdout_data.strip().split('\n')
                if display_format == "타겟명만":
                    return [line.split("\t")[-1] for line in selected_lines if "\t" in line]
                return selected_lines
            elif fzf_proc.returncode != 130:  # 130 is Ctrl+C, not an error
                logging.error(f"fzf exited with error code {fzf_proc.returncode}. Stderr: {stderr_data.strip()}")
            return []

    except FileNotFoundError:
        logging.error("fzf가 설치되어 있지 않거나 PATH에 없습니다. fzf를 설치해주세요.")
        return []
    except Exception as e:
        logging.error(f"fzf 실행 중 오류 발생: {e}")
        return []


def ensure_targets_found(operation_option=None) -> List[str]:
    import logging
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    logging.info("--- 대화형 다중 타겟 검색 도구 시작 ---")
    try:
        options = ["조회", "스캔"]
        if QC_MODE: options.append("디버그")

        if operation_option is None:
            operation_option = ensure_value_completed_2025_10_12_0000("work options", options)

        if operation_option == "스캔":
            ensure_target_file_system_scanned()
            return []

        elif operation_option == "조회":
            if QC_MODE:
                target_type = ensure_value_completed_2025_10_12_0000("조회할 타겟 타입을 선택하세요:", ["파일", "디렉토리", "모두", "영상만"])
                filter_choice = "제외"
                # display_format = "경로포함"
                display_format = "타겟명만"
            else:
                target_type = ensure_value_completed_2025_10_12_0000("조회할 타겟 타입을 선택하세요:", ["파일", "디렉토리", "모두", "영상만"]) or "파일"
                filter_choice = ensure_value_completed_2025_10_12_0000("시스템 타겟을 포함할까요?", ["포함", "제외"]) or "제외"
                display_format = ensure_value_completed_2025_10_12_0000("조회 방식을 선택하세요:", ["타겟명만", "경로포함"]) or "경로포함"

            db_type_for_path = "파일" if target_type == "영상만" else target_type
            db_path = get_db_path(db_type_for_path)

            if not db_path.exists():
                logging.info(f"{db_path}가 존재하지 않아, 먼저 파일 시스템 스캔을 시작합니다.")
                ensure_target_file_system_scanned()

            include_system = (filter_choice == "포함")
            selected_items = _perform_multi_query(db_path, include_system, display_format, target_type)
            logging.debug(f'selected_items={selected_items}')
            return selected_items

    except (KeyboardInterrupt, EOFError):
        logging.info("프로그램을 종료합니다.")
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        logging.info("--- 대화형 다중 타겟 검색 도구 종료 ---")
    return []
