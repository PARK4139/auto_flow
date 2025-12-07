from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_windows_deduplicated():
    from collections import Counter
    import win32gui
    import win32con

    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
    windows = get_windows_opened_with_hwnd()
    window_titles = [title for title, hwnd in windows]

    title_counts = Counter(window_titles)

    for title, count in title_counts.items():
        if count > 1:
            # Get all hwnds for the duplicated title
            duplicated_hwnds = [hwnd for t, hwnd in windows if t == title]

            # Keep the first one, close the rest
            for hwnd_to_close in duplicated_hwnds[1:]:
                try:
                    win32gui.PostMessage(hwnd_to_close, win32con.WM_CLOSE, 0, 0)
                    print(f"Closed duplicate window with title: {title}")
                except Exception as e:
                    print(f"Error closing window with title {title}: {e}")
