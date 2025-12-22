import winreg

import win32con
import undetected_chromedriver as uc
import traceback
import time
import sys
import speech_recognition as sr
import shutil
import pythoncom
import pygetwindow
import platform
import pandas as pd
import numpy as np
import nest_asyncio
import mutagen
import math
import importlib
import hashlib
import functools
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from tkinter import UNDERLINE
from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from queue import Queue, Empty
from pynput import mouse
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


from PIL import Image
from paramiko import SSHClient, AutoAddPolicy
from os import path
from mutagen.mp3 import MP3
from gtts import gTTS
from functools import partial as functools_partial
from functools import lru_cache
from datetime import timedelta
from datetime import date
from cryptography.hazmat.backends import default_backend
from collections import defaultdict, Counter
from base64 import b64encode
from base64 import b64decode

# 
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def get_age_biological(birth_day):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # 2023-1994=29(생일후)
    # 2024-1994=30(생일후)
    # 만나이 == 생물학적나이
    # 생일 전 만나이
    # 생일 후 만나이
    pass
