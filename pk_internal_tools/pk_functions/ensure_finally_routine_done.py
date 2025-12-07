from pk_internal_tools.pk_objects.pk_texts import PkTexts


def ensure_finally_routine_done(*, d_pk_root, traced_file, console_log_block_mode=True):
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_pk_console_log_blocked import ensure_pk_console_log_blocked
    from pk_internal_tools.pk_functions.ensure_spoken import get_pk_spoken_manager
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

    try:
        logging.debug(PK_UNDERLINE)

        if QC_MODE:
            exceptions = [
                "pk_ensure_snipping_tool_exe_opened.py",
                "pk_ensure_pk_scenarios_tested.py",
            ]

            if not any(name in traced_file for name in exceptions):
                # ensure_pk_log_editable() # pk_option
                pass
            # ensure_cursor_enabled()
            # ensure_window_titles_printed()
            # ensure_pycharm_opened()
            pass

        if not QC_MODE:
            script_to_run = rf"{d_pk_root}\.venv\Scripts\activate && python {traced_file} && deactivate"
            logging.debug(PK_UNDERLINE)
            logging.debug(f"'{PkTexts.TRY_GUIDE}' {script_to_run}")
            logging.debug(PK_UNDERLINE)

        get_pk_spoken_manager()._queue.join()  # 완전히 재생될때 까지 # 모든 큐 작업이 완료될 때까지 flow 더 흘러가지 못하도록, 블로킹
        get_pk_spoken_manager().terminate()  # 리소스 해제

        # QC_MODE 모드에서는 console_log_block_mode를 무시하고 로깅을 비활성화하지 않음
        # QC_MODE 모드는 개발/테스트 모드이므로 창이 닫히지 않도록 함
        if console_log_block_mode and not QC_MODE:
            ensure_pk_console_log_blocked("pk_system is successfully worked.")

        # pk_option
        # if QC_MODE:
        #     ensure_pk_log_editable()

        # pk_option : remove useless lines from end of file
        # ensure_pk_log_useless_removed(text=PK_UNDERLINE)

        # pk_option : code for debugging
        # ensure_console_paused()
    except:
        ensure_debug_loged_verbose(traceback)
