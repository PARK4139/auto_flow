
import json
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def remmina(users, ip, distro_name, wsl_window_title_seg, pw, exit_mode):
    # todo
    cmd = 'wsl sudo apt update'
    ensure_command_executed(cmd=cmd)

    cmd = 'sudo apt install remmina'
    ensure_command_executed(cmd=cmd)

    cmd_to_wsl_os_like_human(cmd=rf'remmina -c rdp://{users}@{ip}', distro_name=distro_name,
                              wsl_window_title_seg=wsl_window_title_seg)
    pass
