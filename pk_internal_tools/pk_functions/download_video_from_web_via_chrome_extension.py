

import win32com.client
import uuid
import urllib.parse
import undetected_chromedriver as uc
import tqdm
import tomllib
import toml
import timeit
import time
import sqlite3
import socket
import shlex
import secrets

import pythoncom
import pygetwindow
import pyautogui
import psutil
import platform
import paramiko
import pandas as pd
import mutagen
import keyboard
import ipdb
import importlib
import easyocr
import colorama
import calendar
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from urllib.parse import quote
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging



from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


from mysql.connector import connect, Error
from mutagen.mp3 import MP3
from functools import partial as functools_partial
from functools import partial
from dirsync import sync
from datetime import datetime, timedelta
from colorama import init as pk_colorama_init
from collections import Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup
from base64 import b64decode


from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def download_video_from_web_via_chrome_extension():
    while 1:
        # press("ctrl", "0")
        f_png = rf"{d_pk_root}\pk_external_tools\download_video_via_chrome_extensions.png"
        click_center_of_img_recognized_by_mouse_left(img_pnx=f_png, loop_limit_cnt=10)

        ensure_slept(1000)

        ensure_pressed("tab")
        ensure_slept(30)

        ensure_pressed("enter")
        ensure_slept(30)

        ensure_pressed("ctrl", "shift", "tab")

        ensure_pressed("ctrl", "0")
        ensure_pressed("ctrl", "-")
        ensure_pressed("ctrl", "-")
        break
