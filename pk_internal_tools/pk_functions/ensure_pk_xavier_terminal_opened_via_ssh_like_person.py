import logging
import time

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_hash import get_hash
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.move_window_to_front_via_window_title_seg import move_window_to_front_via_window_title_seg
from pk_internal_tools.pk_functions.run_cmd_exe import ensure_cmd_exe_executed, _PkModes


def _type_ip_and_user_id(window_title):
    remote_target_ip = ensure_env_var_completed(key_name="pk_xavier_ip")
    remote_target_user_id = ensure_env_var_completed(key_name="pk_xavier_user_id")
    ensure_window_to_front(window_title_seg=window_title)
    ensure_typed(f"ssh {remote_target_user_id}@{remote_target_ip}")
    ensure_slept(milliseconds=111)
    ensure_pressed("enter")
    ensure_slept(milliseconds=111)


def _type_pw(window_title):
    remote_target_pw = ensure_env_var_completed(key_name="pk_xavier_pw")
    ensure_window_to_front(window_title_seg=window_title)
    logging.info(f"remote_target_pw={remote_target_pw}")
    ensure_typed(remote_target_pw)
    logging.info(f"remote_target_pw={remote_target_pw}")
    ensure_slept(milliseconds=111)
    ensure_pressed("enter")


@ensure_seconds_measured
def ensure_pk_xavier_terminal_opened_via_ssh_like_person():
    """
        TODO: Write docstring for ensure_pk_xavier_terminal_opened_via_ssh_like_person.
    """
    try:
        window_title = f"pk_xavier_terminal"
        ensure_cmd_exe_executed(setup_op=_PkModes.CUSTOM_TITLE, custom_title=window_title)

        timeout_seconds_limit = 3
        time_s = time.time()
        while True:
            if time.time() - time_s > timeout_seconds_limit:
                logging.debug("pk_timeout")
                break
            if is_window_title_front(window_title=window_title):
                _type_ip_and_user_id(window_title)
                ensure_slept(milliseconds=1000)
                _type_pw(window_title)
                break
            else:
                move_window_to_front_via_window_title_seg(window_title_seg=window_title)

        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
