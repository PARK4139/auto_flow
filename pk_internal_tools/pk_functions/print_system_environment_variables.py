import yt_dlp

import win32con
import uuid
import urllib.parse
import urllib
import tomllib
import toml
import timeit
import subprocess
import sqlite3
import shutil
import secrets
import requests
import random
import pywintypes
import pyautogui
import platform
import paramiko
import os, inspect
import numpy as np
import nest_asyncio
import mutagen
import math
import ipdb
import inspect
import importlib
import functools
import clipboard
import chardet

from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote, urlparse, parse_qs
from tkinter import UNDERLINE
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession


from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state


from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pathlib import Path
from passlib.context import CryptContext
from os import path
from mutagen.mp3 import MP3
from functools import partial
from enum import Enum
from cryptography.hazmat.primitives import padding
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from bs4 import ResultSet
from pk_internal_tools.pk_functions.get_nx import get_nx
# 
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def print_system_environment_variables():
    import sys
    """print 시스템 환경변수 path"""
    from os.path import dirname
    sys.path.insert(0, dirname)
    sys.path.append(r'C:\Python312\Lib\site-packages')
    for i in sys.path:
        print(i)
