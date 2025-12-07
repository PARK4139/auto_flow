import win32com.client
import undetected_chromedriver as uc
import traceback
import tomllib
import tomllib
import toml
import timeit
import sqlite3
import socket, time
import socket
import shutil
import requests
import pythoncom
import psutil
import paramiko
import os, inspect
import mysql.connector
import mutagen
import math
import json
import ipdb
import hashlib
import functools
import datetime
import cv2
import chardet
import calendar
from telegram import Bot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

from PIL import Image, ImageFilter
from os.path import dirname
from moviepy import VideoFileClip
from functools import partial
from functools import lru_cache
from enum import Enum
from dirsync import sync
from datetime import datetime, time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def print_current_mouse_abs_info():
    import inspect

    import ipdb
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    x, y = get_current_mouse_abs_info()
    logging.debug(f'''x="{x}"''')
    logging.debug(f'''y="{y}"''')

    ipdb.set_trace()
