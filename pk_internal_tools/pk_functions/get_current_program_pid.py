
import urllib
import tomllib
import toml
import timeit
import sqlite3
import pyaudio
import pickle
import mutagen
import inspect
import importlib
import functools
import easyocr
import calendar
import asyncio
from typing import TypeVar, List
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from queue import Queue, Empty
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pathlib import Path
from passlib.context import CryptContext
from moviepy import VideoFileClip
from fastapi import HTTPException
from enum import Enum
from cryptography.hazmat.backends import default_backend
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pathlib import Path

import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def get_current_program_pid():
    import inspect
    import subprocess

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    pro = subprocess.check_output(
        rf'powershell (Get-WmiObject Win32_Process -Filter ProcessId=$PID).ParentProcessId', shell=True).decode(
        'utf-8')  # 실험해보니 subprocess.check_output(cmd,shell=True).decode('utf-8') 코드는 프로세스가 알아서 죽는 것 같다. 모르겠는데 " " 가 있어야 동작함
    lines = pro.split('\n')
    pids = []
    for line in lines:
        if "" != line.strip():
            pid = line
            pids.append(pid)
            logging.debug(f'pid: {pid}')
    return pids
