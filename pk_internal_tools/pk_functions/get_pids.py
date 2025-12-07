from pk_internal_tools.pk_functions.get_pids_by_process_name import get_pids_by_process_name
import logging


def get_pids(process_img_n=None, pid=None):
    """
    프로세스명 또는 PID로 PID 리스트를 반환하는 함수 (기존 함수 호환성 유지)
    
    Args:
        process_img_n (str): 프로세스 이미지명
        pid (int): 프로세스 ID
    
    Returns:
        list: PID 리스트
    """
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    if process_img_n is not None and pid is not None:
        logging.debug(rf"{func_n}() 동작 조건 불충족")
        return

    if process_img_n is not None:
        # 새로운 통합 함수 사용
        return get_pids_by_process_name(process_img_n)
    elif pid is not None:
        # PID로 프로세스 종료 (기존 로직 유지)
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.get_list_leaved_element_pattern import get_list_leaved_element_pattern
        
        cmd = f'taskkill /f /pid {pid}'
        std_list = ensure_command_executed(cmd=cmd)
        pids = get_list_leaved_element_pattern(items=std_list, pattern=r'^\S+\s+(\d+)\s+[A-Za-z]')
        return pids
    else:
        # 모든 프로세스 목록 반환
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        
        cmd = f'tasklist'
        std_list = ensure_command_executed(cmd=cmd)
        return std_list
