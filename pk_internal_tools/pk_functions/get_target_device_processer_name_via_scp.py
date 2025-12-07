

def get_target_processer_name_via_scp (target_device_data_raw):
    remote_device_target_config = {}
    remote_device_target_config['ip'] = target_device_data_raw.target_device_ip
    remote_device_target_config['port'] = target_device_data_raw.target_device_port
    remote_device_target_config['user_n'] = target_device_data_raw.target_device_user_n
    remote_device_target_config['local_ssh_private_key'] = target_device_data_raw.target_device_local_ssh_private_key
    remote_device_target_config['local_ssh_public_key'] = target_device_data_raw.target_device_local_ssh_public_key
    std_outs, std_err_list = ensure_command_to_remote_os(cmd='ifconfig', **remote_device_target_config)
