
import win32con
import win32con
import webbrowser
import urllib.parse
import traceback
import tqdm
import time
import sqlite3
import socket
import re
import os, inspect
import nest_asyncio
import mutagen
import ipdb
import inspect
import datetime
import clipboard
import chardet
import calendar

from yt_dlp import YoutubeDL
from urllib.parse import quote
from tkinter import UNDERLINE
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pytube import Playlist
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.get_d_working import get_d_working

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f


from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from passlib.context import CryptContext
from mysql.connector import connect, Error
from mutagen.mp3 import MP3
from functools import partial as functools_partial
from functools import partial
from colorama import init as pk_colorama_init
from bs4 import ResultSet

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

import logging


def get_random_urlsafe():
    import secrets

    return secrets.token_urlsafe(16)  # 16바이트의 난수를 URL-safe 문자열로 생성
