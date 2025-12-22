


import win32con
import win32con
import win32com.client
import webbrowser
import urllib.parse
import undetected_chromedriver as uc
import tqdm
import tomllib
import tomllib
import toml
import toml
import time
import threading
import tarfile
import sys
import subprocess
import string
import speech_recognition as sr
import socket
import shutil
import requests
import re
import random


import pythoncom
import pygetwindow
import pyautogui
import pyaudio
import psutil
import platform
import paramiko
import pandas as pd
import os, inspect
import os
import nest_asyncio
import mutagen
import math
import keyboard
import json
import ipdb
import inspect
import importlib
import functools
import easyocr
import cv2
import colorama
import clipboard

from yt_dlp import YoutubeDL
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from urllib.parse import quote, urlparse
from urllib.parse import quote
from typing import TypeVar, List
from tkinter import UNDERLINE
from telethon import TelegramClient, events
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from queue import Queue, Empty
from PySide6.QtWidgets import QApplication
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed




from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, D_PK_ROOT_HIDDEN
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from PIL import Image, ImageFilter
from paramiko import SSHClient, AutoAddPolicy
from os.path import dirname
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from gtts import gTTS
from functools import partial as functools_partial
from functools import partial
from fastapi import HTTPException
from datetime import timedelta
from datetime import datetime, timedelta
from datetime import datetime, time
from datetime import date
from dataclasses import dataclass
from Cryptodome.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from collections import Counter
from bs4 import ResultSet
from bs4 import BeautifulSoup
from base64 import b64encode
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
# 
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.is_d import is_d

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def is_only_eng_and_no(text):
    import re
    pattern = "^[0-9a-zA-Z]+$"
    if re.search(pattern, text):
        return 1
    else:
        return 0
