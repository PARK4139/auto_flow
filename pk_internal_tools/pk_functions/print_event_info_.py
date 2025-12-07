import zipfile
import yt_dlp

import toml
import subprocess, time
import sqlite3
import socket, time
import re
import random

import pygetwindow
import pyaudio
import numpy as np
import nest_asyncio
import colorama
import clipboard
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


from PIL import Image
from os.path import dirname
from dirsync import sync
from datetime import timedelta
from colorama import init as pk_colorama_init
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_etc import PkFilter, PK_UNDERLINE
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style

from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def print_event_info_(event, thing_curious):
    import inspect
    """
        jhp_debugger.print_event_info_(event)
        # └>call sample
    """
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    print(str(event))
    # print(event.type())
    # if type(thing_curious)==str:
    #     print('{{mkr}}')
    # if type(thing_curious)==list:
    #     print(thing_curious[str(event.type())])
    # if type(thing_curious) == tuple:
    #     print('{{mkr}}')
