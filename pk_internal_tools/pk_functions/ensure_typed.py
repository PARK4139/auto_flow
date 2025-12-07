def ensure_typed(text: str, interval: float = 0.0):
    """
    한글/이모지 포함 문자열을 안정적으로 타이핑.
    - Windows: SendInput(KEYEVENTF_UNICODE)로 직접 주입
    - macOS/Linux: 클립보드 붙여넣기 (Cmd/CTRL+V)
    """
    import platform
    import time
    import sys

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging

    if text is None:
        logging.debug(f'''text is None ''')
        return

    system = platform.system()

    def paste_via_clipboard(s: str):
        import pyautogui
        try:
            import pyperclip  # pip install pyperclip
        except Exception:
            # pyperclip이 없으면 간단 대안: tkinter 클립보드 사용
            try:
                import tkinter as tk
                r = tk.Tk(); r.withdraw()
                r.clipboard_clear(); r.clipboard_append(s); r.update(); r.destroy()
            except Exception:
                raise RuntimeError("클립보드 설정 실패: pyperclip 설치 권장")
        else:
            pyperclip.copy(s)

        if system == "Darwin":
            pyautogui.hotkey('command', 'v')
        else:
            pyautogui.hotkey('ctrl', 'v')

    if system == "Windows":
        # n. Windows: SendInput(KEYEVENTF_UNICODE)
        import ctypes
        import pyautogui

        user32 = ctypes.WinDLL('user32', use_last_error=True)

        # INPUT 구조체들 정의
        PUL = ctypes.POINTER(ctypes.c_ulong)

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = (("wVk", ctypes.c_ushort),
                        ("wScan", ctypes.c_ushort),
                        ("dwFlags", ctypes.c_uint),
                        ("time", ctypes.c_uint),
                        ("dwExtraInfo", PUL))

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = (("dx", ctypes.c_long),
                        ("dy", ctypes.c_long),
                        ("mouseData", ctypes.c_uint),
                        ("dwFlags", ctypes.c_uint),
                        ("time", ctypes.c_uint),
                        ("dwExtraInfo", PUL))

        class HARDWAREINPUT(ctypes.Structure):
            _fields_ = (("uMsg", ctypes.c_uint),
                        ("wParamL", ctypes.c_short),
                        ("wParamH", ctypes.c_ushort))

        class INPUT(ctypes.Structure):
            class _I(ctypes.Union):
                _fields_ = (("ki", KEYBDINPUT),
                            ("mi", MOUSEINPUT),
                            ("hi", HARDWAREINPUT))
            _anonymous_ = ("i",)
            _fields_ = (("type", ctypes.c_uint), ("i", _I))

        INPUT_KEYBOARD = 1
        KEYEVENTF_KEYUP = 0x0002
        KEYEVENTF_UNICODE = 0x0004

        def send_unicode_char(ch: str):
            code = ord(ch)
            # key down
            inp_down = INPUT(type=INPUT_KEYBOARD)
            inp_down.ki = KEYBDINPUT(0, code, KEYEVENTF_UNICODE, 0, None)
            # key up
            inp_up = INPUT(type=INPUT_KEYBOARD)
            inp_up.ki = KEYBDINPUT(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, None)

            n = user32.SendInput(2, ctypes.byref((INPUT * 2)(inp_down, inp_up)), ctypes.sizeof(INPUT))
            if n != 2:
                raise ctypes.WinError(ctypes.get_last_error())

        # 제어문자는 SendInput로도 잘 찍히지만, 엔터/탭 등은 명시적으로 보내면 더 안정적
        control_map = {
            '\n': lambda: pyautogui.press('enter'),
            '\r': lambda: None,  # 무시 (Windows 대부분은 \n으로 충분)
            '\t': lambda: pyautogui.press('tab'),
        }

        for ch in text:
            if ch in control_map:
                control_map[ch]()
            else:
                send_unicode_char(ch)
            if interval:
                time.sleep(interval)

        logging.debug(rf'''Typed: "{text}"  ''')
        return

    else:
        # 2) macOS/Linux: 클립보드 붙여넣기
        paste_via_clipboard(text)
        import logging
        logging.debug(rf'''Typed (paste): "{text}"  ''')
        return

# def ensure_typed_v2(text: str, interval: float = 0.1):
#     '''한글 타이필이 안됨 '''
#     from pk_internal_tools.pk_functions.switch_to_keyboard_mode_to_english_at_windows import switch_to_keyboard_mode_to_english_at_windows
#     import pyautogui
#     import platform
#     """
#     Types given text with optional IME switching on Windows.
#     """
#     from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
#     import logging
#
#     if text is None:
#         logging.debug(f'''text is None ''')
#
#         return
#     system = platform.system()
#
#     if system == "Windows":
#         switch_to_keyboard_mode_to_english_at_windows()
#     elif system in ("Linux", "Darwin"):
#         print("[info] IME switching is not supported on this OS. Please ensure input is in English.")
#     else:
#         print(f"[info] Unknown OS: {system}. IME switching skipped.")
#
#     pyautogui.write(text, interval=interval)
#     logging.debug(rf'''Typed: "{text}"  ''')



