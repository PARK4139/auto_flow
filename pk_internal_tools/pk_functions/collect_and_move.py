import zlib
import zipfile
import yt_dlp


import win32con
import urllib.parse
import tqdm
import tomllib
import toml
import timeit
import tarfile
import string
import sqlite3
import secrets
import requests
import random
import platform
import pandas as pd
import os, inspect
import numpy as np
import mysql.connector
import math
import hashlib
import easyocr
import datetime
import calendar
from zipfile import BadZipFile
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs, unquote
from urllib.parse import quote
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from PIL import Image
from moviepy import VideoFileClip
from functools import partial
from functools import lru_cache
from enum import Enum
from dirsync import sync
from datetime import timedelta
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from bs4 import BeautifulSoup
from base64 import b64encode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style

import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def collect_and_move(files, src_root):
    """files를 src_root+'_merged' 폴더로 이동, 중복 파일명에 (n) 붙임"""
    import os
    import shutil

    dst_root = f"{src_root.rstrip(os.sep)}_merged"
    os.makedirs(dst_root, exist_ok=True)

    for src_path in files:
        name = os.path.basename(src_path)
        unique_name = ensure_unique(dst_root, name)
        dst_path = os.path.join(dst_root, unique_name)
        shutil.move(src_path, dst_path)
        print(f"Moved: {src_path} -> {dst_path}")
