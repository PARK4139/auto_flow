def get_text_dragged():
    import logging

    import clipboard

    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_text_from_clipboard import get_text_from_clipboard
    clipboard_current_contents = get_text_from_clipboard()
    while 1:
        ensure_pressed("ctrl", "c")
        ensure_slept(milliseconds=15)
        text_dragged = get_text_from_clipboard()
        logging.debug(f'text_dragged={text_dragged}')
        if clipboard_current_contents != text_dragged:
            break
    clipboard.copy(clipboard_current_contents)
    return text_dragged
