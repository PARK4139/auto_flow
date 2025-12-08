from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_slept_by_following_history import ensure_slept_by_following_history
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def ensure_edited_code_tested():
    func_n = get_caller_name()
    history_reset = False
    # history_reset = True

    if history_reset:
        ensure_pressed("win", "m")
        ensure_slept(milliseconds=500)

    ensure_pressed("win", "1")
    ensure_slept_by_following_history(key_name="pk_system cli 실행대기", history_reset=history_reset, func_n=func_n)
    ensure_console_paused()
    ensure_pressed("enter")

