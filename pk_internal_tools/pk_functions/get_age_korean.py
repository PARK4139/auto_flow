import yt_dlp

import win32con
import win32con
import uuid
import tomllib
import timeit
import threading
import subprocess
import shlex
import secrets


import pyaudio
import platform
import pickle
import os.path
import os, inspect
import keyboard
import hashlib
import functools
import easyocr
import colorama
import clipboard
import calendar
from urllib.parse import quote, urlparse
from urllib.parse import quote
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from selenium.webdriver.support import expected_conditions as EC
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title


from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext



from paramiko import SSHClient, AutoAddPolicy
from os import path
from mutagen.mp3 import MP3
from functools import partial as functools_partial
from enum import Enum
from datetime import datetime
from datetime import date
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from collections import Counter
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
import logging


import logging


def get_age_korean(birth_day):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # 2023-1994=29(생일후)
    # 2024-1994=30(생일후)
    # 만나이 == 생물학적나이
    # 생일 전 만나이
    # 생일 후 만나이
    pass
