def get_pid_by_window_title(window_title_seg):
    """
    윈도우 타이틀로 PID를 찾는 함수 (기존 get_pid_by_window_title_via_tasklist 함수 개선)

    Args:
        window_title_seg (str): 윈도우 타이틀 일부

    Returns:
        str or list: PID 또는 PID 리스트
    """
    import logging

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    try:
        cmd = rf'tasklist'
        lines = ensure_command_executed(cmd=cmd)
        matching_lines = None

        for line in lines:
            if window_title_seg in line:
                matching_lines = line
                break

        if not matching_lines:
            logging.debug(f"️ 윈도우 타이틀 '{window_title_seg}'을 포함하는 프로세스를 찾을 수 없습니다.")
            return None

        pids = []
        parts = matching_lines.split()
        if len(parts) > 1 and window_title_seg in parts[0]:
            pids.append(parts[1])

        if len(pids) == 1:
            logging.debug(f"윈도우 타이틀 '{window_title_seg}'의 PID: {pids[0]}")
            return pids[0]
        else:
            logging.debug(f"윈도우 타이틀 '{window_title_seg}'의 PID들: {pids}")
            return pids

    except Exception as e:
        logging.debug(f"윈도우 타이틀 PID 검색 중 오류 발생: {e}")
        return None