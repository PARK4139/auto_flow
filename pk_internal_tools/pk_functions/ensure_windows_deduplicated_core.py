from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_windows_deduplicated_core(len_before=None, previous_windows_opened_list=None):
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
    import logging
    from pk_internal_tools.pk_functions.ensure_windows_closed import ensure_windows_closed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
    from pk_internal_tools.pk_functions.ensure_func_info_loaded import ensure_func_info_loaded

    if previous_windows_opened_list is None:
        previous_windows_opened_list = get_windows_opened_with_hwnd()

    if len_before is None:
        len_before: int = 0

    # 윈도우 중복 제거
    current_windows_opened_list = get_windows_opened_with_hwnd()
    len_current = len(current_windows_opened_list)

    if len_before != len_current:
        logging.debug(f'''len_before={len_before}  ''')
        logging.debug(f'''len_current={len_current}  ''')
        ensure_iterable_data_printed(iterable_data=current_windows_opened_list,
                                        iterable_data_n="current_windows_opened_list")
        len_before = len_current

    if len(current_windows_opened_list) != len(previous_windows_opened_list):
        # 창 중복 제거를 위한 기본 창 제목들
        windows_to_close = ["explorer.exe", "cmd.exe", "powershell.exe"]
        for window_title in windows_to_close:
            ensure_windows_closed(window_title)

        title = ensure_func_info_loaded(func_n="ensure_windows_closed")["title"]
        ensure_window_to_front(title)
        previous_windows_opened_list = current_windows_opened_list

    # ensure_slept(seconds=1)
    # ensure_console_cleared()
