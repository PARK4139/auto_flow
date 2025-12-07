import yt_dlp
import win32con
import webbrowser
import tomllib
import threading
import pygetwindow
import pickle
import keyboard
import inspect
import cv2
import asyncio
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front



from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from passlib.context import CryptContext
from gtts import gTTS
from dirsync import sync
from bs4 import ResultSet

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_list_added_suffix_each_element(working_list, suffix):
    return [f"{line}{suffix}" for line in working_list]
