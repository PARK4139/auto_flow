from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_cursor_enabled import ensure_cursor_enabled
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_repo_editable import ensure_pk_repo_editable
    from pk_internal_tools.pk_functions.ensure_pycharm_opened import ensure_pycharm_opened
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    try:
        ensure_pk_wrapper_starter_suicided(__file__)
        ensure_pk_colorama_initialized_once()
        ensure_window_title_replaced(get_nx(__file__))

        ensure_pk_repo_editable()
        ensure_pycharm_opened()
        ensure_cursor_enabled()

        # ensure_claude_enabled()

        # ensure_slept(milliseconds=5000)
        
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
