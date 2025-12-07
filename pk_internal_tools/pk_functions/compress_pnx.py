

import win32con
import sqlite3
import secrets
import mutagen
import json
import cv2
from selenium.common.exceptions import WebDriverException
import logging
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from os.path import dirname
from functools import partial
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


def compress_pnx(src, dst, with_timestamp=1):
    return compress_pnx_via_rar(src=src, dst=dst, with_timestamp=with_timestamp)
