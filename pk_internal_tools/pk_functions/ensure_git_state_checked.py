def ensure_git_state_checked(start_time, label):
    import logging
    import time

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_colors import PkColors

    cmd = "git status"
    stdout_lines, stderr_lines, _ = ensure_command_executed(cmd)
    output_lines = stdout_lines + stderr_lines
    for _ in output_lines:
        logging.debug(f"{PkColors.YELLOW}{_}{PkColors.RESET}")
    duration = time.time() - start_time
    logging.debug(f"{PkColors.YELLOW}{label}{PkColors.RESET} at {time.strftime('%Y-%m-%d %H:%M:%S')} (elapsed {duration:.2f} sec)")
    return False

