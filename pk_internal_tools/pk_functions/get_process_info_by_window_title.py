def get_process_info_by_window_title(window_title_seg):
    """
    윈도우 타이틀로 프로세스 정보를 검색하는 함수

    Args:
        window_title_seg (str): 윈도우 타이틀 일부

    Returns:
        list: 프로세스 정보 딕셔너리 리스트
    """
    import logging

    from pk_internal_tools.pk_functions.get_process_info_by_pid import get_process_info_by_pid
    from pk_internal_tools.pk_functions.get_pid_by_window_title import get_pid_by_window_title # Import from new file

    try:
        pid = get_pid_by_window_title(window_title_seg)
        if not pid:
            return []

        if isinstance(pid, list):
            # 여러 PID가 있는 경우
            process_info_list = []
            for p in pid:
                process_info = get_process_info_by_pid(p)
                if process_info:
                    process_info_list.append(process_info)
            return process_info_list
        else:
            # 단일 PID인 경우
            process_info = get_process_info_by_pid(pid)
            return [process_info] if process_info else []

    except Exception as e:
        logging.debug(f"윈도우 타이틀 프로세스 정보 검색 중 오류 발생: {e}")
        return []