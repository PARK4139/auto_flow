from pk_system_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_wrapper_started(pk_wrapper_files=None, mode_window_front=False):
    import logging
    import os
    import subprocess
    import time
    import traceback

    from source.constants.project_paths import D_WRAPPERS
    from pk_system_functions.ensure_debug_loged_verbose import \
        ensure_debug_loged_verbose
    from pk_system_functions.ensure_slept import ensure_slept
    from pk_system_functions.ensure_window_to_front_2024 import \
        ensure_window_to_front
    from pk_system_functions.get_cached_files import \
        get_cached_pk_system_wrappers_path
    from pk_system_functions.get_caller_n import get_caller_name
    from pk_system_functions.get_f_historical import get_history_file_path
    from pk_system_functions.get_file_id import get_file_id
    from pk_system_functions.get_fzf_command import get_fzf_command
    from pk_system_functions.get_last_choice_from_history_file import \
        get_last_choice_from_history_file
    from pk_system_functions.get_nx import get_nx
    from pk_system_functions.get_smart_file_selection_fast import \
        get_smart_file_selection_fast
    from pk_system_functions.save_to_history import save_to_history
    from pk_system_objects.pk_fzf_processor import PkFzfProcessor
    from pk_system_objects.pk_system_files import F_VENV_PYTHON_EXE
    from pk_system_objects.pk_system_not_organized import pk_

    func_n = get_caller_name()

    step_start = time.time()
    logging.info(f"ensure_pk_system_wrapper_started: 시작")

    if pk_wrapper_files is None:
        t1 = time.time()
        pk_wrapper_files = get_cached_pk_system_wrappers_path(D_WRAPPERS)
        logging.debug(f"get_cached_pk_system_wrappers_path 실행 시간: {time.time() - t1:.3f}초")
        # pk_files = get_pnxs_from_d_working(D_PK_SYSTEM_WRAPPERS)

    if not pk_wrapper_files:
        logging.info(f"실행 가능한 래퍼 파일이 없습니다.")
        return False
    logging.info(f"{len(pk_wrapper_files)}개의 파일을 발견했습니다.")

    #  히스토리 처리
    t2 = time.time()
    key_name = "last_choice"
    history_file = get_history_file_path(file_id=get_file_id(key_name, func_n))
    last_choice = get_last_choice_from_history_file(history_file)
    logging.debug(f'last_choice={last_choice}')
    logging.debug(f"히스토리 처리 시간: {time.time() - t2:.3f}초")

    #  초고속 fzf 실행
    t3 = time.time()
    file_to_execute = None
    fzf_cmd = get_fzf_command()

    if fzf_cmd and os.path.exists(fzf_cmd):
        try:
            last_choice = get_nx(last_choice).removeprefix(pk_)
            processor = PkFzfProcessor(fzf_cmd=fzf_cmd, files=pk_wrapper_files, last_choice=last_choice)
            returncode, selected_name, err = processor.run_ultra_fast_fzf()

            if returncode == 0 and selected_name:
                logging.debug(f"selected_name='{selected_name}'")
                for pk_file in pk_wrapper_files:
                    prefix = pk_
                    if get_nx(pk_file).removeprefix(prefix) == selected_name.removeprefix(prefix):
                        file_to_execute = pk_file
                if file_to_execute:
                    logging.debug(f"matched: {selected_name}")
                else:
                    logging.debug(f"not matched: {selected_name}")
                    file_to_execute = None
            elif returncode == 130:  # Ctrl+C
                logging.info(f"사용자가 Ctrl+C로 취소했습니다.")
                file_to_execute = None
            elif returncode != 0:
                logging.debug(f"fzf 오류 (code {returncode}): {err}")
                file_to_execute = None
            else:
                logging.info(f"사용자가 선택을 취소했습니다.")
                file_to_execute = None

        except Exception as e:
            ensure_debug_loged_verbose(traceback)
            logging.debug(f"fallback as normal complete mode")
            file_to_execute = get_smart_file_selection_fast(pk_wrapper_files, last_choice)
    else:
        logging.debug(f"fzf를 찾을 수 없습니다")
        return False

    logging.debug(f"fzf 처리 시간: {time.time() - t3:.3f}초")

    if not file_to_execute:
        logging.info("선택된 파일이 없으므로 종료합니다.")
        return False

    last_choice_to_save = file_to_execute
    logging.debug(f'last_choice_to_save={last_choice_to_save}')
    if last_choice_to_save:
        if not os.path.exists(last_choice_to_save):
            logging.debug(f"파일이 존재하지 않습니다: {last_choice_to_save}")
            return False
        else:
            save_to_history(contents_to_save=str(last_choice_to_save), history_file=history_file)

    #  성능 최적화 실행
    file_to_execute = os.path.normpath(file_to_execute)
    filename_to_display = get_nx(file_to_execute)
    if filename_to_display.startswith(pk_):
        filename_to_display = filename_to_display.removeprefix(pk_)
    os_name = os.name
    logging.info(f'os_name={os_name}')
    logging.info(f"실행 중: {filename_to_display}")
    if os_name == 'nt':  # Windows
        # cmd = f'start "" cmd.exe /k "python "{file_to_execute}""'
        cmd = f'start "" {F_VENV_PYTHON_EXE} "{file_to_execute}"'
    elif os_name == 'posix':  # Linux/WSL
        cmd = f'python3 "{file_to_execute}"'
    else:
        cmd = f'python "{file_to_execute}"'
    logging.info(f'cmd={cmd}')

    #  비동기 실행으로 UI 블로킹 방지
    # subprocess.Popen(cmd, shell=True)
    # ensure_python_file_executed_advanced(file_path = file_to_execute)
    # cmd = rf'start "" cmd /D /K "{F_VENV_PYTHON_EXE} "{file_to_execute}"'
    # cmd = rf'start "" "{F_VENV_PYTHON_EXE}" "{file_to_execute}"'
    # cmd = rf'"{F_VENV_PYTHON_EXE}" "{file_to_execute}"'
    # ensure_command_executed(cmd, mode='a')
    subprocess.Popen([F_VENV_PYTHON_EXE, file_to_execute], creationflags=subprocess.CREATE_NEW_CONSOLE)
    logging.debug(f"pk system wrapper 실행 완료")

    #  실행 후 대기 (최소화)
    # ensure_slept(milliseconds=200)  # 500ms → 200ms로 단축 # pk_checkpoint
    ensure_slept(milliseconds=10)

    #  윈도우 포커스
    if mode_window_front:
        ensure_window_to_front(rf"{file_to_execute}")

    #  전체 실행 시간 측정
    total_time = time.time() - step_start
    logging.debug(f"총 실행 시간: {total_time:.3f}초")
