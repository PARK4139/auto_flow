if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_xavier_terminal_opened_via_ssh_like_person import ensure_pk_xavier_terminal_opened_via_ssh_like_person
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        ensure_pk_xavier_terminal_opened_via_ssh_like_person()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_root)
