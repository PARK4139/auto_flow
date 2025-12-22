from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed


def print_os_sys_environment_variables():
    import os
    import ipdb
    ensure_iterable_data_printed(iterable_data=os.environ, iterable_data_n='모든 시스템 환경변수 출력')

    ipdb.set_trace()
