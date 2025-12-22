from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def open_and_move_wsl_console_to_front(distro_name, window_title_seg):
    import time

    ensure_wsl_distro_session(distro_name)

    cmd = f'start cmd /k "wsl -d {distro_name}"'
    ensure_command_executed(cmd=cmd, mode='a')
    time_limit = 20
    time_s = time.time()
    while 1:
        # logging.debug(time.time() - time_s)
        if time.time() - time_s > time_limit:
            break
        if is_window_opened(window_title_seg=window_title_seg):
            break
        ensure_slept(seconds=0.5)

    time_limit = 5
    time_s = time.time()
    while 1:
        # logging.debug(time.time() - time_s)
        if time.time() - time_s > time_limit:
            break
        if ensure_window_to_front(window_title_seg):
            break
        else:
            ensure_window_to_front(window_title_seg)
        ensure_slept(seconds=0.5)
        break

    # cd

    # clear
