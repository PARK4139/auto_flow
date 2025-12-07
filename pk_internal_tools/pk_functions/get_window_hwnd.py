import traceback

from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_window_hwnd(title):
    try:
        import win32gui
        hwnd = win32gui.FindWindow(None, title)
        return hwnd
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
