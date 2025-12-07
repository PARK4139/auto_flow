
if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_gemini_cli_executed_interactive import ensure_gemini_cli_executed_interactive
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        ensure_gemini_cli_executed_interactive(__file__=__file__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
        ensure_pk_wrapper_starter_suicided(__file__)
