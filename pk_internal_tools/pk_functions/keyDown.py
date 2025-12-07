
import webbrowser
import urllib.parse
import tqdm
import tomllib
import tarfile
import subprocess
import sqlite3
import socket, time
import socket
import random
import pywintypes
import pyglet
import pygetwindow
import pandas as pd
import mutagen
import keyboard
import colorama
import calendar

from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from PySide6.QtWidgets import QApplication
from pynput import mouse
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
import logging
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f

from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.performance_logic import ensure_seconds_measured, pk_measure_memory
from pathlib import Path
from os.path import dirname
from os import path
from moviepy import VideoFileClip
from functools import lru_cache
from fastapi import HTTPException
from enum import Enum
from cryptography.hazmat.primitives import padding
from concurrent.futures import ThreadPoolExecutor
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_objects.pk_etc import PkFilter, PK_UNDERLINE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

import logging


def keyDown(key: str):
    import inspect
    import pyautogui
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    pyautogui.keyDown(key)
