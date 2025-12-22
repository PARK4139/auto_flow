






from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style


def ensure_pnx_moved_from_remote_os_to_local(pnx, d_dst=None, **remote_device_target_config):
    # todo

    pnx = get_pnx_unix_style(pnx)
    ip = remote_device_target_config['ip']
    port = remote_device_target_config['port']
    user_n = remote_device_target_config['user_n']
    d_dst = d_dst or D_DOWNLOADS
    d_dst = get_pnx_unix_style(d_dst)
    ensure_command_executed(cmd=f'scp -P {port} -r {user_n}@{ip}:"{pnx}" "{d_dst}"')
    ensure_slept(milliseconds=500)
