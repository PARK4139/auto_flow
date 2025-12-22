import zipfile
import winreg

import uuid
import urllib.parse
import traceback
import toml
import timeit
import time
import threading
import tarfile
import subprocess
import socket, time
import socket
import shutil
import re
import pywintypes
import pythoncom
import pyglet
import pyaudio
import psutil
import pandas as pd
import os, inspect
import numpy as np
import nest_asyncio
import ipdb
import importlib
import easyocr
import colorama
import colorama

import asyncio
from yt_dlp import YoutubeDL
from urllib.parse import quote
from telegram import Bot, Update
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from pynput import mouse
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list


from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


from PIL import Image, ImageFilter
from pathlib import Path
from mutagen.mp3 import MP3
from gtts import gTTS
from fastapi import HTTPException
from enum import Enum
from datetime import datetime, timedelta
from datetime import datetime
from dataclasses import dataclass
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from bs4 import ResultSet
from base64 import b64encode
from base64 import b64decode

from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
# 

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def report_target_test_report(issue_code, solution_code):
    # issue discovered
    pass
