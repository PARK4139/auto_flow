# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict

from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers

"""
대화형 타겟 검색 및 스캔 도구 (효율성 개선)
- 스캔: 연결된 모든 드라이브를 스캔하여 파일/디렉토리/모두 DB 3종에 동시 저장
    - DB 데이터 일관성: 스캔 시 기존 DB 데이터를 모두 삭제하고 현재 파일 시스템의 데이터만 저장하여 DB의 데이터 일관성을 보장합니다.
    - 시스템 디렉토리 제외: 스캔 시 '$RECYCLE.BIN'과 같은 시스템 관련 디렉토리를 제외하여 불필요한 스캔을 방지하고 성능을 향상시킵니다.
- 조회: DB 조회 시 SQL 필터링을 적용하고, fzf에 직접 파이핑하여 효율성 증대
- 조회 옵션: 타겟명만 보거나, 전체 경로를 포함해서 볼 수 있는 옵션 추가
- 스캔 안정성: 스캔 시작 전 기존 DB를 자동으로 백업
"""


# --- DB 관리 ---
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

def _handle_walk_error(e):  # New error handler for os.walk
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
    from pathlib import Path

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
        # Specific log for user's Downloads folder if it's the C: drive
        if Path(scan_root) == Path('C:\\'):
            user_downloads_path = Path.home() / "Downloads"
            if user_downloads_path.exists():
                logging.info(f"사용자 Downloads 폴더 스캔 시도: {user_downloads_path}")
        
        # Windows의 MAX_PATH(260자) 경로 길이 제한을 우회하기 위해 \\?\ 접두사 추가
        walk_path = scan_root
        if os.name == 'nt':
            walk_path = f"\\\\?\\{scan_root}"

        try:
            for root, dirs, files in os.walk(walk_path, onerror=_handle_walk_error):  # Pass onerror handler
                # Exclude system directories from scanning
                system_filters = get_system_path_filters()
                # Convert filters to actual directory names for direct comparison
                # Remove '%' and convert to lowercase for case-insensitive comparison
                excluded_dir_names = [f.replace('%', '').lower() for f in system_filters]
                dirs[:] = [d for d in dirs if d.lower() not in excluded_dir_names]

                # Add debug logging for Downloads folder content
                if user_downloads_path.exists() and Path(root).is_relative_to(user_downloads_path):
                    logging.debug(f"[DEBUG SCAN] Downloads content in {root}: dirs={len(dirs)}, files={len(files)}")
                    if "박정훈" in root or any("박정훈" in f for f in files):
                        logging.debug(f"[DEBUG SCAN] '박정훈' found in Downloads related path: {root}")

                for d in dirs:
                    dirs_to_insert.append((os.path.join(root, d), "directory", scan_time))
                for f in files:
                    files_to_insert.append((os.path.join(root, f), "file", scan_time))
        except Exception as e:
            logging.error(f"드라이브 스캔 중 예외 발생: {scan_root} - {e}")
    logging.info(f"총 {len(files_to_insert)}개의 파일과 {len(dirs_to_insert)}개의 디렉토리를 찾았습니다. DB에 저장합니다...")
    with get_db_connection(db_paths["파일"]) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM targets")  # 기존 데이터 삭제
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert)
        conn.commit()
    with get_db_connection(db_paths["디렉토리"]) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM targets")  # 기존 데이터 삭제
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", dirs_to_insert)
        conn.commit()
    with get_db_connection(db_paths["모두"]) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM targets")  # 기존 데이터 삭제
        conn.executemany("INSERT OR REPLACE INTO targets VALUES (?, ?, ?)", files_to_insert + dirs_to_insert)
        conn.commit()
    logging.info("전체 스캔 및 DB 저장이 완료되었습니다.")


# --- 조회 & 디버그 로직 ---
def get_system_path_filters() -> List[str]:
    return ["%.git%", "%__pycache__%", "%node_modules%", "%.venv%", "%pk_system%", "%System Volume Information%", "%RECYCLE.BIN%", "%$RECYCLE.BIN%", "%Windows%", "%Program Files%", "%Program Files (x86)%", "%ProgramData%", "%Recovery%"]


