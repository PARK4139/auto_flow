def ensure_screen_saved():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    if is_os_windows():
        # ensure_command_executed_like_human(cmd=rf'''%systemroot%\system32\scrnsave.scr /s''')# 성공
        cmd = rf'''%systemroot%\system32\scrnsave.scr /s '''
        ensure_command_executed(cmd=cmd)
