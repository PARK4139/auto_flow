import zlib
import zipfile
import winreg


import webbrowser
import urllib.parse
import urllib
import undetected_chromedriver as uc
import tomllib
import tomllib
import toml
import timeit
import subprocess
import string
import sqlite3
import speech_recognition as sr
import socket
import shutil
import secrets
import pywintypes


import pythoncom
import paramiko
import os.path
import os
import numpy as np
import nest_asyncio
import mysql.connector
import mutagen
import inspect
import importlib
import functools
import cv2
import colorama
import clipboard
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, urlparse
from urllib.parse import quote
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from telegram import Bot, Update
from telegram import Bot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.ensure_state_printed import ensure_state_printed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext


from PIL import Image, ImageFilter
from PIL import Image
from pathlib import Path
from os.path import dirname
from os import path
from gtts import gTTS
from functools import lru_cache
from enum import Enum
from dirsync import sync
from datetime import timedelta
from datetime import datetime, time
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from collections import defaultdict, Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup
from base64 import b64encode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def reensure_pnx_moved_parmanently(pnx):
    import inspect
    import os
    import platform
    import shutil
    import traceback

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if platform.system() == 'Windows':
        try:
            if validate_and_return(value=pnx) is not False:
                os.chdir(os.path.dirname(pnx))
                if os.path.exists(pnx):
                    if is_d(pnx):
                        # shutil.rmtree(pnx_todo)
                        # if is_d(pnx_todo):
                        #     run_via_cmd_exe(rf'echo y | rmdir /s "{pnx_todo}"')
                        ensure_pnxs_move_to_recycle_bin(pnx)
                    elif is_f(pnx):
                        # os.remove(pnx_todo)
                        # if is_f(pnx_todo):
                        #     run_via_cmd_exe(rf'echo y | del /f "{pnx_todo}"')
                        ensure_pnxs_move_to_recycle_bin(pnx)

                    # logging.debug(f" green {texts}")
                    # logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        except:
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

        finally:
            os.chdir(d_pk_root)
    else:
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        try:
            if validate_and_return(value=pnx) is not False:
                os.chdir(os.path.dirname(pnx))
                if os.path.exists(pnx):
                    if is_d(pnx):
                        shutil.rmtree(pnx)
                    elif is_f(pnx):
                        os.remove(pnx)
        except:
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")

        finally:
            os.chdir(d_pk_root)