def perform_query(db_path: Path, include_system: bool, display_format: str, target_type: str):
    import logging
    import subprocess
    from pathlib import Path

    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows  # Lazy Import

    logging.info(f"DB에서 타겟 목록을 조회합니다... (표시 형식: {display_format})")
    if not db_path.exists():
        logging.error(f"DB 파일이 존재하지 않습니다: {db_path}. 먼저 스캔을 실행해주세요.")
        return

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

    query += " ORDER BY path ASC"  # Added sorting
    try:

        fzf_cmd = [
            "fzf",
            # "--height",
            # "99%",
            "--layout",
            "reverse",
            "--info",
            "inline",
            "--prompt", "검색어=",
            "--header", "실시간 검색",
            "--footer", "Ctrl+O: Open selected item( if path include #. can't open in this way)  ",
            "--color=prompt:#ffffff,pointer:#4da6ff,hl:#3399ff,hl+:#3399ff,fg+:#3399ff",
            # "--preview", "ls -la {}"
            # "--regex",
        ]
        F_PK_ENURE_PNX_STARTED_EXTERNAL_ARGUMENT = d_pk_wrappers / "pk_enure_pnx_started_external_argument.py"
        logging.debug(f"is_os_windows() result: {is_os_windows()}")
        if is_os_windows():
            fzf_cmd.extend([
                # "--bind",
                # rf'ctrl-o:execute(cmd /c {F_UV_PYTHON_EXE} {F_PK_ENURE_PNX_STARTED_EXTERNAL_ARGUMENT} --pnx "{{}}")'
            ])

        if display_format == "타겟명만":
            fzf_cmd.extend(["--delimiter", "\t", "--with-nth", "1"])
        elif display_format == "경로포함":
            fzf_cmd.extend([])
            # fzf_cmd.extend(["--regex"])
        logging.debug(f"Final fzf_cmd: {fzf_cmd}")

        popen_kwargs = {
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'text': True,
            'encoding': 'utf-8',
            'errors': 'ignore'
        }

        if is_os_windows():
            # On Windows, manually join the command list into a string
            # and use shell=True to handle complex arguments correctly.
            command_str = subprocess.list2cmdline(fzf_cmd)
            logging.debug(f"Executing on Windows with shell=True: {command_str}")
            popen_kwargs['shell'] = True
            fzf_executable = command_str
        else:
            # On other OSes, use the list directly (safer)
            logging.debug(f"Executing on non-Windows with shell=False: {fzf_cmd}")
            fzf_executable = fzf_cmd

        with get_db_connection(db_path) as conn, subprocess.Popen(fzf_executable, **popen_kwargs) as fzf_proc:
            cursor = conn.cursor()
            for row in cursor.execute(query, params):
                try:
                    path_str = row[0]
                    if display_format == "타겟명만":
                        display_and_search_str = f"{Path(path_str).name}	{path_str}"

                    else:  # display_format == "경로포함"
                        # Explicitly quote paths with spaces for fzf input
                        if " " in path_str:
                            display_and_search_str = f'"{path_str}"'
                        else:
                            display_and_search_str = path_str
                    fzf_proc.stdin.write(display_and_search_str + "\n")
                except (IOError, BrokenPipeError):
                    break
            if fzf_proc.stdin:
                fzf_proc.stdin.close()
            stdout_data, stderr_data = fzf_proc.communicate()
            logging.debug(f"fzf stdout_data (raw): {stdout_data!r}")
            logging.debug(f"fzf stderr_data (raw): {stderr_data!r}")
            if fzf_proc.returncode == 0:
                selected = stdout_data.strip()
                # If path was quoted, remove quotes
                if display_format == "경로포함" and selected.startswith('"') and selected.endswith('"'):
                    selected = selected[1:-1]
                # "타겟명만" 모드에서 실제로는 전체경로를 돌려주고 싶으면 탭 분리해 마지막 필드 사용
                if display_format == "타겟명만":
                    # 탭이 없으면 전체를 그대로 반환 (안전장치)
                    return selected.split("\t")[-1]
                return selected
            else:
                logging.error(f"fzf exited with error code {fzf_proc.returncode}. Stderr: {stderr_data.strip()}")
                return None
    except FileNotFoundError:
        logging.error("fzf가 설치되어 있지 않거나 PATH에 없습니다. fzf를 설치해주세요.")
        return None
    except Exception as e:
        logging.error(f"fzf 실행 중 오류 발생: {e}")
        return None


