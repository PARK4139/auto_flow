if __name__ == "__main__":
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_git_repo_pushed import ensure_git_repo_pushed
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_directories import D_PK_MEMO_REPO, d_pk_root, D_AUTO_FLOW_REPO

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()
        repo_to_push = ensure_value_completed(
            key_name="repo_to_push",
            func_n=func_n,
            options=[d_pk_root, D_PK_MEMO_REPO, D_AUTO_FLOW_REPO],
        )
        ai_commit_massage_mode = ensure_value_completed(
            key_name="ai_commit_massage_mode",
            func_n=func_n,
            options=[True, False],
        )
        state = ensure_git_repo_pushed(d_local_repo=repo_to_push, ai_commit_massage_mode=bool(ai_commit_massage_mode))
        if state and state.get("state") == True:
            logging.debug(f'''state={state} ''')
            ensure_spoken("푸쉬 성공", wait=True)
            ensure_pk_wrapper_starter_suicided(__file__)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
