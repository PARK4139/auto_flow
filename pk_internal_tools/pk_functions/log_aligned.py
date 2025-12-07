# @ensure_seconds_measured
import logging

from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE


def log_aligned(*, key: str, value: str, gap: int, width: int = 100, seperator: str = '|'):
    """
    # expected return format
    key      | value

    # tip
    gap = len("mode_with_window")  # 가장 긴 key 길이

    """
    import logging
    logging.debug(f"{key:<{gap}}  {seperator} {value:<{width}}")


def log_command_output_aligned(
        command: str,
        mode: str,
        encoding: str,
        mode_with_window: bool,
        stdout: str,
        stderr: str,
        returncode: int,
        logger_name: str = __name__
):
    gap = 24  # Based on the example output "LINE 0                   |"
    width = 100  # Default width
    seperator = '|'

    logging.debug(PK_UNDERLINE)
    log_aligned(key="cmd", value=command, gap=gap, width=width, seperator=seperator)
    log_aligned(key="mode", value=mode, gap=gap, width=width, seperator=seperator)
    log_aligned(key="encoding", value=encoding, gap=gap, width=width, seperator=seperator)
    log_aligned(key="mode_with_window", value=str(mode_with_window), gap=gap, width=width, seperator=seperator)

    if stdout:
        for i, line in enumerate(stdout.splitlines()):
            log_aligned(key=f"LINE {i}", value=line, gap=gap, width=width, seperator=seperator)
    if stderr:
        for i, line in enumerate(stderr.splitlines()):
            log_aligned(key=f"STDERR {i}", value=line, gap=gap, width=width, seperator=seperator)

    log_aligned(key="returncode", value=str(returncode), gap=gap, width=width, seperator=seperator)
    logging.debug(PK_UNDERLINE)
