from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_window_minimized(window_title: str):
    import logging

    import win32con
    import win32gui

    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            current_title = win32gui.GetWindowText(hwnd)
            if window_title.lower() in current_title.lower():
                logging.debug(f"Minimizing window: {current_title}")
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    win32gui.EnumWindows(enum_handler, None)
