from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
import logging


@ensure_seconds_measured
def ensure_pycharm_opened():
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    from pk_internal_tools.pk_objects.pk_files import F_PYCHARM_EXE

    if F_PYCHARM_EXE:
        ensure_command_executed(cmd=f'start "" {get_text_chain(F_PYCHARM_EXE, D_PK_ROOT)}', mode='a')
    else:
        logging.warning("PyCharm 실행 파일을 찾을 수 없어 PyCharm을 열 수 없습니다.")
