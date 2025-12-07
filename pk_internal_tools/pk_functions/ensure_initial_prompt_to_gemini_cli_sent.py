from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_initial_prompt_to_gemini_cli_sent(initial_prompt=None):
    """
        TODO: Write docstring for ensure_initial_prompt_to_gemini_cli_sent.
    """
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title
    from pk_internal_tools.pk_functions.ensure_gemini_cli_requests_processed_2025_11_22 import ensure_gemini_cli_requests_processed_2025_11_22
    from pk_internal_tools.pk_functions.get_gemini_prompt_starting import get_gemini_prompt_starting

    try:
        gemini_cli_window_title = get_gemini_cli_window_title()
        if initial_prompt is None:
            initial_prompt = get_gemini_prompt_starting()
        ensure_gemini_cli_requests_processed_2025_11_22(
            prompts=[initial_prompt],
            gemini_cli_window_title=gemini_cli_window_title,
        )
        return True
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
