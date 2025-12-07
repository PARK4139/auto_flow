if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_max_and_min_value_printed_by_text_seperator import ensure_max_and_min_value_printed_by_text_seperator
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_max_and_min_value_printed_by_text_seperator()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
