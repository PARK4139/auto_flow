# @ensure_seconds_measured
def is_window_opened(window_title_seg):
    from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
    import logging
    windows = get_windows_opened()
    for window in windows:
        if window_title_seg in window:
            logging.debug(f'''"{window_title_seg}" window is opened''')
            return True
    logging.debug(f'''"{window_title_seg}" window is not opened''')
    return False
