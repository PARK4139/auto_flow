def ensure_elapsed_time_logged(start_time, log_file_path=None):
    from pk_internal_tools.pk_functions.print_and_save_log_to_file import print_and_save_log_to_file
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    import time
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    import inspect
    from pk_internal_tools.pk_objects.pk_directories import D_DESKTOP

    if log_file_path is None:
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        log_file_default = f"{D_DESKTOP}/result_of_{func_n}.txt"
        log_file_path = log_file_default
    duration = time.time() - start_time
    elapsed_time = rf"{duration:.2f}"
    msg = f"{PkColors.YELLOW}ENDED AT : {duration:.2f} {PkTexts.SECONDS} {PkColors.RESET}"
    print_and_save_log_to_file(msg, log_file_path)

    # pk_option
    # print_marker_and_stop()

    # pk_option
    # ensure_pk_exit_silent()
    return elapsed_time
