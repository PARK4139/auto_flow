from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensrue_debug_clipboard_state():
    # code for fixing 클립보드 삭제 이슈
    import logging
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.get_clipboard_text import get_clipboard_text
    from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
    ensure_pk_system_log_initialized(__file__)
    logging.debug(get_clipboard_text())
    logging.debug(f'''get_clipboard_text()={get_clipboard_text()} ''')
    import sys
    sys.exit()
