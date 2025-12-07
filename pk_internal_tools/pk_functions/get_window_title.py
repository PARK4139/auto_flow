import logging


def get_window_title(window_title_seg=None):
    import os
    from pk_internal_tools.pk_functions.get_set_from_list import get_set_from_list
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    if window_title_seg is not None:
        window_title_list = get_window_titles()
        window_titles = get_set_from_list(window_title_list)
        for window_title in window_titles:
            if window_title_seg == window_title:
                return window_title
    else:
        import win32gui
        import win32process
        current_pid = os.getpid()
        hwnd_found = None

        def _enum_callback(hwnd, _):
            nonlocal hwnd_found
            # PID 매칭 확인
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == current_pid and win32gui.IsWindowVisible(hwnd):
                hwnd_found = hwnd
                return False  # Stop enumeration
        win32gui.EnumWindows(_enum_callback, None)
        if hwnd_found:
            return win32gui.GetWindowText(hwnd_found)
        return None
