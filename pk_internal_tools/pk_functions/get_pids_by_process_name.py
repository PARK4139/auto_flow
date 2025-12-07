def get_pids_by_process_name(process_img_n):
    """
    프로세스명으로 PID 리스트를 반환 (기존 get_pids 함수 개선)

    Args:
        process_img_n (str): 프로세스 이미지명

    Returns:
        list: PID 리스트
    """
    import logging
    import re

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_list_leaved_element_pattern import get_list_leaved_element_pattern

    if not isinstance(process_img_n, str):
        logging.debug(f"[get_pids_by_process_name] [PID 검색 중 오류 발생: process_img_n이 문자열이 아닙니다. (타입: {type(process_img_n)})]")
        return []
    try:
        cmd = f"tasklist | findstr {process_img_n}"
        stdout_lines, _ = ensure_command_executed(cmd=cmd) # stdout_lines만 사용
        pids = get_list_leaved_element_pattern(items=stdout_lines, pattern=r'^\S+\s+(\d+)\s+[A-Za-z]')

        logging.debug(f"프로세스 '{process_img_n}'에서 {len(pids)}개의 PID를 찾았습니다.")
        return pids

    except Exception as e:
        logging.debug(f"PID 검색 중 오류 발생: {e}")
        return []