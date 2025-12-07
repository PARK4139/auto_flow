if __name__ == "__main__":

    import traceback

    from pk_internal_tools.pk_functions.ensure_edited_code_tested import ensure_edited_code_tested
    from pk_internal_tools.pk_functions.ensure_pk_log_error_log_sent_to_cursor import ensure_pk_log_error_log_sent_to_cursor
    from pk_internal_tools.pk_functions.ensure_slept_by_following_history import ensure_slept_by_following_history
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.ensure_cursor_worked_done import ensure_cursor_worked_done
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback, window_relocate_mode=False)
    func_n = get_caller_name()
    try:
        while 1:
            ensure_cursor_worked_done()
            ensure_slept_by_following_history(key_name="GUI 렌더링 대기", func_n=func_n)
            ensure_edited_code_tested()
            ensure_pk_log_error_log_sent_to_cursor()
            input("continue:enter")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root, console_log_block_mode=False)
