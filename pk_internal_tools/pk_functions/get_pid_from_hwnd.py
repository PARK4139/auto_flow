from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_pid_from_hwnd(hwnd: int) -> int:
    from ctypes import windll, wintypes, byref
    pid = wintypes.DWORD()
    windll.user32.GetWindowThreadProcessId(wintypes.HWND(hwnd), byref(pid))
    return pid.value
