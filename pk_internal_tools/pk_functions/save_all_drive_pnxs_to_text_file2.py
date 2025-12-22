


import win32con
import win32com.client
import uuid
import urllib.parse
import tqdm
import toml
import toml
import socket, time
import requests
import random

import pythoncom
import psutil
import platform
import pickle
import pandas as pd
import os, inspect
import nest_asyncio
import mysql.connector
import mutagen
import json
import importlib
import hashlib
import colorama

from urllib.parse import urlparse
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from seleniumbase import Driver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from pynput import mouse
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_state_printed import ensure_state_printed
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from PIL import Image, ImageFilter
from PIL import Image
from passlib.context import CryptContext
from os.path import dirname
from functools import partial as functools_partial
from functools import lru_cache
from fastapi import HTTPException
from datetime import timedelta
from datetime import datetime
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from collections import Counter
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def save_all_drive_pnxs_to_text_file2():  # 루프 수정필요 # 이 함수는 거의 필요 없을 것 같다. 관심_d_만 확인하는 것으로 충분해 보인다.
    import os.path
    import string

    import os

    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    from pk_internal_tools.pk_objects.pk_directories import D_PK_CONFIG
    f_func_n_txt = D_PK_CONFIG / f'{func_n}.txt'
    ensure_pnx_made(pnx=f_func_n_txt, mode="item")

    # if not is_window_opened(window_title=f_func_n_txt):
    #     run_pnx_via_explorer_exe(f_func_n_txt, debug_mode=False)

    # n. 특정 경로를 제외할 텍스트 f에서 경로 읽어오기
    def load_pnxs_exclude(file_path):

        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        exclude_paths = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    exclude_paths.add(line.strip())
        except PermissionError as e:
            print(f"PermissionError: {e}. Check if the item is accessible and you have the right permissions.")
        except Exception as e:
            print(f"Error opening item {file_path}: {e}")
        return exclude_paths

    # n. 모든 드라이브에서 f 목록 가져오기
    def get_drives_connected():

        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        logging.debug(rf'''drives="{drives}"  ''')
        return drives

    # n. 드라이브에서 f 검색하고 처리하기
    def list_files_in_drives(exclude_paths_txt):
        import inspect
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        exclude_paths = load_pnxs_exclude(exclude_paths_txt)
        drives = get_drives_connected()
        cnt = 0
        pnxs = []
        limit = 10000
        cnt_files = limit
        cnt_txt_files = 0
        temp = set()
        # 모든 드라이브에서 f 탐색
        for drive in drives:
            logging.debug(rf'''drive="{drive}"  ''')
            for foldername, subfolders, file_names in os.walk(drive):
                for file_name in file_names:
                    file_pnx = os.path.join(foldername, file_name)
                    # logging.debug(string = rf'''file_pnx="{file_pnx}"  ''')
                    cnt_files = cnt_files - 1
                    pnxs.append(file_pnx)
                    if cnt_files == 0:
                        # logging.debug(string = rf'''file_pnx="{file_pnx}"  ''')
                        cnt_files = limit
                        cnt_txt_files = cnt_txt_files + 1
                        # logging.debug(string = rf'''cnt_txt_files="{cnt_txt_files}"  ''')
                        output_pnx_txt_before = D_PK_CONFIG / f"{func_n}_{cnt_txt_files - 1}.txt"
                        temp = get_list_from_f(f=output_pnx_txt_before)
                        if None != temp:
                            if 0 == len(temp):
                                cnt_txt_files = cnt_txt_files - 1

                        output_pnx_txt = D_PK_CONFIG / f"{func_n}_{cnt_txt_files}.txt"
                        # logging.debug(string = rf'''output_pnx_txt="{output_pnx_txt}"  ''')
                        # if any(exclude_path in file_pnx for exclude_path in exclude_paths):
                        #     continue
                        with open(output_pnx_txt, 'w', encoding='utf-8') as f:
                            for pnx in pnxs:
                                cnt = cnt + 1
                                # temp.add(rf"{pnx.split("\\")[0]}\{pnx.split("\\")[1]}")
                                # print(temp)
                                for exclude_path in exclude_paths:
                                    if exclude_path in pnx:
                                        break
                                else:
                                    if not pnx.strip() == "":
                                        f.write(f'{pnx}\n')
                                        logging.debug(                                text_working=rf'''cnt="{cnt}" pnxs="{pnx}" output_pnx_txt="{output_pnx_txt}"  ''')
                                    else:
                                        logging.debug(f'''없다''')
        logging.debug(rf'''temp="{temp}"  ''')

    # exec
    exclude_paths_txt = D_PK_CONFIG / f'{func_n}_exclude_paths.txt'
    ensure_pnx_made(pnx=exclude_paths_txt, mode='item')
    list_files_in_drives(exclude_paths_txt)
