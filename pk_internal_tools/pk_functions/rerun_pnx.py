import zlib
import win32con
import uuid
import urllib.parse
import urllib
import tqdm
import tomllib
import toml
import toml
import threading
import subprocess
import speech_recognition as sr
import socket
import shutil
import re
import pywintypes

import pyautogui
import os.path
import nest_asyncio
import json
import inspect
import datetime
import colorama
import chardet

import asyncio
from typing import TypeVar, List
from telegram import Bot, Update
from telegram import Bot
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list


from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX

from pathlib import Path
from datetime import timedelta
from datetime import datetime, time
from datetime import date
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from base64 import b64encode
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def rerun_pnx(my_name):  # 종료용이름 시작용이름 이 다름 따로 수집해서 코딩 필요
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    ensure_process_killed_via_taskkill(process_name=my_name)
    ensure_slept(milliseconds=200)  # 최적화 테스트 필요
    cmd = rf'start "{my_name}"'
    ensure_command_executed(cmd=cmd, mode="a")
