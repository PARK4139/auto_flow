import zlib

import win32con
import undetected_chromedriver as uc
import traceback
import toml
import timeit
import threading
import subprocess
import sqlite3
import random
import pywintypes
import nest_asyncio
import mysql.connector
import inspect
import easyocr
import cv2
import chardet
from yt_dlp import YoutubeDL
from urllib.parse import quote, urlparse
from tkinter import UNDERLINE
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from gtts import gTTS
from dirsync import sync
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from collections import Counter
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style


import logging


def get_pnx_new(d_working, pnx):
    # ensure_pnx_moved 에  mode_count 로 통합
    """중복되지 않는 새로운 f명을 생성"""
    import os
    pnx_nx = get_nx(pnx)
    pnx_n, pnx_x = os.path.splitext(pnx_nx)
    counter = 1
    pnx_new = os.path.join(d_working, pnx_nx)
    while os.path.exists(pnx_new):
        pnx_new = os.path.join(d_working, f"{pnx_n}_{counter}{pnx_x}")
        counter += 1
    return get_pnx_unix_style(pnx=pnx_new)
