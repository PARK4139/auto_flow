

import zlib

import win32con
import webbrowser
import tomllib
import timeit
import tarfile
import requests
import pywintypes
import pygetwindow
import pyautogui
import paramiko
import mysql.connector
import math
import json
import hashlib
import chardet
import calendar
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from passlib.context import CryptContext
from os import path
from functools import lru_cache
from cryptography.hazmat.primitives import padding
from collections import Counter
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_ip_connected_via_http(url):
    import requests
    """Check if an IP is reachable via HTTP."""
    try:
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"  # Default to HTTP
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.debug(f"HTTP connection to {url} failed: {e}")
        return 0
