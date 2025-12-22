import yt_dlp
import win32con
import win32com.client
import timeit
import time
import subprocess, time
import subprocess
import string
import sqlite3
import shlex
import re

import psutil
import pandas as pd
import os, inspect
import numpy as np
import nest_asyncio
import json
import ipdb
import inspect
import importlib
import hashlib
import datetime
import chardet
import calendar

from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from telegram import Bot
from selenium.webdriver.common.action_chains import ActionChains
from pynput import mouse
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from PIL import Image
from passlib.context import CryptContext
from os.path import dirname
from os import path
from moviepy import VideoFileClip
from gtts import gTTS
from datetime import datetime, timedelta
from datetime import date
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from collections import Counter
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
# 
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_media_files_allowed_to_load(ext_list_allowed, d_working):
    import os
    if QC_MODE:
        logging.debug(f'''ext_list_allowed={ext_list_allowed}  ''')
    media_files_allowed = []
    pnx_list = get_pnxs_from_d_working(d_working=d_working, with_walking=False)
    ensure_list_written_to_f(working_list=pnx_list, f=F_VIDEO_LIST_ALLOWED_TO_LOAD_TXT, mode='w')

    for f in get_list_from_f(F_VIDEO_LIST_ALLOWED_TO_LOAD_TXT):
        f = f.replace("\n", '')
        f_x = os.path.splitext(f)[1].replace("\n", '')
        f_nx = os.path.basename(f).lower()

        if not f_x:  # 확장자가 없을 경우 빈 문자열이기 때문에 예외 처리
            if QC_MODE:
                logging.debug(f"[NOT ALLOWED] [확장자 없음]: {f}")
            continue

        f_x = f_x.lower()  # 확장자가 있을 때만 소문자로 변환

        if f_x not in ext_list_allowed:
            if QC_MODE:
                logging.debug(f"[NOT ALLOWED] [확장자 불가]: f={f}")
            continue

        if any(keyword in f_nx for keyword in {"seg", "temp"}):
            if QC_MODE:
                logging.debug(f"[NOT ALLOWED] [금지 키워드 포함] : f={f} f_x={f_x}")
            continue
        if QC_MODE:
            logging.debug(f"[ALLOWED] [확장자 가능]: f={f} f_x={f_x}")
        media_files_allowed.append(f)

    return media_files_allowed
