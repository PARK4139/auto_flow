from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_process_killed_by_window_title(window_title: str):
    import logging

    import win32con
    import win32gui
    import win32process

    from pk_internal_tools.pk_functions.get_window_titles_matches import get_window_titles_matches

    matches = get_window_titles_matches(window_title)
    if not matches:
        logging.debug(f"No window found '{window_title}'")
        return

    logging.debug(f"Found {len(matches)} window(s). Similarity check:")
    for hwnd, title, is_similar in matches:
        sim_mark = "" if is_similar else "  "
        logging.debug(f"{sim_mark} hwnd={hwnd} title={title}")

    # 창 핸들을 기준으로 중복 제거 (동일한 창은 하나만 선택)
    # 모든 창이 같은 PID를 공유하므로 창 핸들로 구분
    unique_windows = {}
    for hwnd, title, similarity in matches:
        if hwnd not in unique_windows:
            unique_windows[hwnd] = (hwnd, title, similarity)

    if not unique_windows:
        logging.debug(f"windows not found to kill")
        return

    # 가장 오래된 창 1개만 선택 (첫 번째 창 핸들)
    first_hwnd = list(unique_windows.keys())[0]
    best_match_hwnd, best_match_title, _ = unique_windows[first_hwnd]
    _, pid = win32process.GetWindowThreadProcessId(best_match_hwnd)

    logging.debug(f"Using best match title: {best_match_title} (HWND={first_hwnd}, PID={pid}, 1개만 종료) ")

    # 특정 창만 닫기 (PID로 프로세스 종료하지 않음)
    try:

        # 창을 직접 닫기
        win32gui.PostMessage(best_match_hwnd, win32con.WM_CLOSE, 0, 0)
        logging.debug(f"창 닫기 요청 완료: {best_match_title} (HWND={first_hwnd})")

    except Exception as e:
        logging.debug(f"창 닫기 실패: {e}")
