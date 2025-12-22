

def ensure_wsl_exe_killed():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_process_killed_via_taskkill import ensure_process_killed_via_taskkill
    from pk_internal_tools.pk_functions.ensure_writen_like_human import ensure_writen_like_human
    from pk_internal_tools.pk_functions.get_pids import get_pids
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    process_name = "wsl.exe"
    cmd = "wsl --shutdown"
    ensure_command_executed(cmd=cmd, mode="a")
    pids = get_pids("wsl.exe")
    if pids is not None:
        for pid in pids:
            if pid is not None:
                ensure_process_killed_via_taskkill(pid=pid)
    ensure_writen_like_human("exit")
    ensure_pressed("enter")


