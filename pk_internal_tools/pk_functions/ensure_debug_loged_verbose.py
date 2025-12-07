# @ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
import traceback


def ensure_debug_loged_verbose(exception_info):
    import logging
    import tempfile

    from pk_internal_tools.pk_functions.ensure_str_writen_to_f import ensure_str_writen_to_f
    from pk_internal_tools.pk_functions.ensure_window_killed_by_title import ensure_window_killed_by_title
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
    from pk_internal_tools.pk_functions.print_red import print_red
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_files import F_pk_ERROR_ISOLATED_LOG_LATEST
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext

    error_isolated_temp_log_file = None

    if isinstance(exception_info, str):
        text_to_print_raw = exception_info
    else:
        text_to_print_raw = traceback.format_exc()

    if QC_MODE:
        error_isolated_temp_log_file = F_pk_ERROR_ISOLATED_LOG_LATEST
        ensure_str_writen_to_f(text=text_to_print_raw, f=error_isolated_temp_log_file, mode='w')
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log", mode="w", encoding="utf-8") as tmp_file:
            tmp_file.write(text_to_print_raw)
            error_isolated_temp_log_file = tmp_file.name
    logging.debug(rf"error_isolated_temp_log_file={error_isolated_temp_log_file}")

    # console print
    traceback_format_exc_list = text_to_print_raw.split("\n")
    print_red("# pk_traceback\n")
    for line in traceback_format_exc_list:
        print_red(f'{line}')
    # text_to_print = get_text_red(text_to_print_raw)
    # logging.debug(text_to_print)

    # open
    for window in get_windows_opened():  # pk_checkpoint
        if get_nx(error_isolated_temp_log_file) in window:
            ensure_window_killed_by_title(window_title=window)

    ensure_pnx_opened_by_ext(error_isolated_temp_log_file)

    ensure_text_saved_to_clipboard(text=text_to_print_raw)
    logging.info(rf"error log is saved to clipboard.")

