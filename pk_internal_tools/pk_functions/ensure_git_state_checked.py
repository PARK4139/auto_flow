def ensure_git_state_checked(start_time, label):
    import logging
    import time

    from pk_internal_tools.pk_functions.run_command import run_command
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP

    cmd = "git status"
    _, output = run_command(cmd, capture_output=True)
    output = output.split("\n")
    for _ in output:
        logging.debug(f"{PK_ANSI_COLOR_MAP['YELLOW']}{_}{PK_ANSI_COLOR_MAP['RESET']}")
    duration = time.time() - start_time
    logging.debug(f"{PK_ANSI_COLOR_MAP['YELLOW']}{label}{PK_ANSI_COLOR_MAP['RESET']} at {time.strftime('%Y-%m-%d %H:%M:%S')} (elapsed {duration:.2f} sec)")
    return False

