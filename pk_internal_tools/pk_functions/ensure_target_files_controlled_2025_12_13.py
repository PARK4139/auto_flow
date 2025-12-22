"""
대화형 다중 타겟 검색 및 스캔 도구
- 다중 선택: fzf의 `--multi` 옵션을 사용하여 여러 파일/디렉토리를 한 번에 선택.
- 스캔: 연결된 모든 드라이브를 스캔하여 파일/디렉토리/모두 DB 3종에 동시 저장.
    - DB 데이터 일관성: 스캔 시 기존 DB 데이터를 모두 삭제하고 현재 파일 시스템의 데이터만 저장하여 DB의 데이터 일관성을 보장합니다.
    - 시스템 디렉토리 제외: 스캔 시 '$RECYCLE.BIN'과 같은 시스템 관련 디렉토리를 제외하여 불필요한 스캔을 방지하고 성능을 향상시킵니다.
- 조회: DB 조회 시 SQL 필터링을 적용하고, fzf에 직접 파이핑하여 효율성 증대.
- 조회 옵션: 타겟명만 보거나, 전체 경로를 포함해서 볼 수 있는 옵션 추가.
- 스캔 안정성: 스캔 시작 전 기존 DB를 자동으로 백업.
"""



import logging
import subprocess
import traceback
from pathlib import Path
from typing import List

from pk_internal_tools.pk_functions._pk_target_db_utils import (
    get_db_path, get_sqlite3_connection, ensure_target_file_system_scanned,
    get_windows_os_system_path_sql_like_patterns
)
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
from pk_internal_tools.pk_functions.get_fzf_executable_command import get_fzf_executable_command
from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_history_file
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE_HALF, PK_UNDERLINE_SHORT, PK_BLANK
from pk_internal_tools.pk_objects.pk_file_extensions import PK_FILE_EXTENSIONS




def _perform_fzf_query(db_path: Path, include_system: bool, display_format: str, target_type: str, multi_select: bool = True) -> List[str]:
    func_n = get_caller_name()

    # --- Search Query History Integration ---
    search_history_file_id = f"search_queries_{func_n}"
    f_search_history = get_history_file_path(file_id=search_history_file_id)

    # Load existing search history
    existing_search_queries = get_values_from_history_file(f_search_history)

    texts_to_search = []  # 검색어 리스트
    # if not QC_MODE: # QC_MODE에서는 프롬프트 생략
    #    text_to_search = ensure_value_completed(
    #        key_name="검색할 키워드를 입력하세요 (공백으로 구분하여 여러 개 입력 가능)",
    #        func_n=func_n,
    #        options=[""] + existing_search_queries, # 기존 검색어 포함
    #        is_path=False, # 경로가 아님을 명시
    #        allow_empty=True # 빈 값 허용
    #    )
    #    if text_to_search:
    #        text_list_to_search = text_to_search.split()
    #        # Save new search query to history
    #        if text_to_search not in existing_search_queries:
    #            with open(f_search_history, 'a', encoding='utf-8') as f:
    #                f.write(text_to_search + '\n')

    query = "SELECT path FROM targets"
    params = []
    where_clauses = []

    if not include_system:
        filters = get_windows_os_system_path_sql_like_patterns()
        where_clauses.append("(" + " AND ".join(["path NOT LIKE ?"] * len(filters)) + ")")
        params.extend(filters)

    if target_type == "영상파일":
        video_clauses = [f"path LIKE '%{ext}'" for ext in PK_FILE_EXTENSIONS['videos']]
        where_clauses.append("(" + " OR ".join(video_clauses) + ")")

    # Add search query filter(s)
    if texts_to_search:
        search_clauses = []
        for search_term in texts_to_search:
            if search_term.strip():
                search_clauses.append("path LIKE ?")
                params.append(f"%{search_term.strip()}%")
        if search_clauses:
            where_clauses.append("(" + " OR ".join(search_clauses) + ")")

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY path ASC"

    try:
        from pk_internal_tools.pk_functions.get_pk_fzf_options import get_pk_fzf_options

        # get_pk_fzf_options를 통해 기본 fzf 옵션 가져오기
        fzf_cmd = get_pk_fzf_options(prompt_text=f"SEARCH TEXT={PK_BLANK}")

        # _perform_fzf_query의 특정 옵션들로 오버라이드 또는 추가
        # `--no-multi` 옵션이 이미 기본으로 설정되어 있으므로, multi_select가 True일 때만 `--multi`를 추가
        if multi_select and "--no-multi" in fzf_cmd:
            fzf_cmd.remove("--no-multi")
            fzf_cmd.append("--multi")
        elif not multi_select and "--multi" in fzf_cmd:  # 실수로 multi가 붙어있을 경우 제거
            fzf_cmd.remove("--multi")

        # --prompt, --header, --color는 get_pk_fzf_options에서 이미 설정되어 있으므로 필요시만 변경
        # 여기서는 get_pk_fzf_options에서 설정된 값을 사용합니다.

        # display_format에 따른 옵션 추가
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

        if is_os_windows():
            # `get_fzf_executable_command()` 대신 "fzf"를 직접 사용하거나, 
            # get_pk_fzf_options에서 전체 fzf 명령어를 반환하도록 수정해야 할 수 있습니다.
            # 여기서는 get_pk_fzf_options가 순수 옵션 리스트를 반환한다고 가정하고,
            # 실행 가능한 fzf 명령은 별도로 구성합니다.
            fzf_executable = get_fzf_executable_command()
            fzf_full_cmd = [fzf_executable] + fzf_cmd
            fzf_executable_command = subprocess.list2cmdline(fzf_full_cmd)
            popen_kwargs['shell'] = True
        else:
            fzf_executable = get_fzf_executable_command()
            fzf_executable_command = [fzf_executable] + fzf_cmd

        with get_sqlite3_connection(db_path) as conn, subprocess.Popen(fzf_executable_command, **popen_kwargs) as fzf_proc:
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
            elif fzf_proc.returncode != 130:
                logging.error(f"fzf exited with error code {fzf_proc.returncode}. Stderr: {stderr_data.strip()}")
            return []

    except FileNotFoundError:
        logging.error("fzf가 설치되어 있지 않거나 PATH에 없습니다. fzf를 설치해주세요.")
        return []
    except Exception as e:
        logging.error(f"fzf 실행 중 오류 발생: {e}")
        return []


