def get_remote_tree(d_path, **remote_device_target_config):
    ip = remote_device_target_config['ip']
    user_n = remote_device_target_config['user_n']
    pw = remote_device_target_config['pw']

    from paramiko import SSHClient, AutoAddPolicy
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(hostname=ip, username=user_n, password=pw)

    cmd = f"find {d_path}"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    tree_output = stdout.read().decode()
    ssh.close()
    return tree_output
