from pk_internal_tools.pk_objects.pk_texts import PkTexts


def ensure_windows_closed(window_title):
    """특정 창을 닫는 함수
    
    Args:
        window_title (str): 닫을 창의 제목
    
    Returns:
        bool: 창을 닫았으면 True, 못 닫았으면 False
    """
    import time
    import logging
    from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd

    # 닫을 창 제목들
    window_titles_to_close = [window_title]

    max_wait_time = 10  # 최대 10초 대기
    wait_count = 0
    
    while wait_count < max_wait_time:
        # 현재 열린 창 목록 확인 (디버깅용)
        windows_opened = get_windows_opened_with_hwnd()
        everything_windows = [w for w in windows_opened if "Everything" in w]
        if everything_windows:
            logging.debug(f"{PkTexts.FOUND_WINDOWS} Everything 창들: {everything_windows}")
        
        # 각 창 제목에 대해 창이 열려있는지 확인하고 닫기
        for title in window_titles_to_close:
            if is_window_opened(window_title_seg=title):
                logging.debug(f"{PkTexts.WINDOW_CLOSE_ATTEMPT}: {title}")
                ensure_process_killed(window_title_seg=title)
                return True  # 창을 닫았으면 True 반환
        
        time.sleep(0.5)  # 0.5초씩 대기
        wait_count += 1
    
    logging.debug(f"'{window_title}' {PkTexts.WINDOW_NOT_FOUND_OR_CANNOT_CLOSE}.")
    return False  # 창을 닫지 못했으면 False 반환
