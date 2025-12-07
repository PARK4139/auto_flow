def ensure_writen_fast(string: str):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person import ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person
    import logging
    ensure_slept(milliseconds=500)
    ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(string)
    logging.debug(rf"{string}")
