from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened

if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import ensure_pk_starting_routine_done_without_pk_log_file_logging
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
    from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    import traceback

    # pk_* -> ensure_pk_starting_routine_done_without_pk_log_file_logging
    ensure_pk_starting_routine_done_without_pk_log_file_logging(traced_file=__file__, traceback=traceback)

    try:
        func_n = get_caller_name()
        window_title = ensure_value_completed_2025_10_13_0000(key_name='window_title', func_n=func_n, options=get_windows_opened())
        ensure_process_killed(window_title_seg=window_title)

    except Exception as exception:
        # pk_* -> ensure_exception_routine_done
        ensure_exception_routine_done(traced_file=__file__, exception=exception, traceback=traceback)

    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
