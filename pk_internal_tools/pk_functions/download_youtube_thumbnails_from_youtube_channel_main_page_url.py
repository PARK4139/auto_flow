import winreg

import win32con
import tomllib
import threading
import tarfile
import socket
import shutil
import psutil
import os
import nest_asyncio
import importlib

import asyncio
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list

from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext


from functools import partial as functools_partial
from functools import partial
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def download_youtube_thumbnails_from_youtube_channel_main_page_url(youtube_channel_main_page_url):
    import os

    youtube_video_url_list = get_videos_urls_from_youtube_channel_main_page(
        youtube_channel_main_page_url=youtube_channel_main_page_url)
    channel_n = get_channel_n(channel_url=youtube_channel_main_page_url)
    d_dst = rf'{D_PK_WORKING_EXTERNAL}/thumbnails/{channel_n}'
    # dst = get_pnx_unix_style(pnx=dst)
    d_dst = Path(d_dst)
    ensure_pnx_made(d_dst, mode="d")
    cnt = 0
    for youtube_video_url in youtube_video_url_list:
        cnt += 1
        f_jpg = os.path.join(d_dst, f"{channel_n}_thumbnail_maxresdefault_{cnt}.jpg")
        download_youtube_thumbnail(youtube_video_url=youtube_video_url, f_dst_jpg=f_jpg)
