

import tomllib
import threading
import secrets
import pywintypes
import pyglet
import os
import hashlib
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from selenium.webdriver.common.keys import Keys
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
import logging

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, d_pk_root_hidden
from passlib.context import CryptContext
from os import path
from functools import partial as functools_partial
from dirsync import sync
from datetime import datetime
from colorama import init as pk_colorama_init
from bs4 import BeautifulSoup

from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def is_empty_tree(d):
    import os

    logging.debug(f"d={d}  ")

    try:
        with os.scandir(d) as entries:
            for entry in entries:
                if entry.is_file():
                    logging.debug(rf"is not empty d {d}")
                    return 0
        logging.debug(rf"is not empty d 있습니다.{d}")
        return 1
    except:
        # logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        return 0
