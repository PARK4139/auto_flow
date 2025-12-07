import logging

from pk_internal_tools.pk_functions.add_public_key_to_remote_via_paramiko import add_public_key_to_remote_via_paramiko
from pk_internal_tools.pk_functions.check_ssh_server_public_key import check_ssh_server_public_key
from pk_internal_tools.pk_functions.get_key_public import get_key_public
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_ssh_public_key_to_remote_os(**remote_device_target_config):
    import paramiko

    ip = remote_device_target_config['ip']
    port = remote_device_target_config['port']
    user_n = remote_device_target_config['user_n']
    pw = remote_device_target_config['pw']

    key_public = get_key_public(**remote_device_target_config)
    if check_ssh_server_public_key(key_public=key_public, **remote_device_target_config):
        logging.debug("SSH PUBLIC KEY IS ALREADY REGISTERED")
        return
    else:
        logging.debug("SSH PUBLIC KEY IS NOT REGISTERED")

    # Paramiko로 SSH 연결
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, port=port, username=user_n, password=pw)
        logging.debug(f"{'{PkTexts.TRY_GUIDE}'} ssh -p {port} {user_n}@{ip} ")

        add_public_key_to_remote_via_paramiko(ssh_paramiko=ssh, key_public=key_public)

    except paramiko.AuthenticationException as e:
        logging.debug(f"Authentication failed. Please check your user_n and password: {e}")
        raise
    except paramiko.SSHException as e:
        logging.debug(f"SSH connection error: {e}")
        raise
    except Exception as e:
        logging.debug(f"An unexpected error occurred: {e}")
        raise
    finally:
        ssh.close()
        if QC_MODE:
            logging.debug("SSH connection closed.")
