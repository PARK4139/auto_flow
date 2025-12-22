from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def move_without_overwrite_via_robocopy(src, dst):  # 명령어 자체가 안되는데 /mir 은 되는데 /move 안된다
    import inspect
    import os
    import traceback

    src = src
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    try:
        logging.debug(f'타겟이동 시도')
        # run_via_cmd_exe(rf'robocopy "{pnx_todo}" "{dst}" /MOVE')
        if os.path.exists(rf'{dst}\{os.path.dirname(src)}'):
            ensure_pnxs_move_to_recycle_bin(src)

    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
