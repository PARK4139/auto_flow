from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_children_pids_by_window_title import get_children_pids_by_window_title


@ensure_seconds_measured
def get_pids_by_window_title(window_title: str, exact: bool = True):
    # return get_parent_pids_by_window_title()
    return get_children_pids_by_window_title(window_title, exact)
