from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
import logging


@ensure_seconds_measured
def ensure_pk_system_log_editable():
    from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
    from pk_internal_tools.pk_objects.pk_files import F_PYCHARM_EXE

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG
    if F_PYCHARM_EXE:
        # 'start' 명령어 없이 실행 파일과 인자를 직접 리스트로 전달 (windows shell=False 호환)
        command_list = [str(F_PYCHARM_EXE), str(F_PK_LOG)]
        ensure_command_executed(cmd=command_list, mode='a', mode_with_window=True) # mode_with_window=True는 새 창으로 실행을 시도
        ensure_window_to_front(window_title_seg=get_nx(F_PK_LOG))
    else:
        logging.warning("PyCharm 실행 파일을 찾을 수 없어 로그 파일을 열 수 없습니다.")
