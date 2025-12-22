
if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_gemini_cli_executed_interactive import ensure_gemini_cli_executed_interactive
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        ensure_gemini_cli_executed_interactive(__file__=__file__)

    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)
        ensure_pk_wrapper_starter_suicided(__file__)
