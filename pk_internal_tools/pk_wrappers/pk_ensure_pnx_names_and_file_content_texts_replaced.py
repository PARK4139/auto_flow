if __name__ == "__main__":
    try:
        import traceback
        from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
        from pk_internal_tools.pk_functions.ensure_pnx_names_and_file_content_texts_replaced import ensure_pnx_names_and_file_content_texts_replaced
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import ensure_pk_starting_routine_done_without_pk_log_file_logging
        from pk_internal_tools.pk_objects.pk_losslesscut import PkLosslesscut
        from pk_internal_tools.pk_objects.pk_system_operation_options import PlayerSelectionMode, SetupOpsForEnsureValueCompleted20251130
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_30 import ensure_value_completed_2025_11_30
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        ensure_pnx_names_and_file_content_texts_replaced()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
        # ensure_pk_wrapper_starter_suicided(__file__)
