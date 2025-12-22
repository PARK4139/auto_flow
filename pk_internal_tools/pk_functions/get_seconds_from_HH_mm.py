import yt_dlp
import winreg



import win32con
import uuid
import urllib
import undetected_chromedriver as uc
import traceback
import tqdm
import toml
import timeit
import time
import threading
import tarfile
import sys
import subprocess, time
import subprocess
import string
import sqlite3
import speech_recognition as sr
import socket
import shutil
import re
import random
import pywintypes


import pythoncom
import pygetwindow
import pyautogui
import pyaudio
import platform
import pickle
import paramiko
import pandas as pd
import os.path
import os
import mysql.connector
import json
import inspect
import importlib
import functools
import datetime
import cv2
import clipboard
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from typing import TypeVar, List
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from PySide6.QtWidgets import QApplication
from pynput import mouse

from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front




from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

import logging
import logging

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, D_PK_ROOT_HIDDEN

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from PIL import Image
from os.path import dirname
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial as functools_partial
from fastapi import HTTPException
from dirsync import sync
from datetime import datetime, timedelta
from datetime import datetime
from datetime import date
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_seconds_from_HH_mm(HH, mm):
    import datetime
    now = datetime.datetime.now()
    target_time = datetime.datetime(now.year, now.month, now.day, HH, mm)
    if now > target_time:
        target_time += datetime.timedelta(days=1)
    return (target_time - now).seconds