def perform_debug_query():
    import os
    import logging
    from pathlib import Path

    """DB 내용을 직접 조회하여 스캔 문제를 진단"""
    db_path = get_db_path("모두")
    logging.info(f"디버그 모드: {db_path} DB 내용 확인 ---")
    if not db_path.exists():
        logging.error("DB 파일이 존재하지 않습니다. 스캔을 먼저 실행해주세요.")
        return

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()

        # n. Downloads 폴더 내용 확인
        logging.info("[1] 'Downloads' 포함 경로 조회 (최대 20개):")
        cursor.execute("SELECT path FROM targets WHERE path LIKE '%Downloads%' LIMIT 20")
        results_downloads = cursor.fetchall()
        if results_downloads:
            for row in results_downloads:
                logging.info(f"{row[0]}")
        else:
            logging.info("-> 'Downloads' 포함 경로를 찾을 수 없습니다.")

        # n. '박정훈' 키워드 내용 확인
        logging.info("[2] '박정훈' 포함 경로 조회 (최대 20개):")
        cursor.execute("SELECT path FROM targets WHERE path LIKE '%박정훈%' LIMIT 20")
        results_keyword = cursor.fetchall()
        if results_keyword:
            for row in results_keyword:
                logging.info(f"{row[0]}")
        else:
            logging.info("-> '박정훈' 포함 경로를 찾을 수 없습니다.\n")

        # n. Downloads 폴더 직접 접근 시도
        downloads_dir = Path.home() / "Downloads"
        logging.info(f"[3] Downloads 폴더 직접 접근 시도: {downloads_dir}")
        if downloads_dir.exists() and downloads_dir.is_dir():
            try:
                contents = os.listdir(downloads_dir)
                logging.info(f" -> 접근 성공. 내용 (처음 5개): {contents[:5]} ... (총 {len(contents)}개)")
            except OSError as e:
                logging.error(f" -> 접근 실패: {e}")
        else:
            logging.info("-> Downloads 폴더가 존재하지 않거나 디렉토리가 아닙니다.")

    logging.info("--- 디버그 모드 종료 ---")


def ensure_target_found(operation_option=None):
    import logging
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    logging.info("--- 대화형 타겟 검색 도구 시작 ---")
    try:
        if QC_MODE:
            if operation_option is None:
                operation_option = ensure_value_completed_2025_10_12_0000("work options", ["조회", "스캔"]) or "조회"
        else:
            operation_option = ensure_value_completed_2025_10_12_0000("work options", ["조회", "스캔"]) or "조회"
        if operation_option == "스캔":
            ensure_target_file_system_scanned()
        elif operation_option == "조회":
            if QC_MODE:
                target_type = "파일"
                filter_choice = "제외"
                display_format = "경로포함"
            else:
                target_type = ensure_value_completed_2025_10_12_0000("조회할 타겟 타입을 선택하세요:", ["파일", "디렉토리", "모두", "영상만"]) or "파일"
                filter_choice = ensure_value_completed_2025_10_12_0000("시스템 타겟을 포함할까요?", ["포함", "제외"]) or "제외"
                display_format = ensure_value_completed_2025_10_12_0000("조회 방식을 선택하세요:", ["타겟명만", "경로포함"]) or "경로포함"
            
            db_type_for_path = "파일" if target_type == "영상만" else target_type
            db_path = get_db_path(db_type_for_path)

            if not db_path.exists():
                ensure_target_file_system_scanned()
            include_system = (filter_choice == "포함")
            selected_item = perform_query(db_path, include_system, display_format, target_type)
            logging.debug(f'selected_item={selected_item}')
            return selected_item
        elif operation_option == "디버그":
            perform_debug_query()

    except (KeyboardInterrupt, EOFError):
        logging.info("프로그램을 종료합니다.")
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        logging.info("--- 대화형 타겟 검색 도구 종료 ---")
