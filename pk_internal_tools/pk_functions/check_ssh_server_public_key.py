def check_ssh_server_public_key(key_public, **remote_device_target_config):
    import logging

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import paramiko

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ip = remote_device_target_config['ip']
    port = remote_device_target_config['port']
    user_n = remote_device_target_config['user_n']
    pw = remote_device_target_config['pw']

    try:
        ssh.connect(hostname=ip, port=port, username=user_n, password=pw)

        cmd = f'grep -qxF "{key_public}" ~/.ssh/authorized_keys && echo "Key exists" || echo "Key not found"'
        stdin, stdout, stderr = ssh.exec_command(cmd)
        std_out_str = stdout.read().decode().strip()
        signature = "Key exists"
        if signature == std_out_str:
            logging.debug("PUBLIC KEY IS ALREADY REGISTERED ON THE REMOTE SERVER.")
            return 1
        else:
            logging.debug("PUBLIC KEY IS NOT REGISTERED ON THE REMOTE SERVER.")
            return 0

    except Exception as e:
        logging.debug(f"{"[ ERROR ]"} {e}")
        raise
    finally:
        ssh.close()
        if QC_MODE:
            logging.debug(rf"SSH connection closed.")
