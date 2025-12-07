



from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
import logging
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def ensure_pnx_moved_to_remote_os(pnx, dst='~/Downloads', **remote_device_target_config):
    ensure_ssh_public_key_to_remote_os(**remote_device_target_config)

    ip = remote_device_target_config['ip']
    pw = remote_device_target_config['pw']
    port = remote_device_target_config['port']
    user_n = remote_device_target_config['user_n']

    if not is_pnx_existing(pnx=pnx):
        logging.debug(f'''does not exist pnx to send ''')
        return

    pnx = get_pnx_unix_style(pnx)
    dst = get_pnx_unix_style(dst)
    cmd = f'scp -P {port} -r "{pnx}" {user_n}@{ip}:{dst}'
    # cmd = f'rsync -avz -e "ssh -p {port}" "{src}" {users}@{ip}:{dst}' # windows 환경에는 rsync 없이 가능해야한다... wsl 설치하고 지우면...?너무 비효율적인가?

    ensure_command_executed(cmd=cmd)  # warning : pw 물은 채로 정지
    window_title_seg = r"C:\Windows\system32\cmd"
    # ensure_slept(milliseconds=2000) # success : but late
    # ensure_slept(milliseconds=1000) # success : but late
    ensure_slept(milliseconds=500)
    while 1:
        if is_window_opened(window_title_seg=window_title_seg):
            ensure_window_to_front(window_title_seg)
            # ensure_slept(milliseconds=500)  # success : but late
            # ensure_slept(milliseconds=200)
            ensure_slept(milliseconds=100)
            ensure_writen_like_human(text_working=pw)
            ensure_slept(milliseconds=100)
            ensure_pressed("enter")
            break
    ensure_slept(milliseconds=500)
