

def switch_to_keyboard_mode_to_english_at_windows():
    import time
    """
    Switch to English input on Windows using win32api and ctypes.
    """
    try:
        import ctypes
        import win32api
        import win32con

        # Get the current thread id and foreground window
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)

        # Get current keyboard layout for the thread
        current_layout = ctypes.windll.user32.GetKeyboardLayout(thread_id)
        lang_id = current_layout & (2 ** 16 - 1)  # low word

        # 0x0409 == English (United States)
        if lang_id != 0x0409:
            # Post message to switch input method
            win32api.PostMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x0409)
            time.sleep(0.2)  # Give time to switch
    except Exception as e:
        print(f"[warn] Failed to switch IME: {e}")


