def kill_cmd_exe():
    import logging
    from pk_internal_tools.pk_functions.ensure_process_killed_by_pid import ensure_process_killed_by_pid
    from pk_internal_tools.pk_functions.get_pids import get_pids
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    try:
        pids = get_pids(process_img_n ="cmd.exe")
        for pid in pids:
            ensure_process_killed_by_pid(pid=pid)
    except Exception as e:
        logging.debug(rf'''''')