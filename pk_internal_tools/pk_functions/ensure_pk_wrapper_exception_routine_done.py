def ensure_pk_wrapper_exception_routine_done(*, traced_file, traceback, e):
    from pk_internal_tools.pk_functions.ensure_pk_system_log_editable import ensure_pk_system_log_editable
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
    from pk_internal_tools.pk_functions.get_text_red import get_text_red
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

    PK_UNDERLINE = get_text_red(PK_UNDERLINE)

    # log error cause
    logging.debug(PK_UNDERLINE)
    ensure_debugged_verbose(traceback, e)  # logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

    if QC_MODE:
        ensure_pk_system_log_editable()
    # ensure_pk_wrapper_starter_suicided(__file__)
