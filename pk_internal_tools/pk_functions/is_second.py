import zlib
import zipfile
import winreg

import win32con
import win32con
import win32com.client
import traceback
import toml
import toml
import sys
import string
import speech_recognition as sr
import socket

import pickle
import paramiko
import pandas as pd
import numpy as np
import mutagen
import math
import ipdb
import inspect
import importlib
import functools
import easyocr
import clipboard
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs, unquote
from urllib.parse import quote, urlparse
from urllib.parse import quote
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from queue import Queue, Empty
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from PIL import Image
from pathlib import Path
from os.path import dirname
from os import path
from functools import partial as functools_partial
from functools import lru_cache
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from bs4 import BeautifulSoup
from base64 import b64encode

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE



def is_second(ss):
    from datetime import datetime
    return datetime.today().second == int(ss)
