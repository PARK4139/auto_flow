import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
from pk_internal_tools.pk_functions.move_window_to_front import move_window_to_front


def ensure_window_titles_moved_to_front_like_person():
    func_n = get_caller_name()
    try:
        windows_opened = get_windows_opened()
        windows_to_move = ensure_values_completed(
            key_name="windows_to_move",
            func_n=func_n,
            options=windows_opened,  # Use the filtered list
            history_reset=True,
        )
        if windows_to_move:
            if not isinstance(windows_to_move, list):
                windows_to_move = [windows_to_move]
            for window_title in windows_to_move:
                move_window_to_front(window_title=window_title)
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
