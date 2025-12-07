from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import ensure_pk_starting_routine_done_without_pk_log_file_logging

if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_flow_executed import ensure_pk_flow_executed
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    # pk_option
    # ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    ensure_pk_starting_routine_done_without_pk_log_file_logging(traced_file=__file__, traceback=traceback)
    try:
        ensure_pk_flow_executed()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
