from pathlib import Path

from pk_system.pk_sources.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
# _project_root = Path(__file__).resolve().parent.parent.parent
# if str(_project_root) not in sys.path:
#     sys.path.insert(0, str(_project_root))
from pk_system.pk_sources.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_wrapper_started(pk_wrapper_files=None, mode_window_front=False):
    import logging
    import os
    import subprocess
    import time
    import traceback
    from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept
    from pk_system.pk_sources.pk_functions.ensure_value_completed_2025_11_11 import \
        ensure_value_completed_2025_11_11
    from pk_system.pk_sources.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_system.pk_sources.pk_functions.get_cached_files import get_cached_pk_system_wrappers_path
    from pk_system.pk_sources.pk_functions.get_caller_name import get_caller_name
    from pk_system.pk_sources.pk_functions.get_f_historical import get_history_file_path
    from pk_system.pk_sources.pk_functions.get_file_id import get_file_id
    from pk_system.pk_sources.pk_functions.get_fzf_command import get_fzf_command
    from pk_system.pk_sources.pk_functions.get_last_choice_from_history_file import \
        get_last_choice_from_history_file
    from pk_system.pk_sources.pk_functions.get_nx import get_nx
    from pk_system.pk_sources.pk_functions.get_smart_file_selection_fast import \
        get_smart_file_selection_fast
    from pk_system.pk_sources.pk_functions.save_to_history import save_to_history
    from pk_system.pk_sources.pk_objects.pk_fzf import PkFzf
    from pk_system.pk_sources.pk_objects.pk_system_files import F_VENV_PYTHON_EXE
    from pk_system.pk_sources.pk_objects.pk_system_not_organized import pk_
    from source.constants.directory_paths import D_HUVITS_WRAPPERS_PATH, D_JUNG_HOON_PARK_WRAPPERS_PATH

    func_n = get_caller_name()

    step_start = time.time()
    logging.info(f"ensure_pk_system_wrapper_started: 시작")

    if pk_wrapper_files is None:
        t1 = time.time()
        wrapper_paths = [D_HUVITS_WRAPPERS_PATH, D_JUNG_HOON_PARK_WRAPPERS_PATH]
        wrapper_path = ensure_value_completed_2025_11_11(
            key_name="wrapper_path",
            func_n=func_n,
            guide_text="실행할 래퍼의 종류를 선택해주세요:",
            options=[str(p) for p in wrapper_paths]
        )
        pk_wrapper_files = get_cached_pk_system_wrappers_path(wrapper_path)
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
            # 1단계: 디렉토리명만 표시하기 위해 파일 경로에서 디렉토리명 추출
            # 디렉토리별로 파일들을 그룹화
            dir_to_files_map = {}
            dir_names_for_fzf = []

            for pk_file in pk_wrapper_files:
                pk_file_path = Path(pk_file)
                # 부모 디렉토리명 추출 (예: "Huvitz", "Jung_Hoon_Park")
                dir_name = pk_file_path.parent.name
                if dir_name not in dir_to_files_map:
                    dir_to_files_map[dir_name] = []
                    dir_names_for_fzf.append(dir_name)
                dir_to_files_map[dir_name].append(pk_file)

            # 중복 제거 (순서 유지)
            unique_dir_names = list(dict.fromkeys(dir_names_for_fzf))

            # last_choice도 디렉토리명으로 변환
            last_choice_dir = None
            last_choice_file = None
            if last_choice:
                try:
                    last_choice_path = Path(last_choice)
                    if last_choice_path.exists():
                        last_choice_dir = last_choice_path.parent.name
                        last_choice_file = get_nx(last_choice_path).removeprefix(pk_)
                except:
                    pass

            # 1단계: 디렉토리 선택
            processor = PkFzf(fzf_cmd=fzf_cmd, files=unique_dir_names, last_choice=last_choice_dir)
            returncode, selected_dir_name, err = processor.run_ultra_fast_fzf()

            if returncode == 0 and selected_dir_name:
                logging.debug(f"selected_dir_name='{selected_dir_name}'")

                # 선택된 디렉토리의 파일들 가져오기
                files_in_dir = dir_to_files_map.get(selected_dir_name, [])

                if len(files_in_dir) == 1:
                    # 파일이 하나만 있으면 바로 선택
                    file_to_execute = files_in_dir[0]
                    logging.debug(f"single file in directory: {file_to_execute}")
                elif len(files_in_dir) > 1:
                    # 파일이 여러 개면 2단계: 파일 선택
                    file_names_for_fzf = []
                    for f in files_in_dir:
                        file_name = get_nx(f).removeprefix(pk_)
                        file_names_for_fzf.append(file_name)

                    processor2 = PkFzf(fzf_cmd=fzf_cmd, files=file_names_for_fzf, last_choice=last_choice_file)
                    returncode2, selected_file_name, err2 = processor2.run_ultra_fast_fzf()

                    if returncode2 == 0 and selected_file_name:
                        logging.debug(f"selected_file_name='{selected_file_name}'")
                        # 선택된 파일명으로 파일 찾기
                        for f in files_in_dir:
                            file_name = get_nx(f).removeprefix(pk_)
                            if file_name == selected_file_name or file_name.removeprefix(pk_) == selected_file_name.removeprefix(pk_):
                                file_to_execute = f
                                logging.debug(f"matched: {selected_file_name} -> {file_to_execute}")
                                break
                        if not file_to_execute:
                            logging.debug(f"not matched: {selected_file_name}")
                            file_to_execute = None
                    elif returncode2 == 130:  # Ctrl+C
                        logging.info(f"사용자가 Ctrl+C로 취소했습니다.")
                        file_to_execute = None
                    elif returncode2 != 0:
                        logging.debug(f"fzf 오류 (code {returncode2}): {err2}")
                        file_to_execute = None
                    else:
                        logging.info(f"사용자가 파일 선택을 취소했습니다.")
                        file_to_execute = None
                else:
                    logging.debug(f"선택된 디렉토리에 파일이 없습니다: {selected_dir_name}")
                    file_to_execute = None
            elif returncode == 130:  # Ctrl+C
                logging.info(f"사용자가 Ctrl+C로 취소했습니다.")
                file_to_execute = None
            elif returncode != 0:
                logging.debug(f"fzf 오류 (code {returncode}): {err}")
                file_to_execute = None
            else:
                logging.info(f"사용자가 디렉토리 선택을 취소했습니다.")
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
