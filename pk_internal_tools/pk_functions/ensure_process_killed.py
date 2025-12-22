def ensure_process_killed(window_title_seg: str):
    import subprocess
    import wmi
    from pk_internal_tools.pk_functions.get_window_title import get_window_title
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.get_nx import get_nx

    """
    Kill Windows processes that match a specific window title segment in their command line.
    """
    try:
        window_title = get_window_title(window_title_seg=window_title_seg)
        logging.debug(f"window_title={window_title} ")

        if not window_title:
            logging.debug("window_title is empty")
            return

        matched_pids = set()
        c = wmi.WMI()

        for proc in c.query("SELECT ProcessId, CommandLine, Caption FROM Win32_Process"):
            caption = (proc.Caption or "").lower()
            command_line = (proc.CommandLine or "").lower()
            if "cmd.exe" in caption and get_nx(window_title).lower() in command_line:
                matched_pids.add(proc.ProcessId)

        if not matched_pids:
            logging.debug(f"PK KILL '{window_title}' not found")
            return

        for pid in matched_pids:
            logging.debug(f"PK KILL PID={pid} window_title={window_title}")
            subprocess.run(['taskkill', '/PID', str(pid), '/T', '/F'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

    except Exception as e:
        logging.warning(f"{e}")
