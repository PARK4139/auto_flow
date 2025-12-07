if __name__ == "__main__":
    try:
        import os
        import traceback
        from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
        from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed import ensure_pk_wrapper_starter_executed
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    except:
        traceback.print_exc()
        ensure_console_paused()

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        os.chdir(d_pk_root)
        ensure_pk_wrapper_starter_executed()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
