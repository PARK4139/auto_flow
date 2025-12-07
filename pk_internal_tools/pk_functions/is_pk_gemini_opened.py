from pk_internal_tools.pk_functions.get_gemini_prompt_interface_title import get_pk_gemini_title
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def is_pk_gemini_opened(local_gemini_root=None):
    from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
    import logging
    window_title = get_pk_gemini_title(local_gemini_root)
    if is_window_opened_via_window_title(window_title):
        logging.debug(f'gemini interface is already opened')
        return True
    logging.debug(f'gemini interface is not opened')
    return False
