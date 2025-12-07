import zlib
import winreg
import win32con
import webbrowser
import uuid
import urllib.parse
import urllib
import timeit
import string
import secrets
import requests
import pywintypes
import pythoncom
import pygetwindow
import pyautogui
import pyaudio
import psutil
import paramiko
import os, inspect
import mysql.connector
import mutagen
import math
import importlib
import hashlib
import functools
import datetime
import colorama
import chardet
import calendar

import asyncio
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from urllib.parse import quote, urlparse
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pytube import Playlist
from pynput import mouse
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext



from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial as functools_partial
from functools import partial
from functools import lru_cache
from fastapi import HTTPException
from enum import Enum
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from bs4 import BeautifulSoup
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pathlib import Path
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, d_pk_root_hidden, d_pk_external_tools

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_f_changed_list_from_d_interested_list(d_interested_list, monitoring_interval=0.2, time_limit=None,
                                              change_cnt_limit=None):
    import time

    import importlib

    # 모듈 자체를 먼저 import
    watchdog_observers = importlib.import_module("watchdog.observers")
    watchdog_events = importlib.import_module("watchdog.events")
    pkg_cli = importlib.import_module("pk_external_tools.interface_cmd_line")
    pkg_constants = importlib.import_module("pk_external_tools.constants")

    # 필요한 속성만 참조
    Observer = watchdog_observers.Observer
    FileSystemEventHandler = watchdog_events.FileSystemEventHandler
    logging.debug = pkg_cli.logging.debug
    DOWNLOADS = D_DOWNLOADS

    d_interested_list = [Path(d) for d in d_interested_list]

from pk_internal_tools.pk_objects.pk_file_change_handler import FileChangeHandler

    event_handler = FileChangeHandler(change_cnt_limit)
    observer = Observer()

    for d in d_interested_list:
        observer.schedule(event_handler, d, recursive=True)

    logging.debug(
        rf"[DETECT F_CHANGED LOOP STARTED] monitoring_interval={monitoring_interval}, len(d_interested_list)={len(d_interested_list)}",
        print_color='blue')

    observer.start()
    start_time = time.time()

    try:
        while 1:
            if time_limit is not None and (time.time() - start_time > time_limit):
                break
            ensure_slept(seconds=monitoring_interval)
    except StopIteration:
        pass
    except KeyboardInterrupt:
        logging.debug("Monitoring stopped by user.")

    observer.stop()
    observer.join()

    return event_handler.f_changed_list
