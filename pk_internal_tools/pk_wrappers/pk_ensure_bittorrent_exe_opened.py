if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_bittorrent_exe_opened import ensure_bittorrent_exe_opened
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    import traceback
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_bittorrent_exe_opened()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
        ensure_pk_wrapper_starter_suicided(__file__)  # pk_option
