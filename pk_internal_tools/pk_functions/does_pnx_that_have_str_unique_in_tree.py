import zlib


import win32con
import win32con
import win32com.client
import urllib
import traceback
import tqdm
import timeit
import time
import threading
import tarfile
import subprocess, time
import subprocess
import secrets
import re
import random
import pywintypes

import pythoncom
import pyglet
import pyautogui
import psutil
import platform
import pickle
import paramiko
import os.path
import mutagen
import hashlib
import easyocr
import cv2
import colorama

import asyncio
from zipfile import BadZipFile
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, urlparse
from urllib.parse import quote
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from queue import Queue, Empty
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
import logging

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from PIL import Image
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from functools import partial as functools_partial
from functools import partial
from functools import lru_cache
from fastapi import HTTPException
from datetime import timedelta
from datetime import datetime, time
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from collections import Counter
from base64 import b64encode

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def does_pnx_that_have_str_unique_in_tree(str_unique, str_positive, tree_pnx=None):
    import os

    if tree_pnx is None:
        f_list = os.listdir()
    else:
        f_list = []
        for root, d_nx_list, file_nxs in os.walk(tree_pnx):
            for f_nx in file_nxs:
                item_pnx = os.path.abspath(os.path.join(root, f_nx))
                f_list.append(item_pnx)

    for f in f_list:
        if is_pattern_in_prompt(f, str_unique):
            logging.debug(str_positive)
            return 1
    else:
        return 0
