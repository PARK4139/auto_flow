import zlib
import win32con
import undetected_chromedriver as uc
import tomllib
import threading
import sys
import sqlite3
import pyautogui
import functools
import calendar

from selenium.webdriver.chrome.options import Options
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing


from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE

from PIL import Image
from os import path
from dirsync import sync
from cryptography.hazmat.primitives import padding
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from base64 import b64encode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_functions.is_d import is_d

from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def parse_youtube_video_id(url):
    import inspect
    import urllib
    from urllib.parse import quote

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    keyword_shorts = '/shorts/'
    keyword_slash = '/'
    if keyword_shorts in url:
        youtube_video_id = url.split(keyword_shorts)[1]
        youtube_video_id = youtube_video_id.split(keyword_slash)[0]
        logging.debug(rf'''youtube_video_id="{youtube_video_id}"  ''')
        return youtube_video_id
    query = urllib.parse.urlparse(url=url)
    # logging.debug(query.scheme)
    # logging.debug(query.netloc)
    # logging.debug(query.hostname)
    # logging.debug(query.port)
    # logging.debug(query._replace(fragment="").geturl())
    # logging.debug(query)
    # logging.debug(query["v"][0])
    if query.hostname == 'youtu.be':
        logging.debug(rf'''query.path[1:]="{query.path[1:]}"  ''')
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            logging.debug(rf'''p['v'][0]="{p['v'][0]}"  ''')
            return p['v'][0]
        if query.path[:7] == '/embed/':
            logging.debug(rf'''query.path.split('/')[2]="{query.path.split('/')[2]}"  ''')
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            logging.debug(rf'''query.path.split('/')[2]="{query.path.split('/')[2]}"  ''')
            return query.path.split('/')[2]
