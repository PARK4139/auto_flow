from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def print_and_save_log_to_file(msg, log_file_path):
    import logging
    import logging

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_str_writen_to_f import ensure_str_writen_to_f
    logging.debug(msg)
    ensure_pnx_made(pnx=log_file_path, mode="f")
    ensure_str_writen_to_f(text=msg, f=log_file_path, mode="w")  # 내용 초기화


