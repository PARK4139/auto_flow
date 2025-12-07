def ensure_window_titles_printed():
    import logging
    from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
    for window_opened in get_windows_opened():
        logging.debug(rf'window_opened="{window_opened}"')
