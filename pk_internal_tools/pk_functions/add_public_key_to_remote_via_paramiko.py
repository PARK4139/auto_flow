def add_public_key_to_remote_via_paramiko(ssh_paramiko, key_public):
    """원격 서버에 공개 키 추가 및 권한 설정"""
    cmd_list = [
        'mkdir -p ~/.ssh',
        'chmod 700 ~/.ssh',
        f'grep -qxF "{key_public}" ~/.ssh/authorized_keys || echo "{key_public}" >> ~/.ssh/authorized_keys',
        'chmod 600 ~/.ssh/authorized_keys'
    ]
    for cmd in cmd_list:
        stdin, stdout, stderr = ssh_paramiko.exec_command(cmd)
        stdout.channel.recv_exit_status()
