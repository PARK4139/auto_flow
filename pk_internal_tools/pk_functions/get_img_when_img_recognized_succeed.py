import yt_dlp
import tqdm
import tomllib
import toml
import shutil
import shlex
import requests
import pywintypes

import pythoncom
import pygetwindow
import pyaudio
import numpy as np
import math
import keyboard
import json
import hashlib
import functools
import easyocr
import clipboard
import chardet
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from telegram import Bot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from PySide6.QtWidgets import QApplication
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_etc import PkFilter
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from mutagen.mp3 import MP3
from gtts import gTTS
from functools import partial
from datetime import timedelta
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
import logging

import logging


def get_img_when_img_recognized_succeed(img_abspath, recognize_loop_limit_cnt=0, is_zoom_toogle_mode=False):
    import inspect

    import pyautogui
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # speak("화면 이미지 분석을 시도합니다")
    PkGui.pop_up_as_complete(title="화면이미지분석 시도 전 보고", ment="화면 이미지 분석을 시도합니다",
                               auto_click_positive_btn_after_seconds=1)

    ensure_pressed('ctrl', '0'
    5)  # 이미지 분석 시 크롬 zoom 초기화(ctrl+0)

    # 고해상도/다크모드 에서 시도
    for i in range(0, 9):
        ensure_pressed('ctrl', '+')

    chrome_zoom_step = 0

    # 루프카운트 제한 n번 default 0번 으로 설정
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    loop_cnt = 0
    # recognize_loop_limit_cnt=recognize_loop_limit_cnt
    if recognize_loop_limit_cnt == 0:
        while 1:
            # 인식률 및 속도 개선 시도
            # pip install opencv-python # 이것은 고급 기능이 포함되지 않은 Python용 OpenCV의 미니 버전입니다. 우리의 목적에는 충분합니다.
            # confidence=0.7(70%)유사도를 낮춰 인식률개선시도, region 낮춰 속도개선시도, grayscale 흑백으로 판단해서 속도개선시도,
            # open cv 설치했는데 적용안되고 있음. 재부팅도 하였는 데도 안됨.
            # xy_infos_of_imgs=pyautogui.locateOnScreen(img_abspath, confidence=0.7, grayscale=True)
            # debug_as_gui(xy_infos_of_imgs is None)
            logging.debug("화면 이미지 인식 시도 중...")
            loop_cnt = loop_cnt + 1
            try:
                img = pyautogui.locateOnScreen(img_abspath, confidence=0.7, grayscale=True)
                logging.debug(type(img))
                logging.debug(img)
                logging.debug(img is not None)
                if img is not None:
                    return img
                else:
                    logging.debug(f"화면 이미지 분석 중...")
                    logging.debug(img_abspath)
                    ensure_slept(milliseconds=15)
                    if is_zoom_toogle_mode == True:
                        if chrome_zoom_step == 14:
                            chrome_zoom_step = 0
                        elif chrome_zoom_step < 7:
                            ensure_pressed('ctrl', '-')
                            chrome_zoom_step = chrome_zoom_step + 1
                        elif 7 <= chrome_zoom_step:
                            ensure_pressed('ctrl', '+')
                            chrome_zoom_step = chrome_zoom_step + 1
            except pyautogui.ImageNotFoundException:
                logging.debug(f"{loop_cnt}번의 화면인식시도를 했지만 인식하지 못하였습니다")
                pass
    else:
        while 1:
            loop_cnt = loop_cnt + 1
            logging.debug("화면 이미지 인식 시도 중...")
            if recognize_loop_limit_cnt == loop_cnt:
                logging.debug(f"{loop_cnt}번의 화면인식시도를 했지만 인식하지 못하였습니다")
                return None
            try:
                img = pyautogui.locateOnScreen(img_abspath, confidence=0.7, grayscale=True)
                logging.debug(type(img))
                logging.debug(img)
                logging.debug(img is not None)
                if img is not None:
                    return img
            except:
                logging.debug(img_abspath)
                ensure_slept(milliseconds=10)
                if is_zoom_toogle_mode == True:
                    if chrome_zoom_step == 14:
                        chrome_zoom_step = 0
                    elif chrome_zoom_step < 7:
                        ensure_pressed('ctrl', '-')
                        chrome_zoom_step = chrome_zoom_step + 1
                    elif 7 <= chrome_zoom_step:
                        ensure_pressed('ctrl', '+')
                        chrome_zoom_step = chrome_zoom_step + 1
