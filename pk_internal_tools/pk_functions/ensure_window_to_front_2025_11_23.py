from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_window_to_front_2025_11_23(
        window_title_seg=None, pid=None,
        timeout_ms=500
        # timeout_ms=1000
):
    import win32gui
    import win32con
    import win32api
    import win32process
    import logging
    import time
    import ctypes
    from ctypes import wintypes

    from pk_internal_tools.pk_functions.move_window_to_front_via_pid import move_window_to_front_via_pid
    from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    if window_title_seg is not None:
        window_title_seg = str(window_title_seg)

    logging.debug("window_title_seg=%r", window_title_seg)
    logging.debug("pid=%r", pid)

    GA_ROOT = 2
    DWMWA_CLOAKED = 14
    user32 = ctypes.windll.user32
    dwmapi = ctypes.windll.dwmapi if hasattr(ctypes.windll, 'dwmapi') else None

    def get_window_styles(hwnd):
        GWL_STYLE = -16
        GWL_EXSTYLE = -20
        style = win32api.GetWindowLong(hwnd, GWL_STYLE)
        exstyle = win32api.GetWindowLong(hwnd, GWL_EXSTYLE)
        return style, exstyle

    def is_cloaked(hwnd):
        if not dwmapi:
            return False
        cloaked = wintypes.DWORD()
        hr = dwmapi.DwmGetWindowAttribute(
            wintypes.HWND(hwnd), wintypes.DWORD(DWMWA_CLOAKED),
            ctypes.byref(cloaked), ctypes.sizeof(cloaked)
        )
        return (hr == 0) and (cloaked.value != 0)

    def zorder_windows():
        # 상단부터 열거 (EnumWindows는 대체로 Z-order 상단→하단)
        out = []

        def cb(hwnd, lParam):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    out.append(hwnd)
            except Exception:
                pass
            return True

        win32gui.EnumWindows(cb, 0)
        return out

    def hwnd_title(hwnd):
        try:
            return win32gui.GetWindowText(hwnd) or ""
        except Exception:
            return ""

    def normalize_hwnd(hwnd):
        # 루트 창 → 마지막 활성 팝업(닫히지 않은) 선택
        try:
            root = win32gui.GetAncestor(hwnd, GA_ROOT)
            # GetLastActivePopup은 파이썬 래핑이 없어 ctypes로 호출
            GetLastActivePopup = user32.GetLastActivePopup
            GetLastActivePopup.restype = wintypes.HWND
            last_popup = GetLastActivePopup(root)
            if last_popup and win32gui.IsWindow(last_popup) and win32gui.IsWindowVisible(last_popup):
                return last_popup
            return root
        except Exception:
            return hwnd

    def pick_target_by_title(seg):
        if not seg:
            return None
        seg_lower = seg.lower()
        zw = zorder_windows()
        candidates = []
        for hwnd in zw:
            try:
                if not win32gui.IsWindow(hwnd) or not win32gui.IsWindowVisible(hwnd):
                    continue
                title = hwnd_title(hwnd)
                if not title:
                    continue
                tl = title.lower()
                if seg_lower == tl:
                    score = (3, len(title))
                elif tl.startswith(seg_lower):
                    score = (2, len(title))
                elif seg_lower in tl:
                    score = (1, len(title))
                else:
                    continue
                candidates.append((score, hwnd, title))
            except Exception:
                continue
        if not candidates:
            return None
        # 점수 → Z-order 상단 우선(이미 zw 순서), 길이로 가중치
        candidates.sort(key=lambda x: (-x[0][0], -x[0][1]))
        return candidates[0][1]

    def bring_to_front_core(hwnd):
        attached = False
        try:
            if not hwnd or not win32gui.IsWindow(hwnd):
                return False

            hwnd = normalize_hwnd(hwnd)

            # 필터링: 비활성/최소화/클로킹
            style, ex = get_window_styles(hwnd)
            if style & win32con.WS_DISABLED:
                logging.debug("Target window is disabled; enabling temporarily.")
                try:
                    win32api.EnableWindow(hwnd, True)
                except Exception:
                    pass

            if style & win32con.WS_MINIMIZE:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                ensure_slept(milliseconds=3)

            if not win32gui.IsWindowVisible(hwnd) or is_cloaked(hwnd):
                logging.debug("Target window is not visible or cloaked; trying ShowWindow(SW_SHOW).")
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    ensure_slept(milliseconds=3)
                except Exception:
                    pass

            # 전경권한 힌트(가능하면)
            try:
                user32.AllowSetForegroundWindow(win32con.ASFW_ANY)
            except Exception:
                pass

            # Alt 제스처(간단한 사용자 입력 힌트)
            try:
                win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
                ensure_slept(milliseconds=3)
                win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            except Exception:
                pass

            # 조건부 AttachThreadInput
            fg = win32gui.GetForegroundWindow()
            fg_tid = win32process.GetWindowThreadProcessId(fg)[0] if fg else 0
            tg_tid, _ = win32process.GetWindowThreadProcessId(hwnd)

            if fg_tid and tg_tid and fg_tid != tg_tid:
                try:
                    win32process.AttachThreadInput(fg_tid, tg_tid, True)
                    attached = True
                    logging.debug("AttachThreadInput success.")
                except Exception as e_att:
                    logging.debug(f"AttachThreadInput failed: {e_att}")

            # 포커스 시퀀스: SetForegroundWindow → BringWindowToTop → SetActiveWindow
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception as e1:
                logging.debug(f"SetForegroundWindow threw: {e1}")

            ensure_slept(milliseconds=3)
            try:
                win32gui.BringWindowToTop(hwnd)
            except Exception as e2:
                logging.debug(f"BringWindowToTop threw: {e2}")

            ensure_slept(milliseconds=3)
            try:
                user32.SetActiveWindow(hwnd)
            except Exception:
                # SetActiveWindow는 때로 실패; 무시
                pass

            # TopMost 토글 보강
            try:
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                ensure_slept(milliseconds=3)
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            except Exception as e_tm:
                logging.debug(f"TopMost toggle failed: {e_tm}")

            return True
        finally:
            if attached:
                try:
                    win32process.AttachThreadInput(fg_tid, tg_tid, False)
                except Exception as e_det:
                    logging.debug(f"Detach failed: {e_det}")

    # ---- 본 로직 ----
    start = time.time()
    end_deadline = start + (timeout_ms / 1000.0)
    success = False
    last_hwnd = None

    last_hwnd = pick_target_by_title(window_title_seg)
    if last_hwnd:
        success = bring_to_front_core(last_hwnd) or False
        if success and is_window_title_front(window_title=window_title_seg):
            logging.debug(f"'{window_title_seg}' is now in front (first try).")
            return True

    # 2) 재시도 루프: 재열거/재매칭/보강
    while time.time() < end_deadline:
        # PID 우회(있으면 1회만)
        if pid is not None:
            try:
                move_window_to_front_via_pid(pid)
            except Exception as e_pid:
                logging.debug(f"move_window_to_front_via_pid failed: {e_pid}")

        # 타이틀로 재발견
        last_hwnd = pick_target_by_title(window_title_seg)
        if last_hwnd:
            bring_to_front_core(last_hwnd)

        # 전면 확인
        if is_window_title_front(window_title=window_title_seg):
            success = True
            break

        ensure_slept(milliseconds=3)

    if not success:
        logging.warning(f"'{window_title_seg}' did not come to front within {timeout_ms} ms.")
        return False

    # logging.info(f"'{window_title_seg}' did come to front within {timeout_ms} ms.")
    return True
