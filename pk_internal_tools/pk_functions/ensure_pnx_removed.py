def ensure_pnx_removed(pnx):
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_pnxs_move_to_recycle_bin import ensure_pnxs_move_to_recycle_bin
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pathlib import Path

    import os
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if not Path(pnx).exists():
        logging.debug(f'''삭제할 {get_nx(pnx)} 가 없습니다. ''')
        return
    if Path(pnx).exists():
        # 1
        # if is_f(pnx):
        #     cmd = rf'echo y | del /f "{pnx}"'
        # else:
        #     cmd = rf'echo y | rmdir /s "{pnx}"'
        # ensure_command_executed(cmd=cmd)

        # 2
        # if does_pnx_exist(pnx):
        #     os.remove(pnx)

        # 3
        ensure_pnxs_move_to_recycle_bin(pnxs=[pnx])
    if not os.path.exists(pnx):
        logging.debug(rf"[{func_n}] pnx={pnx} ")
    else:
        logging.debug(rf"[{func_n}] pnx={pnx} ")
