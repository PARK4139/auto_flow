def ensure_seconds_measured(func):
    # TODO alert_as_gui로 나오도록 다만, auto_click_after_milliseconds
    # TODO FUNCTION PERFORMANCE DATA 수집
    # TODO FUNCTION PERFORMANCE DATA 통계
    # TODO FUNCTION PERFORMANCE DATA 느린기능찾기
    # TODO FUNCTION PERFORMANCE DATA 느린기능개선
    import logging
    from functools import wraps
    from pk_internal_tools.pk_objects.pk_colors import PkColors

    @wraps(func)
    def wrapper(*args, **kwargs):
        # wrapper 함수가 실행될 때 QC_MODE를 임포트
        try:
            from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        except ImportError:
            QC_MODE = False
            logging.warning(f"Failed to import QC_MODE at runtime for {func.__name__}, defaulting to False.")

        if not QC_MODE:
            return func(*args, **kwargs) # QC_MODE가 False면 원본 함수 실행

        import time

        time_s = time.time()

        result = func(*args, **kwargs)

        elapsed_seconds = time.time() - time_s
        elapsed_seconds_str = rf"{PkColors.YELLOW}elapsed_seconds={elapsed_seconds: .4f}{PkColors.RESET}"

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
