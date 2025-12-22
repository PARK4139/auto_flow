import logging

from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def ensure_matrix_console_made():
    import os
    import subprocess

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    os.system('color 0A')
    os.system('color 02')
    while 1:
        lines = subprocess.check_output('dir /b /s /o /a-d', shell=True).decode('utf-8').split("\n")
        for line in lines:
            if "" != line:
                if os.getcwd() != line:
                    logging.debug(lines)
        ensure_slept(seconds=60)
