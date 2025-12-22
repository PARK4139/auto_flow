import winreg
import urllib.parse
import traceback
import timeit
import subprocess
import colorama
from yt_dlp import YoutubeDL
from selenium.common.exceptions import WebDriverException
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING

from functools import partial as functools_partial
from Cryptodome.Cipher import AES
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.is_d import is_d

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def ensure_process_killed_via_taskkill(process_name=None, pid=None, debug_mode=True):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    if process_name is not None or pid is not None:
        logging.debug(rf"{func_n}() 동작 조건 충족")
    else:
        logging.debug(rf"{func_n}() 동작 조건 불충족")
        return

    cmd = None
    if process_name != None:
        cmd = f'taskkill /f /im {process_name}"'
    elif pid != None:
        cmd = f'taskkill /f /pid {pid}"'
    ensure_command_executed(cmd=cmd)
