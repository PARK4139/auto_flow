import win32con
import toml
import time
import tarfile
import string
import sqlite3
import pickle
import os.path
import mysql.connector
import ipdb
import inspect
import importlib
from selenium.webdriver.common.action_chains import ActionChains
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from passlib.context import CryptContext
from mutagen.mp3 import MP3
from gtts import gTTS
from datetime import timedelta
from Cryptodome.Random import get_random_bytes
from bs4 import ResultSet
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ask_to_google(question: str):
    # str preprocess
    question = question.replace(" ", "+")
    question = question.strip()

    # search in google
    cmd = f'explorer "https://www.google.com/search?q={question}"  >NUL'
    ensure_command_executed(cmd=cmd)
    logging.debug(f'''{cmd}  ''')

    # move window to front
    window_title_seg = rf"{question} - Google"
    while 1:
        ensure_window_to_front(window_title_seg)
        if ensure_window_to_front(window_title_seg):
            break
