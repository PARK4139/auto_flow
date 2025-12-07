def ensure_pycharm_window_to_front():
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_pids import get_pids
    try:
        logging.debug("Attempting to get PIDs for pycharm64.exe")
        pids = get_pids(process_img_n="pycharm64.exe")
        if not pids:
            return
        for pid in pids:
            ensure_window_to_front(pid=pid)
    except:
        ensure_debug_loged_verbose(traceback)
