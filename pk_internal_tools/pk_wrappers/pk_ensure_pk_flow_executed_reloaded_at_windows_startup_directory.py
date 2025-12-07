if __name__ == '__main__':
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    import logging
    from pk_internal_tools.pk_functions.ensure_pk_flow_executed_reloaded_at_windows_startup_directory import ensure_pk_flow_executed_reloaded_at_windows_startup_directory
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    try:
        # 로깅 설정 초기화
        ensure_pk_log_initialized(__file__)
        ensure_pk_colorama_initialized_once()
        ensure_window_title_replaced(get_nx(__file__))


        ensure_pk_flow_executed_reloaded_at_windows_startup_directory()
        # ensure_command_executed(cmd=rf"{D_HOME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\pk_startup.lnk")
        # ensure_windows_deduplicated_once_all()


    except Exception as e:
        logging.debug(f"❌ 오류가 발생했습니다: {str(e)}")
        traceback.print_exc()
