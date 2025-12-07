from typing import Optional


# @ensure_seconds_measured
def ensure_command_executed(cmd: str, mode: str = "sync", encoding: Optional[str] = None, mode_with_window: bool = True, errors: Optional[str] = None, mode_silent: bool = False):
    import logging
    import subprocess
    import traceback

    from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.log_aligned import log_aligned
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    func_n = get_caller_name()

    gap = len(func_n)  # 가장 긴 key 길이
    if not mode_silent:
        logging.debug(PK_UNDERLINE)
    # log_aligned(gap=gap, key="", PK_UNDERLINE)    value=
    # log_aligned(gap=gap, key=rf"{func_n}()", PK_UNDERLINE)    value=

    if mode == 'a':
        mode = 'async'

    if encoding is None:
        encoding = PkEncoding.UTF8.value
    if hasattr(encoding, 'value'):
        encoding = encoding.value

    if not mode_silent and QC_MODE:
        log_aligned(gap=gap, key="cmd", value=cmd)
        log_aligned(gap=gap, key="mode", value=mode)
        log_aligned(gap=gap, key="encoding", value=encoding)
        log_aligned(gap=gap, key="mode_with_window", value=str(mode_with_window))

    popen_kwargs = {"shell": True}
    if is_os_windows():
        if not mode_with_window:
            popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    elif mode == "async" and not mode_with_window:
        popen_kwargs["stdout"] = subprocess.DEVNULL
        popen_kwargs["stderr"] = subprocess.DEVNULL

    if mode == "async":
        subprocess.Popen(cmd, **popen_kwargs)
        return None

    try:
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,  # Let subprocess handle decoding
            encoding=encoding,  # Pass the determined encoding
            errors=errors,  # Pass the errors argument
            **popen_kwargs
        )

        stdout = process.stdout
        stderr = process.stderr

        stdout_lines = process.stdout.splitlines() if process.stdout else []
        stderr_lines = process.stderr.splitlines() if process.stderr else []

        if not mode_silent:
            if stdout_lines:
                for idx, line in enumerate(stdout_lines):
                    log_aligned(gap=gap, key=f"LINE {idx}", value=f"{line:<100}")
            else:
                # log_aligned(gap=gap, key="(empty stdout)")    value=
                pass

            if stderr_lines:
                for idx, line in enumerate(stderr_lines):
                    log_aligned(gap=gap, key=f"LINE {idx}", value=f"{line:<100}")

        return stdout_lines, stderr_lines, process.returncode  # Return stdout, stderr, and returncode
    except:
        ensure_debug_loged_verbose(traceback)
        ensure_console_paused()  # pk_option
        return [], [], 1  # Return empty lists and a non-zero returncode on exception
