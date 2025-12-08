from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

if __name__ == "__main__":
    try:
        import traceback

        from pk_internal_tools.pk_functions.ensure_initial_prompt_to_gemini_cli_sent import ensure_initial_prompt_to_gemini_cli_sent
        from pk_internal_tools.pk_functions.ensure_killed_gemini_related_windows import ensure_killed_gemini_related_windows
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_gemini_cli_executed import ensure_gemini_cli_executed
        from pk_internal_tools.pk_functions.ensure_pk_gemini_executed import ensure_pk_gemini_executed
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import ensure_pk_starting_routine_done_without_pk_log_file_logging
        from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
        from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
        from pk_internal_tools.pk_functions.get_pk_gemini_starter_title import get_pk_gemini_starter_title
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root, d_pk_root, d_pk_memo_repo, d_auto_flow_repo
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        ensure_pk_starting_routine_done_without_pk_log_file_logging(traced_file=__file__, traceback=traceback)
        
        func_n = get_caller_name()
        root_path_gemini_launched = ensure_value_completed(
            key_name="root_path_gemini_launched",
            func_n=func_n,
            options=[d_pk_root, d_pk_memo_repo, d_auto_flow_repo],
        )

        ensure_killed_gemini_related_windows()

        get_pk_gemini_starter_title = get_pk_gemini_starter_title()
        ensure_window_title_replaced(get_pk_gemini_starter_title)
        ensure_window_to_front(get_pk_gemini_starter_title)

        ensure_gemini_cli_executed(root_path_gemini_launched=root_path_gemini_launched)
        ensure_initial_prompt_to_gemini_cli_sent()
        ensure_pk_gemini_executed(root_path_gemini_launched=root_path_gemini_launched)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_root)
        ensure_windows_killed_like_human_by_window_title(get_pk_gemini_starter_title())