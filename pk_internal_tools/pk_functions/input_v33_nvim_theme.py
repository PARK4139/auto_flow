import zlib
import yt_dlp


import win32con
import win32con
import win32com.client
import uuid
import urllib.parse
import undetected_chromedriver as uc
import traceback
import tqdm
import timeit
import tarfile
import subprocess, time
import string
import shutil
import secrets
import requests
import random

import pyglet
import pyautogui
import psutil
import platform
import paramiko
import os.path
import os, inspect
import nest_asyncio
import mysql.connector
import mutagen
import math
import keyboard
import ipdb
import functools
import easyocr
import datetime
import cv2
import colorama
import colorama
import chardet
import calendar

import asyncio
from zipfile import BadZipFile
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from telegram import Bot, Update
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from pytube import Playlist
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front




from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging
import logging

from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared



from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from PIL import Image, ImageFilter
from PIL import Image
from os import path
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial as functools_partial
from functools import partial
from fastapi import HTTPException
from enum import Enum
from dirsync import sync
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from collections import Counter
from base64 import b64encode
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def input_v33_nvim_theme(
        text_working: str,
        limit_seconds: int = 30,
        return_default: str | None = None,
        *,
        masked: bool = False,
        fuzzy_accept: list[tuple[str, ...]] | None = None,
        validator=None,  # Callable[[str], bool]
        vi_mode: bool = True,
        **kwargs
):
    """
    input_v33_nvim_theme 함수를 ensure_value_completed로 대체
    """
    # fuzzy_accept가 있는 경우 해당 값들을 options에 추가
    options = []
    if fuzzy_accept:
        for group in fuzzy_accept:
            options.extend(group)
    
    # return_default가 있는 경우 options에 추가
    if return_default:
        options.append(return_default)
    
    # validator가 있는 경우 기본값만 반환 (validator는 ensure_value_completed에서 지원하지 않음)
    if validator:
        return return_default
    
    # ensure_value_completed 호출
    return ensure_value_completed(key_name=text_working, options=options)
