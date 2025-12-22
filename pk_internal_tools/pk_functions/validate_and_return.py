import zipfile
import winreg

import webbrowser
import urllib
import undetected_chromedriver as uc
import tomllib
import toml
import string
import shutil
import pythoncom
import platform
import paramiko
import mysql.connector
import mutagen
import functools
import colorama
import chardet
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from urllib.parse import quote
from selenium.webdriver.chrome.options import Options
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed


from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title

from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from moviepy import VideoFileClip
from Cryptodome.Random import get_random_bytes
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def validate_and_return(value: str):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    try:
        logging.debug(rf'[벨리데이션 테스트 결과] [value={value}] [type(value)={type(value)}] [len(value)={len(value)}]')
    except Exception as e:
        pass
    if value is None:
        logging.debug(rf'[벨리데이션 테스트 결과] [value=None]')
        return 0
    if value == "":
        logging.debug(rf'[벨리데이션 테스트 결과] [value=공백]')
        return 0
    # if 전화번호만 같아 보이는지
    # if 특수문자만 같아 보이는지
    return value
