
import win32con
import win32com.client
import tqdm
import toml
import socket
import shlex
import pywintypes

import pythoncom
import platform
import os.path
import mutagen
import easyocr
import datetime
import asyncio
from seleniumbase import Driver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from passlib.context import CryptContext
from os import path
from dataclasses import dataclass
from base64 import b64encode

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def install_chrome_remote_desktop_server_to_remote_os(users, ip, distro_name, wsl_window_title_seg, pw,
                                                      exit_mode):
    # ssh_in_wsl(users=users, ip=ip, distro_name=distro_name, wsl_window_title_seg=wsl_window_title_seg, pw=pw, exit_mode=exit_mode)
    #
    # # Update package list
    # cmd_to_wsl_os_like_human('sudo apt update')
    #
    # # Install wget
    # cmd_to_wsl_os_like_human('sudo apt install wget')
    #
    # # Download Google Chrome .deb package
    # cmd_to_wsl_os_like_human('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
    #
    # # Install Google Chrome
    # cmd_to_wsl_os_like_human('sudo apt install ./google-chrome-stable_current_amd64.deb')
    pass
