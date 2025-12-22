# @ensure_seconds_measured
def ensure_debugged_verbose(traceback, e):
    import logging
    import tempfile

    from pk_internal_tools.pk_functions.ensure_str_writen_to_f import ensure_str_writen_to_f
    from pk_internal_tools.pk_functions.print_red import print_red
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_files import F_PK_ERROR_ISOLATED_LOG_LATEST
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext

    from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard

    f_pk_error_isolated_log = None

    # logging.error(f"#e\n{e}")
    logging.warning(f"#pk_error\n{e}")

    if isinstance(traceback, str):
        text_to_display = traceback
    else:
        text_to_display = traceback.format_exc()

    if QC_MODE:
        f_pk_error_isolated_log = F_PK_ERROR_ISOLATED_LOG_LATEST
        ensure_str_writen_to_f(text=text_to_display, f=f_pk_error_isolated_log, mode='w')
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log", mode="w", encoding="utf-8") as tmp_file:
            tmp_file.write(text_to_display)
            f_pk_error_isolated_log = tmp_file.name

    # logging.debug(rf"f_pk_error_isolated_log={f_pk_error_isolated_log}")

    print_red("# pk_traceback\n")
    texts_to_display = text_to_display.split("\n")
    for line in texts_to_display:
        print_red(f'{line}')

    # kill
    # for window in get_windows_opened():  # pk_checkpoint
    #     if get_nx(f_pk_error_isolated_log) in window:
    #         ensure_window_killed_by_title(window_title=window)
    # 이로직이 pycharm 닫음. 닫지 않기위해 주석처리

    # open
    ensure_pnx_opened_by_ext(f_pk_error_isolated_log, logging_mode=False)

    # save error log to clipboard
    ensure_text_saved_to_clipboard(text=text_to_display)
    # logging.info(rf"error log is saved to clipboard.")

    # pk_option
    if QC_MODE:
        ensure_paused()  # pk_option