def ensure_target_files_controlled_2025_12_13(operation_option=None, multi_select_mode=False) -> List[str]:
    import logging
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    logging.info(f"{PK_UNDERLINE_SHORT} 대화형 타겟 검색 도구 시작 {PK_UNDERLINE_HALF}")
    func_n = get_caller_name()
    selected_items = []

    try:
        options = ["조회", "스캔"]
        if QC_MODE:
            options.append("디버그")

        if operation_option is None:
            if QC_MODE:
                operation_option = '조회'
            else:
                operation_option = ensure_value_completed(
                    key_name="작업 옵션",
                    options=options,
                    func_n=func_n,
                )
        if operation_option == "스캔":
            ensure_target_file_system_scanned()
            return []

        elif operation_option == "조회":
            target_type_options = ["파일", "디렉토리", "영상파일", "모두"]
            if QC_MODE:
                # target_type = "파일"
                target_type = ensure_value_completed(
                    key_name="조회할 타겟 타입을 선택하세요",
                    func_n=func_n,
                    options=target_type_options
                ) or "파일"
                filter_choice = "제외"
                display_format = "경로포함"
            else:
                target_type = ensure_value_completed(
                    key_name="조회할 타겟 타입을 선택하세요",
                    func_n=func_n,
                    options=target_type_options
                ) or "파일"
                filter_choice = ensure_value_completed(
                    key_name="시스템 타겟을 포함할까요",
                    func_n=func_n,
                    options=["포함", "제외"]
                ) or "제외"
                display_format = ensure_value_completed(
                    key_name="조회 방식을 선택하세요:",
                    func_n=func_n,
                    options=["타겟명만", "경로포함"]
                ) or "경로포함"

            # Determine multi_select behavior
            # If multi_select_mode is explicitly set to True, use it.
            # Otherwise, prompt the user for multi-select.
            if multi_select_mode:
                multi_select = True
            elif not QC_MODE:
                multi_select_str = ensure_value_completed(
                    key_name="다중 선택을 할까요?",
                    func_n=func_n,
                    options=["예", "아니오"]
                ) or "아니오"
                multi_select = (multi_select_str == "예")
            else:  # QC_MODE, and multi_select_mode is False, default to single-select
                multi_select = False

            db_type_for_path = "파일" if target_type == "영상파일" else target_type
            db_path = get_db_path(db_type_for_path)

            if not db_path.exists():
                logging.info(f"{db_path}가 존재하지 않아, 먼저 파일 시스템 스캔을 시작합니다.")
                ensure_target_file_system_scanned()

            include_system = (filter_choice == "포함")
            selected_items = _perform_fzf_query(db_path, include_system, display_format, target_type, multi_select)
            logging.debug(f'선택된 항목: {selected_items}')
            return selected_items
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        logging.info(f"{PK_UNDERLINE_SHORT} 대화형 타겟 검색 도구 종료 {PK_UNDERLINE_HALF}")

    return selected_items
