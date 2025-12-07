import yt_dlp


import win32con
import uuid
import tomllib
import toml
import toml
import timeit
import time
import threading
import sys
import subprocess, time
import sqlite3
import shlex
import requests
import random
import pyglet
import pygetwindow
import pyaudio
import pickle
import paramiko
import mysql.connector
import math
import keyboard
import json
import cv2
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib.parse import quote
from telethon import TelegramClient, events
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical


from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
import logging
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE

from PIL import Image
from os import path
from moviepy import VideoFileClip
from fastapi import HTTPException
from dirsync import sync
from datetime import date
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def copy_pnx_without_overwrite(pnx, dst):
    import os
    import random
    import re
    import shutil
    import traceback

    if not os.path.exists(pnx):
        print(f"소스 경로 '{pnx}'가 존재하지 않습니다.")
        return

    if not os.path.exists(dst):
        ensure_pnx_made(pnx=pnx, mode='d')
    if is_f(pnx):
        shutil.copy2(pnx, dst)
        print(f"f '{pnx}'을(를) '{dst}'로 복사했습니다.")
    elif is_d(pnx):
        try:
            pnx_p = os.path.dirname(pnx)
            time_pattern_with_underbar = rf"_{get_pk_time_2025_10_20_1159('now')}"
            pnx_n = get_n(pnx)
            pnx_x = get_x(pnx)
            pnx_new = rf"{dst}\{pnx_n}{pnx_x}"
            pattern = r'\d{4}_\d{2}_\d{2}_(월|화|수|목|금|토|일)_\d{2}_\d{2}_\d{2}_\d{3}'
            pnx_n = re.sub(pattern=pattern, repl='', string=pnx_n)
            logging.debug(rf'''pnx="{pnx}"  ''')
            logging.debug(rf'''dst="{dst}"  ''')
            dst_nx = None
            if not is_pnx_existing(pnx=pnx_new):
                dst_nx = rf"{dst}\{pnx_n}{pnx_x}"
            else:
                dst_nx = rf"{dst}\{pnx_n}{time_pattern_with_underbar}{random.randint(10, 99)}{pnx_x}"
            shutil.copytree(src=pnx, dst=dst_nx)
        except:
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
    else:
        print(f"소스 경로 '{pnx}'는 f도 d도 아닙니다.")
