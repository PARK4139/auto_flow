def ensure_routine_file_executed_as_hot_reloader():
    import logging
    import traceback
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_directories import d_pk_internal_tools
    from pk_internal_tools.pk_functions import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_chcp_65001 import ensure_chcp_65001
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_target_files_modified_time_stable import ensure_target_files_modified_time_stable
    from pk_internal_tools.pk_functions.ensure_pk_log_useless_removed import ensure_pk_log_useless_removed
    from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
    from pk_internal_tools.pk_functions.ensure_py_system_process_ran_by_pnx import ensure_py_system_process_ran_by_pnx
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
    from pk_internal_tools.pk_functions.get_set_from_list import get_set_from_list
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
    from pk_internal_tools.pk_objects.pk_etc import PK_USERLESS_LINE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers

    try:

        if get_os_n() == 'windows':
            ensure_chcp_65001()
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        windows_opened = get_set_from_list(get_windows_opened_with_hwnd())

        mode = PkTexts.FILE_GEN_TIME_STABLE_MODE

        key_name = 'directory_to_monitor'
        # directories = get_pnxs(d_working=d_pk_internal_tools, filtered="d")
        # directory_to_monitor = ensure_value_completed_2025_11_11(key_name=key_name, func_n=func_n, options=directories)
        directory_to_monitor = ensure_value_completed_2025_11_11(key_name=key_name, func_n=func_n, options=[str(d_pk_internal_tools)])
        directory_to_monitor = Path(directory_to_monitor)
        logging.debug(f'''directory_to_monitor={directory_to_monitor} ''')

        # key_name = 'file_to_monitor'
        # files = get_pnxs(d_working=D_PK_FUNCTIONS, filtered="f")
        # files += get_pnxs(d_working=d_pk_external_tools, filtered="f")
        # file_to_monitor = ensure_value_completed_2025_11_11(key_name=key_name, func_n=func_n, options=files)
        # file_to_monitor = Path(file_to_monitor)
        # logging.debug(f'''file_to_monitor={file_to_monitor} ''')

        key_name = 'file_to_execute'
        files = get_pnxs(d_working=d_pk_wrappers, filtered="f")
        file_to_execute = ensure_value_completed_2025_11_11(key_name=key_name, func_n=func_n, options=files)
        file_to_execute = Path(file_to_execute)
        logging.debug(f'''file_to_execute={file_to_execute} ''')

        files_to_monitor = [
                               # file_to_monitor,
                           ] + get_pnxs(d_working=directory_to_monitor, filtered="f", with_walking=True)
        files_to_execute = [
            file_to_execute,
        ]
        loop_cnt = 1

        # pk_option
        # key_name = 'stable_seconds_limit'
        # stable_seconds_limit = ensure_value_completed_2025_11_11(key_name=key_name, func_n=func_n, options=[1, 2,3,4,5,6,10])
        # stable_seconds_limit = 2
        stable_seconds_limit = 1

        window_title_to_kill = None
        file_to_execute = None
        if mode == PkTexts.FILE_GEN_TIME_STABLE_MODE:
            while 1:
                # ensure_console_cleared()

                if loop_cnt == 1:
                    ensure_spoken(f"핫리로더 시작...")
                    print(f"핫리로더 시작...")
                    for file_to_execute in files_to_execute:
                        file_to_execute = Path(file_to_execute)
                        logging.debug(f'''f={file_to_execute} ''')
                        windows_opened.add(get_nx(file_to_execute))
                        file_to_execute = file_to_execute
                        window_title_to_kill = get_nx(file_to_execute)  # pk_option
                        ensure_py_system_process_ran_by_pnx(file_to_execute=file_to_execute, mode='a')
                    loop_cnt = loop_cnt + 1
                    continue

                logging.debug(PK_USERLESS_LINE)

                if not ensure_target_files_modified_time_stable(files_to_monitor=files_to_monitor, monitoring_seconds=stable_seconds_limit):
                    ensure_spoken(f"edited 감지")
                    logging.debug(f"핫리로더, {stable_seconds_limit} 초, 중에 not stable 감지")
                    if ensure_target_files_modified_time_stable(files_to_monitor=files_to_monitor, monitoring_seconds=stable_seconds_limit):
                        ensure_spoken(f"edit complete 감지")
                        logging.debug(f"핫리로더, {stable_seconds_limit} 초, 동안 stable 감지")
                        for file_to_execute in files_to_execute:
                            ensure_process_killed(window_title_seg=window_title_to_kill)
                            ensure_slept(milliseconds=77)
                            ensure_py_system_process_ran_by_pnx(file_to_execute=file_to_execute, mode='a')
                            logging.debug(f"리로드 시도완료")
                            ensure_spoken(f"", wait=True)
                else:
                    logging.debug(f"{stable_seconds_limit} 초 동안 stable 감지 완료")

                ensure_slept(milliseconds=77)
                # time.sleep(80)  # 로깅 방지

                # pk_option
                ensure_pk_log_useless_removed(text=PK_USERLESS_LINE)

    except:
        ensure_debug_loged_verbose(traceback)
