import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_update_wait_completed():
    """
        TODO: Write docstring for ensure_gemini_cli_update_wait_completed.
    """
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles

    try:

        gemini_cli_window_title_updating  ="npm install @google/gemini-cli@"

        for window in get_window_titles():
            if gemini_cli_window_title_updating in window:
                break

        is_gemini_cli_update_done = False
        while True:
            if is_gemini_cli_update_done:
                logging.debug(f'gemini cli update completed')
                break
            for window in get_window_titles():
                if gemini_cli_window_title_updating not in window:
                    is_gemini_cli_update_done = True
                    break
            logging.debug(f'gemini cli updating...')
            ensure_slept(milliseconds=1000)

        return True

    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
