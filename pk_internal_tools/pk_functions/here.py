import zlib
import win32com.client
import webbrowser
import undetected_chromedriver as uc
import traceback
import toml
import pyautogui
import numpy as np
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.performance_logic import ensure_seconds_measured, pk_measure_memory


from pathlib import Path
from os.path import dirname
from mutagen.mp3 import MP3
from gtts import gTTS
from enum import Enum

from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

import logging


def here(item_str=None):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if item_str is None:
        item_str = ''
    logging.debug(rf"{str(str(item_str) + ' ') * 242:.100} here!")
