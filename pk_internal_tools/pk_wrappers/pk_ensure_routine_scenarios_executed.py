if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_scenario_as_cmd_exe_kill_v1_v2_performance_comparison_test_ran import ensure_scenario_as_cmd_exe_kill_v1_v2_performance_comparison_test_ran
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_pk_log_initialized(__file__)
        ensure_pk_wrapper_starter_suicided(__file__)
        ensure_window_title_replaced(get_nx(__file__))

        ensure_scenario_as_cmd_exe_kill_v1_v2_performance_comparison_test_ran()



    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
