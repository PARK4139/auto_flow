from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_worked_done():
    """
    GEMINI CLI 작업 완료를 음성으로 알립니다.
    """
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    ensure_spoken("GEMINI 작업 완료")
