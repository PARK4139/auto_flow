import zipfile
import yt_dlp

import win32con
import win32com.client
import webbrowser
import urllib.parse
import undetected_chromedriver as uc
import traceback
import tqdm
import tomllib
import tomllib
import timeit
import time
import tarfile
import sys
import subprocess
import socket
import secrets
import requests
import re
import random
import pywintypes
import pythoncom
import pyglet
import pygetwindow
import platform
import pickle
import paramiko
import os, inspect
import mutagen
import inspect
import hashlib
import functools
import easyocr
import datetime
import colorama
import colorama
import clipboard
import chardet
import calendar
from zipfile import BadZipFile
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from tkinter import UNDERLINE
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts




from PIL import Image, ImageFont, ImageDraw
from PIL import Image, ImageFilter
from passlib.context import CryptContext
from os.path import dirname
from os import path
from mysql.connector import connect, Error
from functools import partial as functools_partial
from functools import partial
from dirsync import sync
from datetime import datetime, timedelta
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from collections import Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def should_i_search_to_google():
    # todo : ref : as gui : demerit : slow
    # import system_object.static_logic
    # txt_clicked, function, txt_written = should_i_do(
    #     string=rf"can i search contents dragged to google?",
    #     btns=[system_object.static_logic.POSITIVE, system_object.static_logic.NEGATIVE],
    #     function=partial(ask_to_google, question=question),
    #     auto_click_negative_btn_after_seconds=30,
    #     title=f" ",
    #     input_box_mode=True,
    #     input_box_text_default=question,
    # )
    # if txt_clicked == system_object.static_logic.NEGATIVE:
    #     logging.debug(f'''{system_object.static_logic.NEGATIVE} pressed  ''')
    #     return
    # if txt_clicked == system_object.static_logic.POSITIVE:
    #     logging.debug(f'''txt_clicked={txt_clicked}  ''')
    #     logging.debug(f'''txt_written={txt_written}  ''')
    #     function()

    # todo : ref : as cli
    txt_written = should_i_do_cli(
        title=rf"can i search contents dragged to google?",
        search_keyword_default="",
    )
    txt_written = txt_written.strip()
    if txt_written != "":
        ask_to_google(txt_written)
