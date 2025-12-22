from pathlib import Path


def download_pnx_from_remote_os(f_remote_src, f_local_dst, **remote_device_target_config):
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os import ensure_command_to_remote_target

    f_local_dst = Path(f_local_dst)
    user = remote_device_target_config['user']
    ip = remote_device_target_config['ip']
    port = remote_device_target_config['port']
    ensure_command_to_remote_target(cmd=rf"scp -P {port} -r {user}@{ip}:{f_remote_src} {f_local_dst}", **remote_device_target_config)
