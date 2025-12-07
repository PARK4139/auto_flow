from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    # from pk_internal_tools.pk_objects.500_live_logic import ensure_power_saved_as_s4, ensure_spoken, ensure_screen_saved
    from pk_internal_tools.pk_functions import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_screen_saved import ensure_screen_saved
    from pk_internal_tools.pk_functions.ensure_power_saved_as_s4 import ensure_power_saved_as_s4

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        ensure_screen_saved()
        ensure_spoken('최대 절전 모드 진입')
        ensure_power_saved_as_s4()


    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
        ensure_pk_wrapper_starter_suicided(__file__)
