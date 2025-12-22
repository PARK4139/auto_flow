from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


def handle_losslesscut_loading(window_title, time_limit, with_key_handing=True):
    import time
    if is_window_opened_via_window_title(window_title=window_title):
        time_s = time.time()
        while time.time() - time_s <= time_limit:  # 깔끔한 시간제한루프 예시
            f_loading_nx = get_f_loading_nx_by_pattern(pattern=r"_f_ 불러오는 중 - (.+?) - LosslessCut")
            if is_window_opened_via_window_title(window_title=rf"_f_ 불러오는 중 - {f_loading_nx} - LosslessCut"):
                ensure_pressed("esc")
                ensure_slept(milliseconds=300)
                ensure_pressed("space")
                break
            ensure_window_to_front(window_title)
            # todo : 재생여부가 playing 이 아니면 재생하도록 하고 싶은데 CPU 점유율로는 재생여부를 알 수 가 없네.
    logging.debug(rf"handle_losslesscut_loading {window_title} ... ")
