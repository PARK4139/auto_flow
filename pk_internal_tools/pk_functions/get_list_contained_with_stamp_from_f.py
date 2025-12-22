import zipfile
import win32con
import subprocess, time
import string
import requests

import pythoncom
import pygetwindow
import psutil
import mutagen
import datetime
from zipfile import BadZipFile
from tkinter import UNDERLINE
from PySide6.QtWidgets import QApplication
from prompt_toolkit.styles import Style


from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from PIL import Image
from os import path
from functools import lru_cache
from base64 import b64decode
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_list_contained_with_stamp_from_f(f, STAMP):
    list_filtered = get_list_from_f(f=f)
    logging.debug(f'''STAMP={STAMP}  ''')
    list_filtered = get_list_contained_element(working_list=list_filtered, prefix=rf"{STAMP} ")
    logging.debug(f'''list_filtered={list_filtered}  ''')
    list_filtered = get_list_deduplicated(working_list=list_filtered)
    logging.debug(f'''list_filtered={list_filtered}  ''')
    list_filtered = get_list_removed_element_contain_prompt(working_list=list_filtered, prompt="#")
    logging.debug(f'''list_filtered={list_filtered}  ''')
    list_filtered = get_list_replaced_element_from_str_to_str(working_list=list_filtered, from_str=STAMP, to_str="")
    logging.debug(f'''list_filtered={list_filtered}  ''')
    list_filtered = get_list_striped_element(working_list=list_filtered)
    logging.debug(f'''list_filtered={list_filtered}  ''')
    return list_filtered
