import os  # Added for os.path.join and os.environ
import shlex  # Added for shlex.split
import subprocess  # Moved from inside function
from typing import Optional, Union, List  # Modified import


# @ensure_seconds_measured
def ensure_command_executed(cmd: Union[str, List[str]], mode: str = "sync", encoding: Optional[str] = None, mode_with_window: bool = True, errors: Optional[str] = None, mode_silent: bool = False):
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.log_aligned import log_aligned
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
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
        cmd_to_log = cmd
        if isinstance(cmd_to_log, list):
            cmd_to_log = " ".join(cmd_to_log)  # Convert list to string for logging
        log_aligned(gap=gap, key="cmd", value=cmd_to_log)
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
        # Special handling for Windows to detach processes (e.g., PyCharm)
        if is_os_windows():
            # Check if the command seems to be launching a GUI application with 'start'
            # Determine if cmd is a list (already parsed) or a string (needs parsing)
            if isinstance(cmd, list):
                app_cmd_exec = cmd  # This will be the list for subprocess.Popen
                use_shell = False  # If it's a list, we assume it's for direct execution
            else:  # cmd is a string
                # Check if it's a known GUI app to force shell=False and detachment
                if "pycharm" in cmd.lower() or "code" in cmd.lower():
                    app_cmd_exec = shlex.split(cmd)
                    use_shell = False
                else:
                    # For other string commands, use shell=True by default for async
                    app_cmd_exec = cmd  # This will be the string for subprocess.Popen
                    use_shell = True

            # Use different popen_kwargs if use_shell is False
            if use_shell:
                final_popen_kwargs = popen_kwargs
                # If shell=True, the cmd should be a string
                # Ensure app_cmd_exec is a string when shell=True
                if isinstance(app_cmd_exec, list):
                    app_cmd_exec = " ".join(app_cmd_exec)
            else:
                final_popen_kwargs = {
                    "shell": False,  # Explicitly set shell=False
                    "creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
                    # For now, keep stdout/stderr visible for debugging
                    "stdout": subprocess.DEVNULL,
                    "stderr": subprocess.DEVNULL
                }

                # New logic to handle .BAT/.CMD files
                if isinstance(app_cmd_exec, list) and len(app_cmd_exec) > 0:
                    first_arg = app_cmd_exec[0].lower()
                    if first_arg.endswith(".bat") or first_arg.endswith(".cmd"):
                        logging.debug(f"Detected .BAT/.CMD file, prepending cmd.exe /c: {app_cmd_exec}")
                        app_cmd_exec = [os.path.join(os.environ['SYSTEMROOT'], 'System32', 'cmd.exe'), '/c'] + app_cmd_exec

            if use_shell:
                logging.debug(f"Launching async command (Windows, shell=True): {app_cmd_exec}")
                subprocess.Popen(app_cmd_exec, **final_popen_kwargs)
            else:
                logging.debug(f"Launching detached GUI app directly (Windows, shell=False): {app_cmd_exec}")
                subprocess.Popen(app_cmd_exec, **final_popen_kwargs)
        else:  # Not Windows
            logging.debug(f"Launching async command (Non-Windows): {cmd}")
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
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return [], [], 1  # Return empty lists and a non-zero returncode on exception
#
