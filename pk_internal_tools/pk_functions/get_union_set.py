import zipfile
import yt_dlp

import urllib.parse
import traceback
import tqdm
import time
import string
import pyautogui
import pickle
import paramiko
import numpy as np
import nest_asyncio
import json
import importlib
import easyocr
import cv2
import clipboard

from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pytube import Playlist
from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once


from passlib.context import CryptContext
from mutagen.mp3 import MP3
from enum import Enum
from datetime import datetime
from Cryptodome.Random import get_random_bytes
from base64 import b64encode
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_union_set(set_a, set_b):
    """합집합 A ∪ B"""
    return set(set_a) | set(set_b)
