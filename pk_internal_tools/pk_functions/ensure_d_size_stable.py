from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

import logging


def ensure_d_size_stable(d_working, limit_seconds):
    """_d_ 크기와 f 개수가 일정한지 확인"""

    import time
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    prev_size, prev_count = get_d_size_and_f_cnt(d_working)

    time_s = time.time()
    pk_context_state = SpeedControlContext()

    logging.debug(f'''started at {time_s} for {limit_seconds} seconds stable monitoring''')
    while 1:
        ensure_slept(milliseconds=pk_context_state.milliseconds_for_speed_control)
        cur_size, cur_count = get_d_size_and_f_cnt(d_working)  # 현재 크기 및 f 개수 확인
        set_pk_context_state((cur_size, cur_count), pk_context_state)  # 상태 변화 감지

        logging.debug(f'''d size: {cur_size}, f cnt: {cur_count}, pk_state.milliseconds_for_speed_control={pk_context_state.milliseconds_for_speed_control} ''')

        # _d_ 크기나 f 개수가 변경되면 즉시 0 반환
        if cur_size != prev_size or cur_count != prev_count:
            if QC_MODE:
                logging.debug(f"d size stable = 0")
            return 0
        time_e = time.time()
        time_delta = time_e - time_s
        if limit_seconds < time_delta:
            if QC_MODE:
                logging.debug(f"d size stable = 1")
            logging.debug(f'''ensured d size is stable for {limit_seconds} seconds''')
            return 1  # 일정 시간 동안 변화가 없으면 안정적이라고 판단
