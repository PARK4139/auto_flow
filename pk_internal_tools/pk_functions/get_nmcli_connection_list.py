def get_nmcli_connection_list(**remote_device_target_config):
    std_outs, std_err_list = ensure_command_to_remote_os(cmd=f'nmcli connection show', **remote_device_target_config)
    # std_outs, std_err_list = ensure_command_to_remote_os(cmd=f'nmcli device status',**remote_device_target_config)
    return std_outs, std_err_list
