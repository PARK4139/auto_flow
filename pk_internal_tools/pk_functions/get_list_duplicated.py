


import win32con
import uuid
import tqdm
import tomllib
import time
import tarfile
import string
import shlex
import random


import pyautogui
import psutil
import pickle
import os.path
import nest_asyncio
import keyboard
import inspect
import easyocr
import cv2
import colorama
import clipboard
import chardet
import asyncio
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from pytube import Playlist
from pynput import mouse
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from passlib.context import CryptContext
from os import path
from moviepy import VideoFileClip
from functools import lru_cache
from dirsync import sync
from datetime import datetime, timedelta
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from collections import Counter
from bs4 import BeautifulSoup
from base64 import b64encode
from base64 import b64decode
# 
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


import logging


def get_list_duplicated(working_list):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    items_duplicated = []
    seen = set()  # 이미 본 요소를 추적할 집합
    for item in working_list:
        if item in seen and item not in items_duplicated:
            items_duplicated.append(item)
        else:
            seen.add(item)
    return items_duplicated
