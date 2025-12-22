def ensure_pk_kiria_executed(is_single_answer_mode: bool = False) -> bool:
    import logging
    import traceback
    from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
    from pk_internal_tools.pk_kiria.pk_kiria import ensure_pk_kiria_executed_continuously, ensure_pk_kiria_executed_single_command
    success = False
    try:
        ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
        if is_single_answer_mode:
            logging.info("pk_kiria 단일 명령 처리 모드로 실행합니다.")
            success = ensure_pk_kiria_executed_single_command()
        else:
            logging.info("pk_kiria 지속 실행 모드로 실행합니다.")
            success = ensure_pk_kiria_executed_continuously()
    except:
        alert_as_gui(text=traceback.format_exc())
    return success
