if __name__ == "__main__":

    try:
        import traceback
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done_without_pk_log_file_logging import ensure_pk_starting_routine_done_without_pk_log_file_logging
        from pk_internal_tools.pk_objects.pk_losslesscut import PkLosslesscut
        from pk_internal_tools.pk_objects.pk_system_operation_options import PlayerSelectionMode, SetupOpsForEnsureValueCompleted20251130
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_30 import ensure_value_completed_2025_11_30
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

        ensure_pk_starting_routine_done_without_pk_log_file_logging(traced_file=__file__, traceback=traceback)

        func_n = get_caller_name()
        options_for_selection_mode = [member.value.lower() for member in PlayerSelectionMode]
        selected_mode_str = ensure_value_completed_2025_11_30(
            key_name="player_selection_mode",
            func_n=func_n,
            options=options_for_selection_mode,
            guide_text="재생 모드를 선택하세요 (자동 | 수동):",
            sort_order=SetupOpsForEnsureValueCompleted20251130.HISTORY
        )
        selected_selection_mode = PlayerSelectionMode(selected_mode_str.upper())
        player = PkLosslesscut(selection_mode=selected_selection_mode)
        player.ensure_state_machine_executed()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_root)
        # ensure_pk_wrapper_suicided(__file__)
