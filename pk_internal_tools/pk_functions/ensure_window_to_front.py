import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title


@ensure_seconds_measured
def ensure_window_to_front(
        window_title_seg=None, pid=None,
        timeout_ms=500
        # timeout_ms=1000
):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
    from pk_internal_tools.pk_functions.move_window_to_front_via_window_title_seg import move_window_to_front_via_window_title_seg

    while 1:
        if not is_window_opened_via_window_title(window_title=window_title_seg):
            logging.warning(f'{window_title_seg} is not opened among windows, can not move to front')
            return
        if is_window_title_front(window_title=window_title_seg):
            logging.info(f'already, {window_title_seg} is front among windows')
            return
        else:
            move_window_to_front_via_window_title_seg(
                window_title_seg=window_title_seg,
                pid=pid,
                timeout_ms=timeout_ms
            )
        if QC_MODE:
            # ensure_slept(milliseconds=22)
            ensure_slept(milliseconds=500)
        else:
            ensure_slept(milliseconds=500)
