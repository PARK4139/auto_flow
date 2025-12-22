
import win32com.client
import traceback
import sqlite3
import socket
import shutil
import pyglet
import pyautogui
import paramiko
import pandas as pd
import keyboard
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pytube import Playlist
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

from passlib.context import CryptContext
from colorama import init as pk_colorama_init
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pathlib import Path
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def is_midnight():
    from datetime import datetime
    now = datetime.now()
    if now.hour == 0 and now.minute == 0 and now.second == 0:
        return 1
    else:
        return 0
