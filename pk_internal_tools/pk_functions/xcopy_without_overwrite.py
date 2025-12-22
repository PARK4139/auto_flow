import logging

from pk_internal_tools.pk_functions.ensure_command_executed_like_human_as_admin import ensure_command_executed_like_human_as_admin
from pk_internal_tools.pk_functions.is_f import is_f


def xcopy_without_overwrite(pnx, pnx_future):
    import inspect
    import os
    import traceback

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    try:
        if os.path.exists(pnx_future):
            pnx_future = rf"{os.path.dirname(pnx_future)}\{os.path.basename(pnx)[0]}_{get_pk_time_2025_10_20_1159('%Y_%m_%d_%H_%M_%S_%f')}{os.path.basename(pnx)[1]}"
        ensure_command_executed_like_human_as_admin(rf'echo a | xcopy "{pnx}" "{pnx_future}" /e /h /k')
        if is_f(pnx):
            ensure_command_executed_like_human_as_admin(rf'echo f | xcopy "{pnx}" "{pnx_future}" /e /h /k')
        else:
            ensure_command_executed_like_human_as_admin(rf'echo d | xcopy "{pnx}" "{pnx_future}" /e /h /k')
    except Exception as e:
        print(rf"subprocess.CalledProcessError 가 발생하여 재시도를 수행합니다 {inspect.currentframe().f_code.co_name}")
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
