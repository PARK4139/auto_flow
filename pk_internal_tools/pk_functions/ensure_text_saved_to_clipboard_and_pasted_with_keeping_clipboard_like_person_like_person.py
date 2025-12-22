from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text, wsl_mode=False):
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done

    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
    from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.get_str_from_clipboard import get_str_from_clipboard

    text_bkup = get_str_from_clipboard()
    text_bkup_list = text_bkup.split("\n")
    try:
        # paste for backup
        ensure_iterable_data_printed(iterable_data=text_bkup_list, iterable_data_n="text_bkup_list")

        # copy
        ensure_text_saved_to_clipboard(text=text)
        logging.debug(rf'''text={text}  ''')

        # paste
        if wsl_mode:
            ensure_pressed("ctrl", "c")
            ensure_pressed("ctrl", "shift", "v")
        else:
            ensure_pressed("ctrl", "v")
    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_text_saved_to_clipboard(text=text_bkup)
