import uuid
import tomllib
import tarfile
import sys
import sqlite3
import shutil
import paramiko
import numpy as np
import mutagen
import keyboard
import ipdb
import datetime
from zipfile import BadZipFile
from urllib.parse import urlparse
from selenium.common.exceptions import ElementClickInterceptedException
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from PIL import Image
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style

import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def ensure_docker_env():
    #
    import subprocess

    if not command_exists('docker'):
        logging.debug('Docker missing: installing...')
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker.io'], check=True)
    else:
        logging.debug('Docker exists')
    # 데몬 예외처리
    try:
        subprocess.run(['docker', 'info'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        logging.debug('Docker daemon not running. Attempting to start...')
        # 시스템에 따라 service 또는 systemctl (WSL Ubuntu22.04는 systemctl, 18.04는 service)
        import platform
        start_cmd = ['sudo', 'service', 'docker', 'start']
        try:
            subprocess.run(start_cmd, check=True)
        except Exception as e:
            try:
                subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
            except Exception as e2:
                logging.debug(f'Docker daemon failed to start: {e}\n{e2}')
                raise RuntimeError("Docker daemon could not be started!")
        # 재확인
        try:
            subprocess.run(['docker', 'info'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.debug("Docker daemon started successfully.")
        except subprocess.CalledProcessError:
            logging.debug("Docker daemon is still not running. Please check manually.")
            raise RuntimeError("Docker daemon is not running!")
    return ['docker']
