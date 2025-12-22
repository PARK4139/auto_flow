from pk_internal_tools.pk_functions.ensure_process_killed_by_window_title import ensure_process_killed_by_window_title
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_potplayer_killed():
    from pk_internal_tools.pk_functions.ensure_process_killed_by_window_title import ensure_process_killed_by_window_title
    from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    for window_title in get_window_titles():
        if " - 팟플레이어" in window_title:
            ensure_process_killed_by_window_title(window_title)
            break
