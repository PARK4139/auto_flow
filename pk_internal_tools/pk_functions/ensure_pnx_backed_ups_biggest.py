

def ensure_pnx_backed_ups_biggest():
    from pk_internal_tools.pk_objects.pk_etc import BIGGEST_PNXS
    import logging
    from pk_internal_tools.pk_functions.compress_pnx_via_bz import compress_pnx_via_bz
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug(f"biggest_pnxs에 대한 백업을 시도합니다")
    for biggest_target in BIGGEST_PNXS:
        compress_pnx_via_bz(f'{biggest_target}')
