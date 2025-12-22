import logging


def ensure_status_printed_step(step_num: int, cmd: str, code: int, output: str) -> str:
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    if code == 0:
        label, color = "SUCCESS", PkColors.CYAN
    elif "nothing to commit" in output.lower():
        label, color = "SKIPPED", PkColors.YELLOW
    elif "everything up-to-date" in output.lower():
        label, color = "SKIPPED", PkColors.YELLOW
    else:
        label, color = "FAILED", PkColors.RED
    logging.debug(f"[{color}{label}{PkColors.RESET} ] [STEP {step_num}] {cmd}")
    return label


