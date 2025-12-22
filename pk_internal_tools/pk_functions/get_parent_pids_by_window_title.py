from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_parent_pids_by_window_title(window_title: str, exact: bool = True):
    import logging
    from typing import Set

    try:
        import pygetwindow as gw
        import win32process
    except ImportError as e:
        logging.error("pygetwindow / pywin32(win32process) 필요: %s", e)
        return []

    # 대상 윈도우 찾기
    if exact:
        windows = [w for w in gw.getAllWindows() if w.title == window_title]
    else:
        windows = gw.getWindowsWithTitle(window_title)  # 부분 일치

    pids: Set[int] = set()

    for w in windows:
        hwnd = (
                getattr(w, "_hWnd", None) or
                getattr(w, "hwnd", None) or
                getattr(w, "handle", None)
        )
        if hwnd is None:
            logging.debug("HWND를 찾을 수 없음: %r", w)
            continue
        try:
            _, pid = win32process.GetWindowThreadProcessId(int(hwnd))
            if pid:
                pids.add(int(pid))
        except Exception as e:
            logging.debug("윈도우 '%s' PID 조회 실패: %s", getattr(w, "title", "?"), e)

    if not pids:
        logging.debug("해당 제목의 PID 없음: %r (exact=%s)", window_title, exact)

    logging.debug(f'''pids of window_title={pids} of {window_title}''')
    return sorted(pids)
