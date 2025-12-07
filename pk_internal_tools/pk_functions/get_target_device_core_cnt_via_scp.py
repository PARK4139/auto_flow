import zipfile
import yt_dlp
import urllib
import undetected_chromedriver as uc
import time
import socket
import shutil

# import pyaudio
# import pandas as pd
import mysql.connector
import mutagen
import asyncio
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PySide6.QtWidgets import QApplication
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from os.path import dirname
from bs4 import BeautifulSoup
from base64 import b64decode

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def get_target_core_cnt_via_scp (target_device_data_raw):
    remote_device_target_config = {}
    remote_device_target_config['ip'] = target_device_data_raw.target_device_ip
    remote_device_target_config['port'] = target_device_data_raw.target_device_port
    remote_device_target_config['user_n'] = target_device_data_raw.target_device_user_n
    remote_device_target_config['local_ssh_private_key'] = target_device_data_raw.target_device_local_ssh_private_key
    remote_device_target_config['local_ssh_public_key'] = target_device_data_raw.target_device_local_ssh_public_key
    std_outs, std_err_list = ensure_command_to_remote_os(cmd='ifconfig', **remote_device_target_config)
