import win32con
import uuid
import toml
import threading
import sys
import speech_recognition as sr
import socket
import requests
import re

import pyglet
import pygetwindow
import pyautogui
import pickle
import os.path
import os
import nest_asyncio
import math
import keyboard
import ipdb
import inspect
import cv2
from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import UNDERLINE
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from queue import Queue, Empty
from pynput import mouse

from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical


from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from PIL import Image
from paramiko import SSHClient, AutoAddPolicy
from os.path import dirname
from mutagen.mp3 import MP3
from gtts import gTTS
from functools import partial
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from bs4 import ResultSet
from pathlib import Path
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def is_pattern_in_prompt(prompt: str, pattern: any, with_case_ignored=True):
    import inspect
    import re

    # logging.debug(string = rf'''string="{string}"  ''')
    # logging.debug(string = rf'''regex="{regex}"  ''')
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug(rf'''{PK_UNDERLINE}{func_n}()  ''')
    if with_case_ignored == True:
        pattern = re.compile(pattern, re.IGNORECASE)
    else:
        pattern = re.compile(pattern)
    m = pattern.search(prompt)
    if m:
        # logging.debug("function name   here here here")
        # logging.debug(rf"contents: {contents}")
        # logging.debug(rf"regex: {regex}")
        # logging.debug(rf"True")
        return 1
    else:
        # logging.debug(rf"contents: {contents}")
        # logging.debug(rf"regex: {regex}")
        # logging.debug(rf"False")
        return 0
