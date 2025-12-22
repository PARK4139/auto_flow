import zlib
import yt_dlp
import winreg
import win32com.client
import webbrowser
import urllib.parse
import urllib
import undetected_chromedriver as uc
import tomllib
import toml
import threading
import sys
import subprocess
import string
import sqlite3
import socket
import re
import random, math

import pythoncom
import pygetwindow
import pyautogui
import pyaudio
import platform
import pickle
import pandas as pd
import os, inspect
import os
import numpy as np
import nest_asyncio
import math
import keyboard
import ipdb
import inspect
import importlib
import hashlib
import functools
import easyocr
import datetime
import cv2
import colorama
import chardet
import calendar

import asyncio
from zipfile import BadZipFile
from urllib.parse import urlparse
from telethon import TelegramClient, events
from telegram import Bot, Update
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_ROOT_HIDDEN
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from PIL import Image, ImageFilter
from PIL import Image
from passlib.context import CryptContext
from os.path import dirname
from os import path
from gtts import gTTS
from fastapi import HTTPException
from enum import Enum
from dirsync import sync
from datetime import datetime, timedelta
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from bs4 import ResultSet
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_max_pid(process_img_n: str):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    pids = get_pids(process_img_n=process_img_n)

    logging.debug(f'''pids="{pids}"  ''')

    return max(pids)
