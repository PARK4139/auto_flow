import logging


def ensure_status_printed_step(step_num: int, cmd: str, code: int, output: str) -> str:
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    if code == 0:
        label, color = "SUCCESS", PK_ANSI_COLOR_MAP['CYAN']
    elif "nothing to commit" in output.lower():
        label, color = "SKIPPED", PK_ANSI_COLOR_MAP['YELLOW']
    elif "everything up-to-date" in output.lower():
        label, color = "SKIPPED", PK_ANSI_COLOR_MAP['YELLOW']
    else:
        label, color = "FAILED", PK_ANSI_COLOR_MAP['RED']
    logging.debug(f"[{color}{label}{PK_ANSI_COLOR_MAP['RESET']} ] [STEP {step_num}] {cmd}")
    return label


