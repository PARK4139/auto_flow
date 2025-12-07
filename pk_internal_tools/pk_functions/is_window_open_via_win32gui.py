def is_window_open_via_win32gui(window_title):
      # pywin32
    def enum_windows_callback(hwnd, lparam):
        if win32gui.IsWindowVisible(hwnd):
            # 창의 제목을 확인
            if window_title in win32gui.GetWindowText(hwnd):
                # logging.debug(f'''{win32gui.GetWindowText(hwnd)}"''')
                lparam.append(hwnd)

    # 열린 창들을 확인
    hwnd_list = []
    win32gui.EnumWindows(enum_windows_callback, hwnd_list)

    # 특정 창이 열려 있는지 확인
    return any(window_title in win32gui.GetWindowText(hwnd) for hwnd in hwnd_list)
