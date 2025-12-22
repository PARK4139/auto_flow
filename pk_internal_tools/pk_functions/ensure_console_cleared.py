# @ensure_seconds_measured  # elapsed_seconds= 0.2632 at ensure_console_cleared()
def ensure_console_cleared():
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    import os

    if is_os_windows():
        os.system('cls')
    else:
        os.system('clear')
