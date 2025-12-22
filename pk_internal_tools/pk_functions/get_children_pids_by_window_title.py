from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_children_pids_by_window_title(window_title, recursive: bool = True):
    from ctypes import windll, wintypes, byref
    import psutil
    import logging

    import pygetwindow as gw
    pids = []
    wins = gw.getWindowsWithTitle(window_title)
    children = []
    if wins:
        hwnd = wins[0]._hWnd
        # HWND → PID
        pid = wintypes.DWORD()
        windll.user32.GetWindowThreadProcessId(wintypes.HWND(hwnd), byref(pid))
        pid_val = pid.value

        if not pid_val:
            logging.warning("HWND %s → PID를 찾지 못했습니다.", hwnd)

        try:
            parent = psutil.Process(pid_val)
        except psutil.NoSuchProcess:
            logging.info("PID %s 프로세스가 이미 종료됨", pid_val)

        try:
            children = parent.children(recursive=recursive)

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.error("PID %s child 조회 실패: %s", pid_val, e)

    for c in children:
        logging.debug("child PID:", c.pid, "이름:", c.nick_name(), "cmdline:", c.cmdline())
        pids.append(c.pid)

    return pids
