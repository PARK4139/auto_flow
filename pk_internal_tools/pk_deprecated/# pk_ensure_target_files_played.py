if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_potplayer import PkPotplayer
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.ensure_target_file_controller_executed import ensure_target_file_controller_executed # Manual mode entry point

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    # ensure_pk_starting_routine_done_without_pk_log_file_logging(__file__=__file__, traceback=traceback)
    try:
        func_n = get_caller_name()
        mode_options = ["자동 모드", "수동 모드"]
        selected_mode = ensure_value_completed(
            key_name="playback_mode_selection",
            func_n=func_n,
            options=mode_options,
            guide_text="재생 모드를 선택하세요:"
        )

        if selected_mode == "자동 모드":
            player = PkPotplayer()
            player.ensure_state_machine_executed()
        elif selected_mode == "수동 모드":
            ensure_target_file_controller_executed()
        else:
            import logging
            logging.info("재생 모드 선택이 취소되었습니다. 프로그램을 종료합니다.")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
        # ensure_pk_wrapper_starter_suicided(__file__)
