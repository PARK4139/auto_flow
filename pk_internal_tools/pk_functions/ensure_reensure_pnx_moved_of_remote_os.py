import winreg


import win32con
import uuid
import urllib.parse
import urllib
import tqdm
import toml
import toml
import timeit
import threading
import tarfile
import socket
import requests
import re
import random
import pywintypes

import platform
import paramiko
import os.path
import numpy as np
import mysql.connector
import json
import ipdb
import inspect
import hashlib
import functools
import easyocr
import colorama
from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib.parse import quote
from tkinter import UNDERLINE
from telegram import Bot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front



from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from PIL import Image, ImageFilter
from functools import partial as functools_partial
from functools import partial
from functools import lru_cache
from enum import Enum
from dirsync import sync
from datetime import datetime
from datetime import date
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from collections import defaultdict, Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def ensure_reensure_pnx_moved_of_remote_os(pnx, **remote_device_target_config):
    std_outs, std_err_list = ensure_command_to_remote_os(cmd=f"rm -rf {pnx}", **remote_device_target_config)
    std_outs, std_err_list = ensure_command_to_remote_os(cmd=f"ls {pnx}", **remote_device_target_config)
    signature = 'todo'
    for std_out in std_outs:
        if signature in std_out:
            logging.debug(f'''remove {pnx} at {remote_device_target_config['ip']}  ''')
        else:
            logging.debug(f'''remove {pnx} at {remote_device_target_config['ip']}  ''')
            raise
