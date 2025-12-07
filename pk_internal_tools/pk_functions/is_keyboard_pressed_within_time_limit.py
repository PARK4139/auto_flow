

import logging


def is_keyboard_pressed_within_time_limit(key_plus_key: str, time_limit):
    import inspect
    import time
    import keyboard

    # time_limit 이 아니라 트리거로 ESC 눌렸을 때 종료되도록 하는 함수가 더 유용하겠다.
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    time_s = time.time()
    keys = key_plus_key.split("+")
    waiting_limit = 30
    while 1:
        if all(keyboard.is_pressed(key) for key in keys):
            # 단축키 조합이 모두 눌렸을 때 exec 할 코드
            logging.debug(f"{keys[0]}+{keys[1]}")
            return 1
        else:
            logging.debug(f"{key_plus_key} 눌릴때까지 기다리고 있습니다")
            time_e = time.time()
            time_diff = time_e - time_s
            if time_diff == time_limit:
                return 0
            ensure_slept(milliseconds=waiting_limit)
