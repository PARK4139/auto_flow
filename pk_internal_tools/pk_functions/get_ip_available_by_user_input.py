import zlib


import win32con
import webbrowser
import undetected_chromedriver as uc
import tqdm
import time
import threading
import tarfile
import speech_recognition as sr
import re
import pywintypes
import pyautogui
import psutil
import paramiko
import os.path
import nest_asyncio
import mysql.connector
import ipdb
import inspect
import datetime

import asyncio
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from urllib.parse import quote
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from PIL import Image, ImageFont, ImageDraw
from PIL import Image
from os.path import dirname
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial as functools_partial
from functools import partial
from datetime import datetime, timedelta
from datetime import datetime
from cryptography.hazmat.backends import default_backend
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_ip_available_by_user_input():
    try:
        while True:
            available_ip_list = get_ip_available_list()
            available_ip_without_localhost_list = []
            available_ip_only_localhost_list = []
            local_ip = get_local_ip()
            # logging.debug(rf'''SELECT REMOTE DEVICE IP BY NUMBER REFER TO BELOW (or 'R'=RETRY   0='TODO IP')  ''')
            # logging.debug("AVAILABLE IP LIST:")
            for idx, ip_info in enumerate(available_ip_list):
                if len(ip_info) >= 2:
                    name, ip = ip_info[0], ip_info[1]
                else:
                    ip = ip_info[0]  # name 정보가 없으면 그냥 ip만 사용
                me_marker = ' (me)' if ip == local_ip or ip == 'localhost' else ''
                # logging.debug(f"{idx + 1}: {ip}{me_marker}")
                if me_marker == '':
                    available_ip_without_localhost_list.append(f'{ip}')
                elif not me_marker == '':
                    available_ip_only_localhost_list.append(f'{ip}{me_marker}')

            available_ip_without_localhost_list.append('R(RETRY)')
            available_ip_without_localhost_list.append('0(TODO IP)')

            user_input = ensure_value_completed_2025_10_12_0000(key_name="user_input", options=available_ip_without_localhost_list)
            if user_input.upper() == '0' or '0(TODO IP)':
                ip = None
                return ip
            if user_input.upper() == '':  # IF USER INPUTS '', RETRY
                continue
            if user_input.upper() == 'R' or 'R(RETRY)':
                logging.debug("RETRYING THE CONNECTION TEST...")
                continue
            user_input = int(user_input) - 1
            if 0 <= user_input < len(available_ip_list):
                ip = available_ip_list[user_input][1]
                return ip
            else:
                logging.debug("Invalid choice. Please run the program again.")
                raise
    except ValueError:
        logging.debug("Invalid input. Please enter a number.")
        raise
