def is_os_linux():
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    if not is_os_wsl_linux():
        if not is_os_windows():
            return True
    return False
