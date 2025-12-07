def _check_gemini_action():
    ensure_typed("ok, keep going")
    ensure_slept(milliseconds=50)
    ensure_pressed('enter')

def _permit_gemini_action():
    # ensure_pressed("2")
    ensure_pressed('enter')
    ensure_slept(milliseconds=50)

def _check_flash_mode():
    ensure_slept(milliseconds=5000)
    ensure_pressed("1")

def _toggle_auto_mode():
    ensure_pressed("shift", "tab")
    ensure_slept(milliseconds=50)

if __name__ == "__main__":
    try:
        import traceback
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_gemini_cli_executed import ensure_gemini_cli_executed
        from pk_internal_tools.pk_functions.ensure_initial_prompt_to_gemini_cli_sent import ensure_initial_prompt_to_gemini_cli_sent
        from pk_internal_tools.pk_functions.ensure_killed_gemini_related_windows import ensure_killed_gemini_related_windows
        from pk_internal_tools.pk_functions.ensure_pk_gemini_executed import ensure_pk_gemini_executed
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import ensure_pk_starting_routine_done_without_pk_log_file_logging
        from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
        from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.get_pk_gemini_starter_title import get_pk_gemini_starter_title
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root, D_PK_MEMO_REPO, D_AUTO_FLOW_REPO, d_pk_root

        func_n = get_caller_name()

        ensure_pk_starting_routine_done_without_pk_log_file_logging(traced_file=__file__, traceback=traceback)
        # ensure_killed_gemini_related_windows()

        get_pk_gemini_starter_title = get_pk_gemini_starter_title()
        ensure_window_title_replaced(get_pk_gemini_starter_title)
        ensure_window_to_front(get_pk_gemini_starter_title)

        local_gemini_root = ensure_value_completed(
            key_name="local_gemini_root",
            func_n=func_n,
            options=[d_pk_root, D_PK_MEMO_REPO, D_AUTO_FLOW_REPO],
        )
        ensure_gemini_cli_executed(local_gemini_root=local_gemini_root)
        ensure_initial_prompt_to_gemini_cli_sent(initial_prompt="git status 확인 후, 작업내용을 상세히 commit 해줘")
        # ensure_pk_gemini_executed()

        _toggle_auto_mode()
        _check_flash_mode()
        while True:
            _permit_gemini_action()
            _check_gemini_action()
            ensure_slept(milliseconds=5000)

        # TODO :
        # succeeded = ensure_git_status_good()
        # if succeeded:
        #     ensure_spoken("푸쉬 성공")
        #     logging.debug(f'''state={state} ''')
        #     ensure_spoken(f'', wait=True)
        #     ensure_pk_wrapper_starter_suicided(__file__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)