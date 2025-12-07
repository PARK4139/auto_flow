if __name__ == "__main__":
    import logging
    import os
    import traceback

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_pk_wrappers_killed import ensure_pk_wrappers_killed
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_git_repo_pushed import ensure_git_repo_pushed
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    # pk_option
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    # ensure_pk_starting_routine_done_without_pk_log_file_logging(__file__=__file__, traceback=traceback)
    try:
        state = ensure_git_repo_pushed(d_local_repo = d_pk_root)
        if state and state.get("state") == True:
            ensure_spoken("푸쉬 성공")
            logging.debug(f'''state={state} ''')
            ensure_spoken(f'', wait=True)
            ensure_pk_wrapper_starter_suicided(__file__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
