import logging
import time


# @ensure_seconds_measured
def ensure_windows_killed_like_human_by_window_title(window_title):
    # ensure_process_killed_by_window_title 보다 나은 느낌은 들었음. 검증필요

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front

    timeout_seconds_limit = 3
    time_s = time.time()
    while True:
        elapsed = time.time() - time_s
        if elapsed > timeout_seconds_limit:
            logging.debug("timeout")
            return False
        if not is_window_opened(window_title_seg=window_title):
            return False
        else:
            ensure_window_to_front(window_title_seg=window_title)
            # ensure_slept(milliseconds=77) # -> succeeded
            ensure_slept(milliseconds=40)  # -> succeeded
            if is_window_title_front(window_title=window_title):
                ensure_pressed("alt", "f4")
                logging.debug(f'{window_title} is tried to close')
            else:
                logging.debug(f'{window_title}이 앞에 있지 않아 창 닫기를 시도하지 않았습니다.')
