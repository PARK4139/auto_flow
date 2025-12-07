

def get_key_public(**remote_device_target_config):
    import os.path
    local_ssh_public_key = remote_device_target_config['local_ssh_public_key']

    if not os.path.exists(local_ssh_public_key):
        raise FileNotFoundError(f"PUBLIC KEY NOT FOUND AT {local_ssh_public_key}")
    with open(local_ssh_public_key, "r") as f_obj:
        key_public = f_obj.read().strip()
