from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_interactive_mode_initial_prompt_sent(initial_prompt=None):
    """
        TODO: Write docstring for ensure_gemini_cli_interactive_mode_initial_prompt_sent.
    """
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title
    from pk_internal_tools.pk_functions.ensure_gemini_cli_interactive_mode_prompt_sent import ensure_gemini_cli_interactive_mode_prompt_sent
    from pk_internal_tools.pk_functions.get_gemini_cli_interactive_mode_initial_prompt import get_gemini_cli_interactive_mode_initial_prompt

    try:
        gemini_cli_window_title = get_gemini_cli_window_title()
        if initial_prompt is None:
            initial_prompt = get_gemini_cli_interactive_mode_initial_prompt()
        ensure_gemini_cli_interactive_mode_prompt_sent(
            prompts=[initial_prompt],
            gemini_cli_window_title=gemini_cli_window_title,
        )
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
