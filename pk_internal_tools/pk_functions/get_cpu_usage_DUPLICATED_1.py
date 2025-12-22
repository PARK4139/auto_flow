import zipfile
import winreg

            

import urllib.parse
import traceback
import tomllib
import toml
import threading
import speech_recognition as sr
import requests
import re
import random, math
import psutil
import paramiko
import keyboard
import cv2
import colorama
from tkinter import UNDERLINE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from pynput import mouse
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pathlib import Path
from passlib.context import CryptContext
from mutagen.mp3 import MP3
from functools import partial as functools_partial
from dirsync import sync
from datetime import datetime, timedelta
from datetime import datetime
from datetime import date
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
import logging


def get_cpu_usage(interval, process_n):
    import psutil
    import time
    """LosslessCut 프로세스의 CPU 사용량을 측정"""
    for process in psutil.process_iter(attrs=["name", "pid"]):
        if process_n in process.info["name"]:
            proc = psutil.Process(process.info["pid"])
            proc.cpu_percent(interval=None)  # 첫 번째 호출 (무시)
            time.sleep(interval)  # interval 동안 기다리기
            return proc.cpu_percent(interval=None)  # 두 번째 호출 값 반환
    return None  # 프로세스가 없으면 None 반환
