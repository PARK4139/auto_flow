import zlib
import zipfile
import winreg


import win32con
import win32com.client
import uuid
import urllib.parse
import tqdm
import tomllib
import toml
import time
import tarfile
import subprocess
import string
import socket, time
import secrets
import re
import random
import pythoncom
import pyglet
import pygetwindow
import pyautogui
import pickle
import paramiko
import json
import ipdb
import inspect
import functools
import datetime
import colorama
from zipfile import BadZipFile
from webdriver_manager.chrome import ChromeDriverManager
from telethon import TelegramClient, events
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from queue import Queue, Empty
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_state_printed import ensure_state_printed
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING



from mutagen.mp3 import MP3
from gtts import gTTS
from functools import partial as functools_partial
from functools import partial
from datetime import datetime
from cryptography.hazmat.primitives import padding
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def reset_wired_connection_list(wired_connection_no_range, **remote_device_target_config):
    for wired_connection_no in wired_connection_no_range:
        remote_device_target_config['local_ssh_public_key'] = os.path.join(D_USERPROFILE, ".ssh", "id_ed25519.pub") = {'wired_connection_no': wired_connection_no, "address": rf"", "method": "auto",
                                "gateway": "", "dns": ""}
        set_wired_connection(vpc_wired_connection, **remote_device_target_config)
