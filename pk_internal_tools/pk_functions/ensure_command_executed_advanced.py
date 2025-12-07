from typing import Optional

# @ensure_seconds_measured
def ensure_command_executed_advanced(
    cmd: str,
    mode: str = "sync",                          # "sync" | "async"
    encoding: Optional[str] = None,              # preferred encoding (fallbacks applied automatically)
    mode_with_window: bool = True,               # Windows only: show console window or not
    errors: Optional[str] = None,                # "replace" | "ignore" | "surrogateescape" | None
):
    """
    Robust subprocess runner:
    - Never relies on text=True decoding. Capture bytes and decode manually.
    - Decoding order: (provided 'encoding') -> utf-8 -> cp949 -> mbcs -> latin-1.
    - Preserves spacing/columns exactly (no padding/formatting of lines).
    - Logs stdout/stderr lines with your log_aligned() as-is.
    - Returns (stdout_lines, stderr_lines).
    """
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

    try:
        func_n = get_caller_name()
        gap = len(func_n)
        logging.debug(PK_UNDERLINE)

        # Normalize mode
        if mode == "a":
            mode = "async"

        # Normalize encoding enum -> str
        if encoding is None:
            encoding = PkEncoding.UTF8.value if hasattr(PkEncoding, "UTF8") else "utf-8"
        if hasattr(encoding, "value"):
            encoding = encoding.value  # type: ignore[attr-defined]
        if not errors:
            errors = "replace"

        if QC_MODE:
            log_aligned(gap=gap, key="cmd", value=cmd)
            log_aligned(gap=gap, key="mode", value=mode)
            log_aligned(gap=gap, key="encoding", value=str(encoding))
            log_aligned(gap=gap, key="mode_with_window", value=str(mode_with_window))

        # Popen defaults
        popen_kwargs: dict = {"shell": True}
        if is_os_windows():
            if not mode_with_window:
                popen_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        elif mode == "async" and not mode_with_window:
            popen_kwargs["stdout"] = subprocess.DEVNULL
            popen_kwargs["stderr"] = subprocess.DEVNULL

        # Async: fire-and-forget
        if mode == "async":
            subprocess.Popen(cmd, **popen_kwargs)
            return None

        # Helper: robust decode with fallbacks (preserve spacing)
        def _decode_bytes(b: bytes) -> str:
            if not b:
                return ""
            candidates = []
            # n. user-specified encoding, if any
            if encoding:
                candidates.append(encoding)
            # 2) common fallbacks
            candidates.extend(["utf-8", "cp949"])
            # 3) Windows codepage (mbcs) is useful on KR Windows
            candidates.append("mbcs")
            # 4) last resort that never fails
            candidates.append("latin-1")

            for enc in candidates:
                try:
                    return b.decode(enc, errors=errors)  # type: ignore[arg-type]
                except Exception:
                    continue
            # Shouldn't reach here because of errors handling; still safeguard:
            return b.decode("utf-8", errors="replace")

        # --- SYNC path: capture BYTES, then decode ourselves ---
        completed = subprocess.run(
            cmd,
            capture_output=True,   # get bytes
            text=False,            # IMPORTANT: do not auto-decode
            check=False,
            **popen_kwargs,
        )

        # Decode stdout/stderr separately (preserve exact spacing/newlines)
        raw_out = completed.stdout or b""
        raw_err = completed.stderr or b""

        stdout_text = _decode_bytes(raw_out)
        stderr_text = _decode_bytes(raw_err)

        # Keep lines without padding/formatting to preserve columns
        stdout_lines = stdout_text.splitlines()
        stderr_lines = stderr_text.splitlines()

        if stdout_lines:
            for idx, line in enumerate(stdout_lines):
                # Do NOT format/pad the line; pass as-is to keep columns intact
                log_aligned(gap=gap, key=f"LINE {idx}", value=line)
        # else: (no stdout)

        if stderr_lines:
            for idx, line in enumerate(stderr_lines):
                log_aligned(gap=gap, key=f"LINE {idx}", value=line)

        return stdout_lines, stderr_lines

    except Exception:
        ensure_debug_loged_verbose(traceback)
        ensure_console_paused()  # optional pause for debug
        return [], []
