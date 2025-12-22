import win32con
import uuid
import urllib.parse
import tqdm
import tomllib
import toml
import tarfile
import shlex
import secrets
import re

import pyautogui
import platform
import nest_asyncio
import mutagen
import math
import json
import functools
import colorama
from webdriver_manager.chrome import ChromeDriverManager
from telethon import TelegramClient, events
from telegram import Bot, Update
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from pynput import mouse
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed


from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext



from PIL import Image, ImageFilter
from PIL import Image
from pathlib import Path
from dirsync import sync
from datetime import datetime, timedelta
from colorama import init as pk_colorama_init
from base64 import b64encode


from pathlib import Path
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

import logging


def get_pnx_validated(pnx):
    import os
    pnx = pnx.strip()
    pnx = Path(pnx)
    if not os.path.exists(pnx):
        logging.debug(f"경로가 존재하지 않습니다: {pnx}")
        raise
    return pnx
