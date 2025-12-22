from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_executed():
    import os

    from pk_internal_tools.pk_functions.ensure_gemini_cli_executed_interactive import ensure_gemini_cli_executed_interactive
    from pk_internal_tools.pk_functions.ensure_gemini_cli_executed import ensure_gemini_cli_executed
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT

    # GEMINI.md 위치 로 이동
    os.chdir(D_PK_ROOT)

    ensure_gemini_cli_executed_interactive(__file__=__file__)

    if not ensure_gemini_cli_executed():
        return False
