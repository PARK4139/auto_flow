def set_remote_os_as_nopasswd_v1(**remote_device_target_config):
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os_with_pw_via_paramiko import ensure_command_to_remote_os_with_pw_via_paramiko
    from pk_internal_tools.pk_functions.get_str_from_list import get_str_from_list
    import logging

    pw = remote_device_target_config['pw']
    cmd = "sudo grep -n 'nvidia ALL=(ALL:ALL) NOPASSWD:ALL' /etc/sudoers"
    std_outs, std_err_list = ensure_command_to_remote_os_with_pw_via_paramiko(cmd=cmd, **remote_device_target_config)
    std_out = get_str_from_list(std_outs)
    if "nvidia ALL=(ALL:ALL) NOPASSWD:ALL" in std_out:
        logging.debug("The entry is already present.", 'green')
    else:
        cmd = f"echo '{pw}' | sudo -S bash -c \"echo 'nvidia ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers\""
        std_outs, std_err_list = ensure_command_to_remote_os_with_pw_via_paramiko(cmd=cmd, **remote_device_target_config)
        cmd = f"sudo visudo -c"
        std_outs, std_err_list = ensure_command_to_remote_os_with_pw_via_paramiko(cmd=cmd, **remote_device_target_config)
