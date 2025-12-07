from pk_internal_tools.pk_functions.ensure_window_to_front_2025_11_23 import ensure_window_to_front_2025_11_23
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_window_to_front(
        window_title_seg=None, pid=None,
        timeout_ms=500
        # timeout_ms=1000
):
    ensure_window_to_front_2025_11_23(
        window_title_seg=window_title_seg,
        pid=pid,
        timeout_ms=timeout_ms
    )
