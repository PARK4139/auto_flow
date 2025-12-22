import zipfile

import win32con
import win32con
import win32com.client
import webbrowser
import uuid
import urllib
import traceback
import tomllib
import tomllib
import toml
import time
import threading
import tarfile
import sys
import sqlite3
import speech_recognition as sr
import socket, time
import socket
import shutil
import secrets
import requests
import re
import pywintypes
import pyglet
import pygetwindow
import pyautogui
import pyaudio
import psutil
import paramiko
import pandas as pd
import os
import nest_asyncio
import mysql.connector
import math
import keyboard
import ipdb
import datetime
import cv2
import chardet

import asyncio
from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib.parse import quote
from tkinter import UNDERLINE
from telegram import Bot, Update
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from queue import Queue, Empty
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_ROOT_HIDDEN
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from PIL import Image, ImageFont, ImageDraw
from PIL import Image, ImageFilter
from PIL import Image
from pathlib import Path
from os.path import dirname
from os import path
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial as functools_partial
from functools import partial
from functools import lru_cache
from fastapi import HTTPException
from dirsync import sync
from datetime import datetime, timedelta
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from colorama import init as pk_colorama_init
from collections import defaultdict, Counter
from collections import Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx


from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def kill_chrome_tab_duplicated():
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    chrome_tab_urls_processed = []  # 이미 처리된 URL을 저장하는 리스트
    loop_limit = 10
    loop_out_cnt = 0

    while 1:
        window_title = "Chrome"
        if is_window_opened(window_title_seg=window_title):
            ensure_window_to_front(window_title)

        logging.debug(rf'''loop_out_cnt="{loop_out_cnt}"  ''')
        logging.debug(rf'''loop_limit="{loop_limit}"  ''')

        # 탭을 전환하고 URL을 가져옵니다.
        ensure_pressed("ctrl", "l")
        ensure_slept(milliseconds=5)
        url_dragged = get_txt_dragged()

        # 중복 여부 확인
        if url_dragged in chrome_tab_urls_processed:
            logging.debug(rf'''URL already processed: "{url_dragged}"  ''')
            ensure_pressed("ctrl", "tab")  # 다음 탭으로 이동
            loop_out_cnt += 1
            if loop_out_cnt >= loop_limit:
                break
            continue

        # 다음 탭으로 전환 후 URL 가져오기
        ensure_pressed("ctrl", "tab")
        ensure_slept(milliseconds=5)
        ensure_pressed("ctrl", "l")
        ensure_slept(milliseconds=5)
        url_dragged_new = get_txt_dragged()

        logging.debug(rf'''url_dragged="{url_dragged}"  ''')
        logging.debug(rf'''url_dragged_new="{url_dragged_new}"  ''')

        # 중복된 URL이면 탭 닫기
        if url_dragged == url_dragged_new:
            logging.debug(rf'''Closing duplicate tab for URL: "{url_dragged}"  ''')
            ensure_pressed("ctrl", "w")  # 탭 닫기
            continue

        # 처리된 URL을 리스트에 추가
        chrome_tab_urls_processed.append(url_dragged)
        logging.debug(rf'''chrome_tab_urls_processed="{chrome_tab_urls_processed}"  ''')

        # 최대 반복 횟수 초과 시 종료
        loop_out_cnt += 1
        if loop_out_cnt >= loop_limit:
            break
