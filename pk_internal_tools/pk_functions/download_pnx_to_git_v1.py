import zipfile
import winreg

import win32con
import win32con
import urllib.parse
import urllib
import undetected_chromedriver as uc
import traceback
import tqdm
import tomllib
import toml
import tarfile
import sys
import string
import speech_recognition as sr
import socket
import shutil
import secrets


import pythoncom
import pyglet
import pygetwindow
import pyaudio
import platform
import os.path
import os
import numpy as np
import nest_asyncio
import json
import ipdb
import inspect
import functools
import datetime
import cv2
import colorama
import colorama

from urllib.parse import quote, urlparse
from urllib.parse import quote
from tkinter import UNDERLINE
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from pytube import Playlist
from PySide6.QtWidgets import QApplication
from pynput import mouse
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding


from PIL import Image, ImageFilter
from PIL import Image
from pathlib import Path
from paramiko import SSHClient, AutoAddPolicy
from moviepy import VideoFileClip
from functools import partial
from functools import lru_cache
from dirsync import sync
from datetime import timedelta
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def download_pnx_to_git_v1(d_working, git_repo_url, commit_msg, branch_n):
    import traceback
    from colorama import init as pk_colorama_init

    ensure_pk_colorama_initialized_once()

    try:
        if not is_pnx_existing(pnx=d_working):
            ensure_pnx_made(pnx=d_working, mode='d')

        d_git = rf"{d_working}/.git"

        if not is_pnx_existing(pnx=d_git):
            std_list = ensure_command_executed(f'git clone -b {branch_n} {git_repo_url} {d_working}')
            debug_state_for_py_data_type('%%%CLONE%%%', std_list)

            if any("fatal:" in line.lower() for line in std_list):
                logging.debug(f"Git clone 실패: {std_list}")
                return
        else:
            os.chdir(d_working)
            std_list = ensure_command_executed(f'git pull origin {branch_n}')
            debug_state_for_py_data_type('%%%PULL%%%', std_list)

            if any("fatal:" in line.lower() for line in std_list):
                logging.debug(f"Git pull 실패: {std_list}")
                return

        logging.debug(f"Git 작업 완료: {d_working} ")

    except Exception:
        logging.debug(f"{traceback.format_exc()} ")
