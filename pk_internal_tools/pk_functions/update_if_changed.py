import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def update_if_changed(prev_cnt):
    d_working = get_d_working()
    import os
    current_cnt = len(os.listdir(d_working))
    delta_cnt = current_cnt - prev_cnt
    if delta_cnt != 0:
        logging.debug(f"f_cnt is not stable → update list ({prev_cnt}->{current_cnt}({delta_cnt}))")
        return True, current_cnt
    logging.debug(f"f_cnt is stable")
    return False, prev_cnt
