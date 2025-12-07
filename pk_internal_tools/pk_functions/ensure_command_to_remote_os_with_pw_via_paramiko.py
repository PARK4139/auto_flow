import threading
import speech_recognition as sr
import shlex
import pywintypes
import easyocr
from selenium.webdriver.common.keys import Keys
from pytube import Playlist

from functools import partial


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_command_to_remote_os_with_pw_via_paramiko(ip, port, user_n, pw, cmd):
    # todo   remote_device_target_config 를 16 usages 에 적용할것.
    # todo : pw 가 보안적으로 필요한 경우는 이 함수를 쓰자

    import paramiko
    import traceback

    if QC_MODE:
        logging.debug(f"{"[ REMOTE DEBUG ]"} {'{PkTexts.TRY_GUIDE}'} ssh -p {port} {user_n}@{ip} ")
    logging.debug(f"{"[ REMOTE DEBUG ]"} cmd={cmd}")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Connect to the server
        ssh.connect(hostname=ip, port=port, username=user_n, password=pw, timeout=10)
        # logging.debug("{"[ ️ ]"} SSH connection established")

        # Execute the cmd
        stdin, stdout_stream, stderr_stream = ssh.exec_command(cmd)
        std_out_str = stdout_stream.read().decode('utf-8').strip()
        std_err_str = stderr_stream.read().decode('utf-8').strip()

        # Debugging output
        std_outs = get_list_from_str(item_str=std_out_str)
        std_err_list = get_list_from_str(item_str=std_err_str)
        if len(std_outs) > 1:
            for index, item in enumerate(std_outs):
                logging.debug(f"{"[ REMOTE DEBUG ]"} {item}")
        if len(std_err_list) > 1:
            for index, item in enumerate(std_err_list):
                logging.debug(f"{"[ REMOTE ERROR ]"} {item}")

        # Raise an error if there is output in stderr
        if std_err_str:
            logging.debug(f"{"[ REMOTE ERROR ]"} {cmd} : {std_err_str}")

        std_out_str = std_out_str.strip()
        std_err_str = std_err_str.strip()
        return std_out_str, std_err_str
    except:
        logging.debug(f"{"[ REMOTE ERROR ]"} {traceback.format_exc()}   ")
        return std_out_str, traceback.format_exc()
    finally:
        ssh.close()
        if QC_MODE:
            logging.debug(rf"{"[ REMOTE DEBUG ]"} SSH connection closed.")
