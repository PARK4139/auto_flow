from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_local_ssh_public_key_content_created(f_local_ssh_private_key, f_local_ssh_public_key):
    import logging

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    if not f_local_ssh_private_key.exists() or not f_local_ssh_public_key.exists():
        logging.debug(f"SSH key pair not found. Generating new key pair at {f_local_ssh_private_key}...")
        keygen_cmd = f'ssh-keygen -t ed25519 -f "{f_local_ssh_private_key}" -N ""'
        keygen_outs, keygen_errs = ensure_command_executed(keygen_cmd)
        if keygen_errs:
            logging.error(f"Failed to generate SSH key pair: {keygen_errs}")
            raise RuntimeError("Failed to generate SSH key pair.")
        logging.debug("SSH key pair generated successfully.")
    else:
        logging.debug("SSH key pair already exists.")
    try:
        with open(f_local_ssh_public_key, 'r') as f:
            local_ssh_public_key_content = f.read().strip()
        logging.debug(f"Read public key content from {f_local_ssh_public_key}.")
    except Exception as e:
        logging.error(f"Failed to read public key from {f_local_ssh_public_key}: {e}")
        return None
    return local_ssh_public_key_content
