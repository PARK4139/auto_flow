

def ensure_remote_os_connection(**remote_device_target_config):
    ip = remote_device_target_config['ip']
    while 1:
        if not ensure_pinged(ip=ip):
            todo('%%%FOO%%%')
            continue
        if ensure_pinged(ip=ip):
            break
