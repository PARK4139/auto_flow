from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text, wsl_mode=False):
    import logging
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done

    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
    from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.get_str_from_clipboard import get_str_from_clipboard
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    text_bkup = get_str_from_clipboard()
    text_bkup_list = text_bkup.split("\n")
    try:
        # paste for backup
        ensure_iterable_log_as_vertical(item_iterable=text_bkup_list, item_iterable_n="text_bkup_list")

        # copy
        ensure_text_saved_to_clipboard(text=text)
        logging.debug(rf'''text={text}  ''')

        # paste
        if wsl_mode == True:
            ensure_pressed("ctrl", "c")
            ensure_pressed("ctrl", "shift", "v")
        else:
            ensure_pressed("ctrl", "v")
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        # copy for restore
        ensure_text_saved_to_clipboard(text=text_bkup)
