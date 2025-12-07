import zipfile
import yt_dlp


import win32com.client
import urllib.parse
import undetected_chromedriver as uc
import traceback
import tomllib
import tarfile
import sys
import subprocess
import string
import shlex
import secrets
import requests
import re
import pythoncom
import pyautogui
import pyaudio
import paramiko
import os.path
import os
import mysql.connector
import mutagen
import json
import functools
import easyocr
import datetime
import colorama
import clipboard
import chardet
import calendar

from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from typing import TypeVar, List
from tkinter import UNDERLINE
from telegram import Bot, Update
from seleniumbase import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_etc import PkFilter


from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext



from PIL import Image
from pathlib import Path
from passlib.context import CryptContext
from os import path
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from functools import partial
from functools import lru_cache
from enum import Enum
from dirsync import sync
from datetime import datetime, timedelta
from datetime import datetime, time
from datetime import date
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from Cryptodome.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter
from collections import Counter
from bs4 import BeautifulSoup
from base64 import b64decode

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_etc import PkFilter, PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
import logging
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def ensure_wsl_flash_directory_flashable (target_device_data):
    if 'no' in target_device_data.device_identifier:
        ensure_command_to_remote_os("mkdir -p ~/Downloads/flash/no_flash/")
    elif 'nx' in target_device_data.device_identifier:
        ensure_command_to_remote_os("mkdir -p ~/Downloads/flash/nx_flash/")
    elif 'xc' in target_device_data.device_identifier:
        ensure_command_to_remote_os("mkdir -p ~/Downloads/flash/xc_flash/")
    elif 'evm' in target_device_data.device_identifier:
        ensure_command_to_remote_os("mkdir -p ~/Downloads/flash/evm_flash/")
    else:
        logging.debug(f'''unknown target_device_data.identifier ({target_device_data.device_identifier}) ''',
                      print_color='yellow')
        raise
