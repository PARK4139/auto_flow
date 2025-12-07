if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_python_file_executed_in_uv_venv_windows import ensure_pk_python_file_executed_in_uv_venv_windows
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
    from pk_internal_tools.pk_objects.pk_directories import D_PK_wrappers, D_PK_FUNCTIONS, d_pk_wrappers

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()

        key_name = 'python_file'
        options = get_pnxs_from_d_working(d_working=D_PK_wrappers)
        options += get_pnxs_from_d_working(d_working=D_PK_FUNCTIONS)
        options += get_pnxs_from_d_working(d_working=d_pk_wrappers)
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
        python_file = selected

        ensure_pk_python_file_executed_in_uv_venv_windows(python_file)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
