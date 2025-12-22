
import threading
import pandas as pd
import os.path
import keyboard
import inspect
import colorama
from selenium.webdriver.common.action_chains import ActionChains
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title

from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from PIL import Image
from passlib.context import CryptContext
from os import path
from enum import Enum
from dataclasses import dataclass
from Cryptodome.Cipher import AES
from collections import Counter
from pathlib import Path



from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def send_d_to_remote_os(d_local_src, d_remote_dst, **remote_device_target_config):
    import inspect
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

    import logging

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os import ensure_command_to_remote_target
    from pk_internal_tools.pk_functions.get_wsl_distro_port import get_wsl_distro_port
    from pk_internal_tools.pk_functions.ensure_dockerfile_writen import ensure_dockerfile_writen
    from pk_internal_tools.pk_functions.ensure_remote_os_as_nopasswd import ensure_remote_os_as_nopasswd
    from pk_internal_tools.pk_functions.ensure_ssh_public_key_to_remote_os import ensure_ssh_public_key_to_remote_os
    from pk_internal_tools.pk_functions.ensure_wsl_distro_enabled import ensure_wsl_distro_enabled
    from pk_internal_tools.pk_functions.ensure_wsl_distro_session import ensure_wsl_distro_session
    from pk_internal_tools.pk_functions.get_n import get_n
    from pk_internal_tools.pk_functions.get_wsl_distro_names_installed import get_wsl_distro_names_installed
    from pk_internal_tools.pk_functions.get_wsl_ip import get_wsl_ip
    from pk_internal_tools.pk_functions.get_wsl_pw import get_wsl_pw
    from pk_internal_tools.pk_functions.get_wsl_user_n import get_wsl_user_n
    from pk_internal_tools.pk_objects.pk_directories import D_PK_FASTAPI, D_PK_ROOT, D_USERPROFILE
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import os


    import shutil

    import os
    import paramiko

    ip = remote_device_target_config['ip']
    pw = remote_device_target_config['pw']
    port = remote_device_target_config['port']
    user_n = remote_device_target_config['user_n']
    local_ssh_public_key = remote_device_target_config['local_ssh_public_key']

    ssh = None
    sftp = None
    f_zip_local = None
    try:
        # compress from d_local to f_zip_local
        f_zip_nx = os.path.basename(d_local_src) + ".zip"
        f_zip_local = os.path.join(os.path.dirname(d_local_src), f_zip_nx)
        f_zip_local = Path(f_zip_local)
        shutil.make_archive(base_name=f_zip_local.replace(".zip", ""), format="zip", root_dir=d_local_src)
        if f_zip_local.exists():
            logging.debug(f"compress d from d_local to f_zip_local({f_zip_local})")

        f_zip_remote = os.path.join(d_remote_dst, f_zip_nx).replace("\\", "/")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=port, username=user_n, password=pw)
        sftp = ssh.open_sftp()

        # send d as f_zip
        logging.debug(f"start to send d as f_zip from {f_zip_local} to {f_zip_remote}")
        sftp.put(f_zip_local, f_zip_remote)
        logging.debug(f"send d as f_zip from {f_zip_local} to {f_zip_remote}")

        # decompress in remote
        cmd = f"unzip -o {f_zip_remote} -d {d_remote_dst}"
        stdin, stdout, stderr = ssh.exec_command(cmd)  # 이 방식.

        # ensure d existance
        # todo

    except Exception as e:
        print(f"Error during directory transfer: {e}")
        raise
    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
        # 잔여 pnx 삭제
        if os.path.exists(f_zip_local):
            os.remove(f_zip_local)
        if QC_MODE:
            logging.debug("SSH connection closed.")
