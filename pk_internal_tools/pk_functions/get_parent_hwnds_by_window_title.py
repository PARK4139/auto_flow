from typing import List

import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_parent_hwnds_by_window_title(window_title, exact=True):
    try:
        import pygetwindow as gw
    except ImportError:
        logging.error("pygetwindow 모듈이 필요합니다. pip install pygetwindow")
        return []

    hwnds: List[int] = []

    if exact:
        windows = [w for w in gw.getAllWindows() if w.title == window_title]
    else:
        windows = gw.getWindowsWithTitle(window_title)

    for w in windows:
        hwnd = (
                getattr(w, "_hWnd", None)
                or getattr(w, "hwnd", None)
                or getattr(w, "handle", None)
        )
        if hwnd:
            hwnds.append(int(hwnd))
        else:
            logging.debug(f"HWND를 찾을 수 없는 윈도우: {w}")

    return hwnds
