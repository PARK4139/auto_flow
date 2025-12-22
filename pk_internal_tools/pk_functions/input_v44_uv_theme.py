import zipfile
import winreg


import webbrowser
import urllib
import tqdm
import tomllib
import time
import tarfile
import sqlite3
import speech_recognition as sr
import socket
import secrets
import pywintypes
import pyglet
import pyaudio
import platform
import pickle
import os.path
import math
import functools
import easyocr
import clipboard
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PySide6.QtWidgets import QApplication



from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared



from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_texts import PkTexts


from PIL import Image
from passlib.context import CryptContext
from os.path import dirname
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from fastapi import HTTPException
from Cryptodome.Random import get_random_bytes
from colorama import init as pk_colorama_init
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

import logging
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed


def input_v44_uv_theme(
        text_working: str,
        limit_seconds: int = 30,
        return_default: str | None = None,
        *,
        masked: bool = False,
        fuzzy_accept: list[tuple[str, ...]] | None = None,
        validator=None,
        vi_mode: bool = True,
        **kwargs
):
    """
    input_v44_uv_theme 함수를 ensure_value_completed로 대체
    """
    # fuzzy_accept가 있는 경우 해당 값들을 options에 추가
    options = []
    if fuzzy_accept:
        for group in fuzzy_accept:
            options.extend(group)
    
    # return_default가 있는 경우 options에 추가
    if return_default:
        options.append(return_default)
    
    # validator가 있는 경우 기본값만 반환 (validator는 ensure_value_completed에서 지원하지 않음)
    if validator:
        return return_default
    
    # ensure_value_completed 호출
    return ensure_value_completed(key_name=text_working, options=options)

