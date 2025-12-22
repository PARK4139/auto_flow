import zlib
import yt_dlp

import win32con
import tomllib
import toml
import threading
import subprocess
import shutil

import pyautogui
import importlib
import hashlib
import functools
import datetime
import colorama
import colorama
import clipboard
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from tkinter import UNDERLINE
from telegram import Bot
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from pynput import mouse
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext


from PIL import Image, ImageFilter
from functools import partial as functools_partial
from functools import lru_cache
from enum import Enum
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from bs4 import BeautifulSoup
from base64 import b64encode
from base64 import b64decode

from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style



def fix_f_n_weired(working_d, f_nx_from='init_.py', f_nx_to='__init__.py'):
    import os
    """
    주어진 디렉터리 내의 모든 'init_.py' f을 '__init__.py'로 이름 변경합니다.
    """
    for root, d_nx_list, file_nxs in os.walk(working_d):
        for f_nx in file_nxs:
            if f_nx == f_nx_from:
                old_f = os.path.join(root, f_nx)
                new_f = os.path.join(root, f_nx_to)
                try:
                    os.rename(old_f, new_f)
                    print(f"Renamed: {old_f} ->> {new_f}")
                except Exception as e:
                    print(f"Error renaming {old_f}: {e}")
