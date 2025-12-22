

import logging


def ensure_pnx_backed_ups_smallest():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug(f"smallest_pnxs에 대한 백업을 시도합니다")
    for target in SMALLEST_PNXS:
        compress_pnx_via_bz(f'{target}')
