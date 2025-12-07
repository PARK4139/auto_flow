from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_case_debugger_executed(case_id, case_data, case_debugging_mode=False):
    import logging
    import traceback
    from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow

    from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

    try:
        if case_debugging_mode:
            logging.warning(get_text_yellow(rf"case_data={case_data}"))
            ensure_console_paused(text=get_text_yellow(case_id))
            # ensure_spoken(text=case_id)
            # logging.debug(get_text_yellow(case_id))
        else:
            logging.info(case_id)
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
