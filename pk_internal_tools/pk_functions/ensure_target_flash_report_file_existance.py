import zlib
import win32con
import uuid
import urllib
import undetected_chromedriver as uc
import traceback
import tomllib
import toml
import timeit
import time
import subprocess
import socket
import pywintypes

import pythoncom
import pyaudio
import math
import keyboard
import functools
import easyocr
import datetime
import cv2

from urllib.parse import urlparse
from telegram import Bot, Update
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from pytube import Playlist
from PySide6.QtWidgets import QApplication


from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
import logging
import logging

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_etc import PkFilter


from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext


from PIL import Image
from pathlib import Path
from passlib.context import CryptContext
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from base64 import b64decode

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_etc import PkFilter, PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def ensure_target_flash_report_file_existance(**config):
    # TODO
    target_device_type = config['vpc_type']
    flash_report_file_path = f"{vpc_type}_flash_report.txt"
    ensure_pnx_made(pnx=flash_report_file_path, mode='f', script_list=[
        "====================== ACU NO flash report ======================\n",
    ])
    with open(flash_report_file_path, "a") as f:
        f.write("ACU NO flash report\n")
