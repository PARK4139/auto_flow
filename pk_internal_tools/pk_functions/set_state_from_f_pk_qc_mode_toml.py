import zlib
import yt_dlp

import win32con
import uuid
import urllib.parse
import urllib
import undetected_chromedriver as uc
import toml
import threading
import tarfile
import sys
import subprocess, time
import string


import pythoncom
import pygetwindow
import pyautogui
# import pyaudio
# import pandas as pd
import os
import nest_asyncio
import mysql.connector
import mutagen
import math
import keyboard
import easyocr
import clipboard
from zipfile import BadZipFile
from urllib.parse import urlparse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.ensure_state_printed import ensure_state_printed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts



from passlib.context import CryptContext
from functools import partial
from enum import Enum
from cryptography.hazmat.primitives import padding
from pathlib import Path
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def set_state_from_f_pk_qc_mode_toml(pk_state_address, pk_state_value):
    pk_toml_address_list = pk_state_address.split('/')
    if QC_MODE:
        logging.debug(f'''pk_state_address={pk_state_address} ''')
        logging.debug(f'''pk_state_value={pk_state_value} ''')
    level_1_dict_n = ""
    level_2_dict_n = ""
    level_3_dict_n = ""
    try:
        level_1_dict_n = pk_toml_address_list[0]
        level_2_dict_n = pk_toml_address_list[1]
        level_3_dict_n = pk_toml_address_list[2]
    except Exception as e:
        if QC_MODE:
            logging.debug(f'''{len(pk_toml_address_list)} is idx limit. in setter ''')

    level_1_dict = {}
    level_2_dict = {}
    level_3_dict = {}
    try:
        level_1_dict = toml.load(F_QC_MODE_TOML)[level_1_dict_n]
    except KeyError:
        logging.debug(f'''level_1_dict={level_1_dict}에 해당하는 key 가 없어 생성합니다. ''')
        level_1_dict = toml.load(F_QC_MODE_TOML)[level_1_dict]
        with open(F_QC_MODE_TOML, "w") as f:
            toml.dump(level_1_dict, f)
    try:
        level_2_dict = level_1_dict[level_2_dict_n]
    except KeyError:
        logging.debug(f'''level_2_dict_n={level_2_dict_n}에 해당하는 key 가 없어 생성합니다. ''')
        level_1_dict[level_2_dict_n] = pk_state_value
        with open(F_QC_MODE_TOML, "w") as f:
            toml.dump(level_1_dict, f)
    if len(pk_toml_address_list) == 2:
        level_1_dict[level_2_dict_n] = pk_state_value
        with open(F_QC_MODE_TOML, "w") as f:
            toml.dump(level_1_dict, f)
    try:
        level_3_dict = level_2_dict[level_3_dict_n]
    except KeyError:
        logging.debug(f'''level_3_dict_n={level_3_dict_n}에 해당하는 key 가 없어 생성합니다. ''')
        level_2_dict[level_3_dict_n] = pk_state_value
        with open(F_QC_MODE_TOML, "w") as f:
            toml.dump(level_2_dict, f)
    if len(pk_toml_address_list) == 3:
        level_2_dict[level_3_dict_n] = pk_state_value
        with open(F_QC_MODE_TOML, "w") as f:
            toml.dump(level_2_dict, f)
