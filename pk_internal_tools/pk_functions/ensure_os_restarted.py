def ensure_os_restarted():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    if is_os_windows():
        cmd_list = ['shutdown.exe /r']
    elif is_os_linux():
        cmd_list = ['sudo reboot']  # 'systemctl reboot'
    else:
        cmd_list = ['sudo shutdown -r now']

    for cmd in cmd_list:
        ensure_command_executed(cmd=cmd, mode='a')
