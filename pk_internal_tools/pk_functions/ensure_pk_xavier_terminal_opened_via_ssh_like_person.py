import logging
import time

from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_hash import get_hash
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.run_cmd_exe import ensure_cmd_exe_executed, _SetupOps
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def _type_id(window_title):
    func_n = get_caller_name()
    pk_xavier_ip = ensure_env_var_completed_2025_11_24(key_name="pk_xavier_ip", func_n=func_n)
    pk_xavier_user_id = ensure_env_var_completed_2025_11_24(key_name="pk_xavier_user_id", func_n=func_n)
    ensure_window_to_front(window_title_seg=window_title)
    ensure_typed(f"ssh {pk_xavier_user_id}@{pk_xavier_ip}")
    # ensure_slept(milliseconds=222)
    ensure_slept(milliseconds=111)
    ensure_pressed("enter")
#     ensure_slept(milliseconds=222)
    ensure_slept(milliseconds=111)


def _type_pw(window_title):
    func_n = get_caller_name()
    pk_xavier_pw = ensure_env_var_completed_2025_11_24(key_name="pk_xavier_pw", func_n=func_n)
    ensure_window_to_front(window_title_seg=window_title)
    logging.info(f"pk_xavier_pw={pk_xavier_pw}")
    ensure_typed(pk_xavier_pw)
    logging.info(f"pk_xavier_pw={pk_xavier_pw}")
#     ensure_slept(milliseconds=222)
    ensure_slept(milliseconds=111)
    ensure_pressed("enter")


@ensure_seconds_measured
def ensure_pk_xavier_terminal_opened_via_ssh_like_person():
    """
        TODO: Write docstring for ensure_pk_xavier_terminal_opened_via_ssh_like_person.
    """
    try:
        hash = get_hash("pk_xavier")[0:5]
        window_title = f"[{hash}] pk_xavier"
        ensure_cmd_exe_executed(setup_op=_SetupOps.CUSTOM_TITLE, custom_title=window_title)

        timeout_seconds_limit = 3
        time_s = time.time()
        while True:
            if time.time() - time_s > timeout_seconds_limit:
                logging.debug("timeout")
                break
            if is_window_title_front(window_title=window_title):
                _type_id(window_title)
                # ensure_slept(milliseconds=2222)
                _type_pw(window_title)
                break
            else:
                ensure_window_to_front(window_title_seg=window_title)

        return True
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
