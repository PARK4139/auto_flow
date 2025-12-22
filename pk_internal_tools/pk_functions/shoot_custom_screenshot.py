import yt_dlp


import urllib
import tomllib
import time
import socket
import shlex

import paramiko
import os
import numpy as np
import importlib
import easyocr
import cv2
import colorama

from zipfile import BadZipFile
from telethon import TelegramClient, events
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pathlib import Path
from mutagen.mp3 import MP3
from dirsync import sync
from dataclasses import dataclass
from base64 import b64encode
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def shoot_custom_screenshot():
    import asyncio
    asyncio.run(shoot_custom_screenshot_via_asyncio())
