if __name__ == '__main__':
    try:
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_cmd_exe_deduplicated_all_in_loop import ensure_cmd_exe_deduplicated_all_in_loop

        import traceback
        from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
        from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
        import logging
        from pk_internal_tools.pk_functions.ensure_windows_deduplicated import ensure_windows_deduplicated
        from pk_internal_tools.pk_functions.ensure_chcp_65001 import ensure_chcp_65001
        from pk_internal_tools.pk_functions.get_f_current_n import get_f_current_n
        from pk_internal_tools.pk_functions.deprecated_get_d_current_n_like_human import deprecated_get_d_current_n_like_human

        ensure_cmd_exe_deduplicated_all_in_loop()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
