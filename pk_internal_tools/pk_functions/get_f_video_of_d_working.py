import zipfile
import winreg

import undetected_chromedriver as uc
import traceback
import tomllib
import tomllib
import socket
import pyaudio
import mysql.connector
import asyncio
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT

from os.path import dirname
from moviepy import VideoFileClip
from functools import partial
from functools import lru_cache
from enum import Enum
from colorama import init as pk_colorama_init
from collections import Counter

from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def get_f_video_of_d_working(d_working, ext_list_allowed):
    import os
    logging.debug(f'''d_working={d_working} extension_list_allowed={ext_list_allowed} ''')
    if not os.path.exists(d_working):
        logging.debug(f"d_working does not exists {d_working}")
    if os.path.exists(d_working):
        for f_nx in os.listdir(d_working):
            f = os.path.join(d_working, f_nx)
            ext = os.path.splitext(f)[1].lower()
            if not ext in ext_list_allowed:
                # logging.debug(f"f={f}, ext={ext}, 조건 만족 여부: {ext in extensions}")
                pass
    f_list_of_d_working = [os.path.join(d_working, f) for f in os.listdir(d_working)]
    logging.debug(f'''len(f_list_of_d_working)={len(f_list_of_d_working)}  ''')
    media_files_allowed = [
        f for f in f_list_of_d_working
        if os.path.splitext(f)[1].lower() in ext_list_allowed
           and not any(keyword in os.path.basename(f).lower() for keyword in ["seg", "temp"])
    ]
    logging.debug(f'''len(media_files_allowed)={len(media_files_allowed)}  ''')
    if media_files_allowed:
        media_files_allowed.sort()
        return media_files_allowed[0]
    else:
        logging.debug("조건에 맞는 f 없습니다.")
        return None
