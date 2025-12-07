import zlib
import winreg


import win32con
import webbrowser
import uuid
import urllib.parse
import urllib
import tqdm
import tomllib
import threading
import tarfile
import sys
import string
import sqlite3
import speech_recognition as sr
import shlex

import pythoncom
import pyglet
import pygetwindow
import pyaudio
import psutil
import pickle
import os.path
import os
import mutagen
import math
import inspect
import datetime
import cv2
import chardet
import calendar
import asyncio
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from tkinter import UNDERLINE
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_etc import PkFilter

from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from passlib.context import CryptContext
from os.path import dirname
from os import path
from mutagen.mp3 import MP3
from functools import partial
from functools import lru_cache
from fastapi import HTTPException
from enum import Enum
from datetime import datetime
from datetime import date
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from Cryptodome.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from collections import Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup

from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging

import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_age_package(yyyy_birth, mm_birth, dd_birth, today_date=None):
    from datetime import date

    yyyy_birth = int(yyyy_birth)
    mm_birth = int(mm_birth)
    dd_birth = int(dd_birth)

    # today_date가 주어지지 않으면 오늘 날짜로 설정
    today = today_date or date.today()

    korean_age = today.year - yyyy_birth + 1
    has_had_birthday = (today.month, today.day) >= (mm_birth, dd_birth)
    international_age = today.year - yyyy_birth if has_had_birthday else today.year - yyyy_birth - 1

    return korean_age, international_age
