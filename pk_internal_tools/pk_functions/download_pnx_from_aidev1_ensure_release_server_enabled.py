from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging


def download_pnx_from_aidev1_ensure_release_server_ran(remote_f_src, local_d_dst, **config_aidev1_ensure_release_server_ran):
    import paramiko
    import os

    user_n = config_aidev1_ensure_release_server_ran['user_n']
    ip = config_aidev1_ensure_release_server_ran['ip']
    pw = config_aidev1_ensure_release_server_ran['pw']
    port = config_aidev1_ensure_release_server_ran['port']

    # todo 보안고민필요...ssh public key 저장해도 되는지..안되면 로컬에 다운받아 넣는 식으로...보안 트집 잡히지 말고 자동화 수립
    # todo migrate secret txt f to token

    remote_f_src = get_pnx_unix_style(remote_f_src)
    logging.debug(rf'''src="{remote_f_src}"  ''')

    f_dst = rf"{local_d_dst}/{get_nx(remote_f_src)}"
    f_dst = get_pnx_windows_style(f_dst)
    logging.debug(f'''f_dst={f_dst} ''')

    ssh = None
    sftp = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=port, username=user_n, password=pw)

        sftp = ssh.open_sftp()

        d_local = os.path.dirname(f_dst)
        if not os.path.exists(d_local):
            os.makedirs(d_local)

        logging.debug(f"started to download pnx {remote_f_src} to {f_dst}")
        sftp.get(remote_f_src, f_dst)
        logging.debug(f"download pnx {f_dst}")

    except paramiko.AuthenticationException:
        logging.debug("ssh Authentication failed. Please check your user_n and pw.")
        raise
    except Exception as e:
        logging.debug(f"Error: {e}")
        raise
    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
        if QC_MODE:
            logging.debug("SSH connection closed.")
