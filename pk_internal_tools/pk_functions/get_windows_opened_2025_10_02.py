import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_windows_opened_2025_10_02():
    try:
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
        import win32gui
        windows = []

        def enum_windows_callback(hwnd, lparam):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if window_title:
                    windows.append((window_title))

        win32gui.EnumWindows(enum_windows_callback, None)
        return windows
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
