import zlib
import zipfile
import yt_dlp
import winreg


import undetected_chromedriver as uc
import tomllib
import tomllib
import toml
import threading
import tarfile
import sys
import subprocess, time
import string
import sqlite3
import socket, time
import shutil
import shlex
import secrets
import requests
import re
import random, math

import pythoncom
import pyautogui
import psutil
import platform
import pickle
import paramiko
import pandas as pd
import os.path
import os, inspect
import os
import math
import keyboard
import inspect
import importlib
import hashlib
import easyocr
import datetime
import cv2
import colorama
import colorama
import clipboard
import chardet

import asyncio
from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, urlparse
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging
import logging


from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_etc import PkFilter
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, d_pk_root_hidden
from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_objects.performance_logic import ensure_seconds_measured, pk_measure_memory

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


from PIL import Image, ImageFilter
from os.path import dirname
from os import path
from moviepy import VideoFileClip
from functools import partial as functools_partial
from functools import lru_cache
from fastapi import HTTPException
from enum import Enum
from datetime import datetime, timedelta
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup
from base64 import b64encode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def print_class_field_and_value(class_n):  # print 보다는 get 으로 바꾸는게 좋겠다.

    cmd_usage_explanations = []
    cmd_usage_explanations.append(title)
    cmd_usage_explanations.append('\n')
    cmd_usage_explanations.append('<예시> : python console_blurred.py <mode_option>')
    cmd_usage_explanations.append('\n')
    longest_field = max(vars(class_n), key=len)  # mkr_get_longest_field_name
    longest_value = vars(class_n)[longest_field]  # mkr_get_longest_field_value
    for key, value in class_n.__dict__.items():  # mkr_get_field_name_and_field_value
        if not key.startswith('__'):  # 내장 속성 제외
            cmd_usage_explanations.append(f"{key}{" " * (len(longest_field) - len(key))}: {value}")
    cmd_usage_explanations.append('\n')
    for cmd_usage_explanation in cmd_usage_explanations:
        logging.debug(cmd_usage_explanation)
    cmd_usage_explanations.append('\n')
