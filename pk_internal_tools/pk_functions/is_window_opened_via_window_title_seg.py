_logged_not_opened_windows = set()


# @ensure_seconds_measured
def is_window_opened_via_window_title_seg(window_title_seg, verbose=False):
    from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
    import logging

    if not isinstance(window_title_seg, str):
        logging.error(f"is_window_opened_via_window_title_seg: window_title_seg must be a string, but got {type(window_title_seg).__name__}. Value: {window_title_seg}")
        return False

    windows = get_windows_opened()
    for window in windows:
        if window_title_seg in window:
            logging.debug(f'''"{window_title_seg}" window is opened''')
            # If window is found, reset the "not opened" log status for it.
            if window_title_seg in _logged_not_opened_windows:
                _logged_not_opened_windows.remove(window_title_seg)
            return True

    # If window is not found, log it only once to avoid spam.
    if window_title_seg not in _logged_not_opened_windows:
        logging.debug(f'''"{window_title_seg}" window is not opened''')
        _logged_not_opened_windows.add(window_title_seg)

    return False
