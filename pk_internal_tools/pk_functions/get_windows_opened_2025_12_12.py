# @ensure_seconds_measured


import ctypes
from ctypes import wintypes
from typing import List, Tuple, Union, Optional

# --- Globals for lazy init ---
_user32 = None
_EnumWindows = None
_IsWindow = None
_IsWindowVisible = None
_GetWindow = None
_GetWindowLongW = None
_GetWindowTextLengthW = None
_GetWindowTextW = None
_WNDENUMPROC = None
_initialized = False

# --- Win32 constants ---
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
GW_OWNER = 4

TitleList = List[str]
HwndTitleList = List[Tuple[int, str]]


def _lazy_init() -> None:
    """Bind Win32 APIs exactly once (lazy)."""
    global _initialized, _user32, _EnumWindows, _IsWindow, _IsWindowVisible
    global _GetWindow, _GetWindowLongW, _GetWindowTextLengthW, _GetWindowTextW, _WNDENUMPROC

    if _initialized:
        return

    _user32 = ctypes.windll.user32

    # Define callback type: BOOL CALLBACK EnumWindowsProc(HWND, LPARAM)
    _WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    # Prototypes
    _EnumWindows = _user32.EnumWindows
    _EnumWindows.argtypes = [_WNDENUMPROC, wintypes.LPARAM]
    _EnumWindows.restype = wintypes.BOOL

    _IsWindow = _user32.IsWindow
    _IsWindow.argtypes = [wintypes.HWND]
    _IsWindow.restype = wintypes.BOOL

    _IsWindowVisible = _user32.IsWindowVisible
    _IsWindowVisible.argtypes = [wintypes.HWND]
    _IsWindowVisible.restype = wintypes.BOOL

    _GetWindow = _user32.GetWindow
    _GetWindow.argtypes = [wintypes.HWND, ctypes.c_uint]
    _GetWindow.restype = wintypes.HWND

    _GetWindowLongW = _user32.GetWindowLongW
    _GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    _GetWindowLongW.restype = ctypes.c_long

    _GetWindowTextLengthW = _user32.GetWindowTextLengthW
    _GetWindowTextLengthW.argtypes = [wintypes.HWND]
    _GetWindowTextLengthW.restype = ctypes.c_int

    _GetWindowTextW = _user32.GetWindowTextW
    _GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    _GetWindowTextW.restype = ctypes.c_int

    _initialized = True


def get_windows_opened_2025_12_12(
        include_tool_windows: bool = False,
        include_owned_windows: bool = False,
        return_hwnds: bool = False,
        limit: Optional[int] = 100,  # default top-N
) -> Union[TitleList, HwndTitleList]:
    """
    Fast, single-shot snapshot of visible top-level window titles.

    Args:
        include_tool_windows: include WS_EX_TOOLWINDOW windows if True.
        include_owned_windows: include owned windows (GetWindow(GW_OWNER) != 0) if True.
        return_hwnds: if True, returns list of (hwnd, title); else titles only.
        limit: stop after collecting this many results (early exit). Default 100.

    Returns:
        List[str] or List[Tuple[int, str]]
    """
    _lazy_init()

    results: Union[TitleList, HwndTitleList] = []
    buf_capacity = 256
    text_buf = ctypes.create_unicode_buffer(buf_capacity)

    # Bind locals (micro-optimization)
    _IsWin = _IsWindow
    _IsVis = _IsWindowVisible
    _GetWin = _GetWindow
    _GetWL = _GetWindowLongW
    _GetLen = _GetWindowTextLengthW
    _GetTxt = _GetWindowTextW
    _CBTYPE = _WNDENUMPROC

    _append = results.append
    _limit = limit

    @_CBTYPE
    def _enum_proc(hwnd, lparam):
        nonlocal text_buf, buf_capacity

        # Valid & visible
        if not _IsWin(hwnd) or not _IsVis(hwnd):
            return True

        # Top-level only (skip owned unless requested)
        if not include_owned_windows and _GetWin(hwnd, GW_OWNER):
            return True

        # Skip tool windows unless requested
        if not include_tool_windows:
            exstyle = _GetWL(hwnd, GWL_EXSTYLE)
            if exstyle & WS_EX_TOOLWINDOW:
                return True

        # Length first (fast skip)
        length = _GetLen(hwnd)
        if length <= 0:
            return True

        # Ensure buffer capacity
        needed = length + 1
        if needed > buf_capacity:
            buf_capacity = max(needed, buf_capacity * 2)
            text_buf = ctypes.create_unicode_buffer(buf_capacity)

        # Get text
        copied = _GetTxt(hwnd, text_buf, buf_capacity)
        if copied <= 0:
            return True

        title = text_buf.value
        if not title:
            return True

        if return_hwnds:
            _append((int(hwnd), title))
        else:
            _append(title)

        # Early exit
        if _limit is not None and len(results) >= _limit:
            return False  # stop enumeration

        return True  # continue

    _EnumWindows(_enum_proc, 0)
    return results


# def get_windows_opened_via_falling_way():
#     import win32gui
#     windows = []
#
#     def enum_windows_callback(hwnd, lparam):
#         if win32gui.IsWindowVisible(hwnd):
#             window_title = win32gui.GetWindowText(hwnd)
#             if window_title:
#                 windows.append((window_title))
#
#     win32gui.EnumWindows(enum_windows_callback, None)
#     return windows
