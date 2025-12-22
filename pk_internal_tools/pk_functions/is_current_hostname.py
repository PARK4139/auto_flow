import yt_dlp

import win32com.client
import webbrowser
import undetected_chromedriver as uc
import tqdm
import tomllib
import time
import subprocess
import string
import speech_recognition as sr
import shlex
import requests
import random
import pyautogui
import platform
import paramiko
import os.path
import importlib
import easyocr
import datetime
import colorama
import calendar

from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f


from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from paramiko import SSHClient, AutoAddPolicy
from mysql.connector import connect, Error
from dirsync import sync
from datetime import timedelta
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from collections import defaultdict, Counter
from base64 import b64encode
from base64 import b64decode

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def is_current_hostname(hostname):
    current_hostname = get_hostname()
    logging.debug(rf'''hostname="{hostname}"  ''')
    logging.debug(rf'''current_hostname="{current_hostname}"  ''')
    if current_hostname == hostname:
        return 1
    else:
        return 0
