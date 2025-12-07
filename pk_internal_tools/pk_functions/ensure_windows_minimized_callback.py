from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_windows_minimized_callback(hwnd, lparam):
    import win32gui
    import win32con  # pywin32
    if win32gui.IsWindowVisible(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  # 창을 최소화
        print(f"창 {win32gui.GetWindowText(hwnd)}를 최소화했습니다.")
