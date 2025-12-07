def ensure_process_deduplicated(window_title_seg: str, exact=True):
    import win32gui
    import logging
    from pk_internal_tools.pk_functions.get_window_title import get_window_title
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import win32con

    try:
        window_title = get_window_title(window_title_seg=window_title_seg)
        if not window_title:
            return

        if QC_MODE:
            logging.debug(f"[DEBUG] window_title={window_title} ")

        hwnds = []

        def enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if (exact and title == window_title) or (not exact and window_title in title):
                    hwnds.append(hwnd)

        win32gui.EnumWindows(enum_handler, None)

        if not hwnds:
            logging.debug(f"[SKIP] No matching windows for '{window_title}'")
            return

        survivor_hwnd = hwnds[0]
        to_close = hwnds[1:]

        for hwnd in to_close:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            logging.debug(f"[CLOSE] HWND={hwnd} closed for window_title='{win32gui.GetWindowText(hwnd)}'")

        logging.debug(f"[SURVIVED] HWND={survivor_hwnd} kept alive → '{win32gui.GetWindowText(survivor_hwnd)}'")

    except Exception as e:
        logging.warning(f"{e}")
