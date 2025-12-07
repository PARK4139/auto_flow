

import win32com.client
import uuid
import urllib.parse
import urllib
import toml
import sys
import string
import shutil

import easyocr
import datetime
import calendar
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_state_printed import ensure_state_printed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pathlib import Path
from passlib.context import CryptContext
from os import path
from enum import Enum
from dirsync import sync
from datetime import datetime
from datetime import date
from dataclasses import dataclass
from Cryptodome.Random import get_random_bytes


from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style

import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def save_cash_to_f_pkl(F_CACHE, status):
    import time
    import pickle
    with open(F_CACHE, "wb") as f:
        pickle.dump({
            "timestamp": time.time(),
            "status": status
        }, f)
