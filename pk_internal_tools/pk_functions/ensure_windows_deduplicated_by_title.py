def ensure_windows_deduplicated_by_title():
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
    from collections import defaultdict
    import logging
    from pk_internal_tools.pk_functions.ensure_process_deduplicated import ensure_process_deduplicated
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_values_sanitize_for_cp949 import get_values_sanitize_for_cp949
    from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical

    # ① 열린 창 목록 확보 및 CP949 대응 처리
    values = get_windows_opened_with_hwnd()
    values = [get_values_sanitize_for_cp949(v) for v in values]

    # ② 제목별로 그룹핑 (윈도우 제목 기준)
    grouped = defaultdict(list)
    for title in values:
        grouped[title].append(title)

    ensure_iterable_log_as_vertical(item_iterable=sorted(grouped), item_iterable_n="중복 확인 대상 창 제목들")

    # ③ 각 제목에 대해 1개만 남기고 닫기 시도
    for window_title in grouped:
        logging.debug(f"[처리 중] 창 제목='{window_title}' 중복 제거")
        ensure_process_deduplicated(window_title_seg=window_title, exact=True)
        # ensure_slept(seconds=1000)
        # ensure_slept(seconds=500)
        ensure_slept(milliseconds=200)  # 너무 빠르게 반복되지 않도록 약간 대기
