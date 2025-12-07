def ensure_exception_routine_done(*, traced_file, traceback, exception=None):
    from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
    import logging
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_functions.get_text_red import get_text_red
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

    PK_UNDERLINE = get_text_red(PK_UNDERLINE)

    # log error cause
    # logging.debug(PK_UNDERLINE)
    # ensure_debug_loged_simple(exception)  # logging.debug(rf"exception={exception}")
    logging.debug(PK_UNDERLINE)
    ensure_debug_loged_verbose(traceback)  # logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

    if QC_MODE:
        ensure_pk_log_editable()
    # ensure_pk_wrapper_starter_suicided(__file__)
