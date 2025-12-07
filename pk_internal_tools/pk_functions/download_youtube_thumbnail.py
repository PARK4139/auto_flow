import tomllib
import toml
import shlex
import secrets
import re
import random, math

import pyautogui
import os
import numpy as np
import inspect
import datetime
import calendar
from urllib.parse import quote
from typing import TypeVar, List
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.performance_logic import ensure_seconds_measured, pk_measure_memory
from passlib.context import CryptContext
from mutagen.mp3 import MP3
from fastapi import HTTPException
from enum import Enum
from datetime import datetime, time
from Cryptodome.Random import get_random_bytes
from base64 import b64decode
from pathlib import Path
from pk_internal_tools.pk_functions.is_d import is_d

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def download_youtube_thumbnail(youtube_video_url, f_dst_jpg):
    import requests
    youtube_video_id = youtube_video_url.split('v=')[-1].split('&')[0]
    # 최대 해상도 썸네일 URL
    thumbnail_url = f'https://img.youtube.com/vi/{youtube_video_id}/maxresdefault.jpg'
    # 이미지 다운로드 및 저장
    try:
        response = requests.get(thumbnail_url, stream=True)
        response.raise_for_status()
        with open(file=f_dst_jpg, mode='wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"downloaded : {f_dst_jpg}")
    except requests.exceptions.RequestException as e:
        print(f"썸네일 다운로드 실패: {e}")
