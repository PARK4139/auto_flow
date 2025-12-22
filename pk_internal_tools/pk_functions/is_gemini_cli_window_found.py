from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def is_gemini_cli_window_found(local_gemini_root=None):
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title_by_auto import get_gemini_cli_window_title_by_auto
    gemini_cli_window_title = get_gemini_cli_window_title_by_auto(local_gemini_root)
    if gemini_cli_window_title:
        return True
    return False
