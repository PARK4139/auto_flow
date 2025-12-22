from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_killed_gemini_related_windows():
    from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
    from pk_internal_tools.pk_functions.get_gemini_prompt_interface_title import get_pk_gemini_title
    from pk_internal_tools.pk_functions.get_pk_gemini_starter_title import get_pk_gemini_starter_title
    from pk_internal_tools.pk_functions.get_routine_pk_gemini_enabled_child_process_title import get_routine_pk_gemini_enabled_child_process_title
    """
        TODO: Write docstring for ensure_killed_gemini_related_windows.
    """
    try:
        titles = [
            get_pk_gemini_title(),
            get_pk_gemini_starter_title(),
            get_routine_pk_gemini_enabled_child_process_title(),
            "Windows PowerShell", # TODO 이거 조심스럽긴 한데. 써보자
        ]
        for title in titles:
            ensure_windows_killed_like_human_by_window_title(title)
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
