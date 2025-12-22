import logging
import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def ensure_window_titles_closed_like_person():
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
    from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
    from pk_internal_tools.pk_functions.move_window_to_front import move_window_to_front

    try:
        window_titles = get_windows_opened()
        if not window_titles:
            logging.info("No windows with titles found.")
            return

        func_n = get_caller_name()
        windows_to_close = ensure_values_completed(
            key_name="windows_to_close",
            func_n=func_n,
            options=window_titles,
            history_reset=True
        )
        if windows_to_close:
            if not isinstance(windows_to_close, list):
                windows_to_close = [windows_to_close]
            for window_title in windows_to_close:
                move_window_to_front(window_title=window_title)
                if is_window_title_front(window_title=window_title):
                    ensure_pressed('alt', "space")
                    ensure_pressed("c")

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
