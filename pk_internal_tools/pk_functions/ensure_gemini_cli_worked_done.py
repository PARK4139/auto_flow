from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_worked_done():
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    ensure_spoken("GEMINI 전체작업 완료", read_finished_wait_mode=True, verbose=True)  # Explicitly wait and enable verbose logging
