import yt_dlp


import win32con
import webbrowser
import urllib
import tomllib
import tarfile
import sys
import subprocess
import string
import sqlite3
import pywintypes

import pyglet
import pygetwindow
import pyautogui
import pickle
import os
import numpy as np
import mysql.connector
import mutagen
import keyboard
import ipdb
import functools
import easyocr
import cv2
import clipboard
import chardet
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, urlparse
from urllib.parse import quote
from typing import TypeVar, List
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

import logging


from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import Image, ImageFilter
from passlib.context import CryptContext
from paramiko import SSHClient, AutoAddPolicy
from enum import Enum
from dirsync import sync
from datetime import datetime
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from collections import Counter
from bs4 import ResultSet

# 
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def merge_d_list(d_list: List[str]):
    import os
    import string

    # f명들을 나열한다.
    # f을 깊이 별로 나열을 하고 깊이가 깊은 것부터 시작해서 깊이가 낮은 것으로 처리해 나간다

    d_list = [x for x in d_list if x.strip()]  # 리스트 요소 "" remove,  from ["", A] to [A]    from [""] to []
    d_list = [x.strip() for x in d_list]  # 리스트 각 요소 strip(),  ["   A", "B   "] from ["A", "B"]
    d_list = [x.strip("\"") for x in d_list]  # 리스트 각 요소 strip("\""),  [""A""] from ["A"]
    d_list = [x.strip("\'") for x in d_list]  # 리스트 각 요소 strip("\'),  ["'A'""] from ["A"]

    logging.debug(f'''d_list={d_list}  ''')

    if 0 == len(d_list):
        ensure_spoken_v2("pnx가 아무것도 입력되지 않았습니다")
        return
    elif 1 == len(d_list):
        ensure_spoken_v2("하나의 pnx로는 머지를 시도할수 없습니다, 여러개의 pnx들을 입력해주세요")
        return
    elif 1 < len(d_list):
        for index, d in enumerate(d_list):
            connected_drives = []
            for drive_letter in string.ascii_uppercase:
                drive_path = drive_letter + ":\\"
                if os.path.exists(drive_path):
                    connected_drives.append(drive_path)
                    if d == drive_path:
                        ensure_spoken_v2("입력된 pnx는 너무 광범위하여, 진행할 수 없도록 설정되어 있습니다")
                        break

        # make_d_leaf(D_EMPTY)

        # indices_to_remove=[]  # remove할 인덱스를 기록할 리스트
        # for index, directory in enumerate(directoryies_):
        #     if is_d(directory):
        #         if is_empty_directory(directory):
        #             ensure_pnx_moved_without_overwrite(pnx_todo=directory, dst=D_EMPTY)
        #             indices_to_remove.append(index)
        # for index in indices_to_remove:
        #     directoryies_.pop(index)

        # for index, directory in enumerate(directoryies_):
        #     if directory == "":
        #         speak_ments("하나 이상의 pnx가 공백으로 입력되었습니다", sleep_after_play=0.65)
        #         return
        #     if not os.path.exists(directory):
        #         speak_ments("하나 이상의 pnx가 존재하지 않습니다", sleep_after_play=0.65)
        #         return

        logging.debug("빈 트리 리프d별로 해체한 뒤 remove")
        f_list_to_move = []
        for index, d in enumerate(d_list):
            for root, _, file_nxs in os.walk(d, topdown=True):
                for f_nx in file_nxs:
                    f_list_to_move.append(rf"{root}\{f_nx}")
        [logging.debug(rf'f_to_move : {f_to_move}') for f_to_move in f_list_to_move]
        logging.debug(f'''type(f_list_to_move)={type(f_list_to_move)}  ''')
        logging.debug(f'''len(f_list_to_move)={len(f_list_to_move)}  ''')
        dst = rf"{os.path.dirname(d_list[0])}\{os.path.basename(d_list[0]).replace("_$merged", "")}_$merged"
        ensure_pnx_made(dst, mode="d")
        logging.debug(rf'dst : {dst}')

        for f_to_move in f_list_to_move:
            ensure_pnx_moved(pnx=f_to_move, d_dst=dst)

        # 이 함수는 캐싱문제를 해결하지 못함.
        def count_f_in_folder(folder_path):
            f_cnt = 0
            for _, _, file_nxs in os.walk(folder_path):
                f_cnt += len(file_nxs)
            return f_cnt

        # 이 함수는 캐싱문제를 해결하지 못함.
        # def count_files_in_folder(folder_path):

        #     file_count=0
        #     with os.scandir(folder_path) as entries:
        #         for entry in entries:
        #             if entry.is_file():
        #                 file_count += 1
        #     return file_count

        # 분명히 f이 들어있는데 개수가 0개로 나오네  캐싱때문에 그럴 수 있어?
        # 운영체제 성능향상을 위한 d정보 캐싱으로 갱신이 안될 수 있음.
        # d를 다른 위치로 이동한 후 다시 이동합니다. 이렇게 하면 f 시스템이 d의 변경을 감지하고 캐시를 갱신할 수 있습니다.
        # current_path=os.getcwd()
        # chdir(os.path.dirname(current_path)) # 부모 d로 이동
        # chdir(current_path)

        # [fail] 분명히 가 틀렸다. 운영체제의 캐싱이 문제가 아닌,
        # 로직을 잘못 만든 것이었다.
        # d 변수를 엉뚱하게 초기화하였기 때문이다.
        # d 를 d_ 로 별도로 호출해서 해소하였다.

        # empty d 리프단위로 분해하여 이동
        while 1:
            d_list_to_move = []
            for index, d in enumerate(d_list):
                for root, d_nx_list, file_nxs in os.walk(d, topdown=False):
                    for d_nx in d_nx_list:
                        f_cnt = count_f_in_folder(rf"{root}\{d_nx}")
                        if f_cnt == 0:
                            d_list_to_move.append(rf"{root}\{d_nx}")

            [logging.debug(sample) for sample in d_list_to_move]
            logging.debug(f'''d_list_to_move={d_list_to_move}''')
            logging.debug(rf'''type(d_list_to_move)={type(d_list_to_move)}''')
            logging.debug(rf'''len(d_list_to_move)={len(d_list_to_move)}''')

            logging.debug(rf'dst : {dst}')
            ensure_pnx_made(dst, mode="d")

            if len(d_list_to_move) == 0:
                break

            for d_to_move in d_list_to_move:
                ensure_pnx_moved(pnx=d_to_move, d_dst=dst)

        for d in d_list:
            gather_empty_d(d_working=d)

        print_success(rf'd 머지를 완료했습니다')
