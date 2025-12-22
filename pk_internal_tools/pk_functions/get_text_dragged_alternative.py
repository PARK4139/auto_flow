from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_text_dragged_alternative():
    from pk_internal_tools.pk_functions.get_text_from_clipboard import get_text_from_clipboard
    import logging

    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed

    import clipboard
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    clipboard_current_contents = get_text_from_clipboard()
    ensure_pressed("ctrl", "c")
    text_dragged = get_text_from_clipboard()
    logging.debug(rf'''text_dragged="{text_dragged}"  ''')
    clipboard.copy(clipboard_current_contents)

    return text_dragged
