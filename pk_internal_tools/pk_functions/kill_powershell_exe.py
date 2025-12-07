def kill_powershell_exe(debug_mode=True):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    try:
        pids = get_pids("powershell.exe")
        for pid in pids:
            ensure_process_killed_via_wmic(pid=pid)
    except:
        logging.debug(rf'''''')


