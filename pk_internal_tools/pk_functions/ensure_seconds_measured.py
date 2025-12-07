def ensure_seconds_measured(func):
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging
    from functools import wraps
    if not QC_MODE:
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        import time

        time_s = time.time()

        result = func(*args, **kwargs)

        elapsed_seconds = time.time() - time_s
        elapsed_seconds_str = rf"{PK_ANSI_COLOR_MAP['YELLOW']}elapsed_seconds={elapsed_seconds: .4f}{PK_ANSI_COLOR_MAP['RESET']}"

        log_message = f"{elapsed_seconds_str} at {func.__name__}()"

        # Check for NUL characters before logging (for debugging purposes, can be removed later)
        if '\x00' in func.__name__:
            logging.warning(f"NUL character found in function name: {repr(func.__name__)}")
        if '\x00' in elapsed_seconds_str:
            logging.warning(f"NUL character found in elapsed_seconds string: {repr(elapsed_seconds_str)}")
        if '\x00' in log_message:
            logging.warning(f"NUL character found in final log message: {repr(log_message)}")

        logging.debug(log_message)  # Removed repr()

        return result

    return wrapper
