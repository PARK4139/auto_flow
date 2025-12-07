from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical


def print_os_sys_environment_variables():
    import os
    import ipdb
    ensure_iterable_log_as_vertical(item_iterable=os.environ, item_iterable_n='모든 시스템 환경변수 출력')

    ipdb.set_trace()
