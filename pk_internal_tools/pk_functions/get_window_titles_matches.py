from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_window_titles_matches(window_title: str):
    import win32gui
    from pk_internal_tools.pk_functions.calculate_similarity_beteen_window_title_and_target import calculate_similarity_beteen_window_title_and_target

    matches = []

    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                similarity = calculate_similarity_beteen_window_title_and_target(window_title, title)
                if similarity >= 1.0:  # 유사도 임계값을 완전히 동일하게 설정 (0.9 → 1.0)
                    matches.append((hwnd, title, similarity))

    win32gui.EnumWindows(enum_handler, None)
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches
