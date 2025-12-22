import yt_dlp
import urllib.parse
import urllib
import undetected_chromedriver as uc
import tomllib
import tomllib
import toml
import socket, time
import shlex
import secrets
import re


import pygetwindow
import pyautogui
import pickle
import nest_asyncio
import keyboard
import hashlib
import functools
import colorama
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from pynput import mouse

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front

from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


from passlib.context import CryptContext
from gtts import gTTS
from functools import partial
from enum import Enum
from dataclasses import dataclass
from Cryptodome.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor
from bs4 import ResultSet
from pathlib import Path
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f

from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_target_flash_image_saved():
    # flash image를 만들때 특정 192.168.2.114/22 로 eth0(Wired connection 1 and 3) 로 셋업을 해둬서 XC를 headless 모드로 셋팅(화면 볼필요 없이, ssh로 바로 접속)

    # if xc:
    #     jetpack_version
    # # todo : flash image 생성
    # #  추후에 4.6.6 이 필요하다면, flash image 새로생성하자
    # #  영상처리제어기 headless 로 flash 를 위한 선행작업,
    # #  꼭 ip를 미리 192.168.10.114 로 셋팅을 해두자. headless 로 flash 를 하기 위해서

    # EVM_flash_241125.img
    # EVM_flash_241125.img.raw
    # cp EVM_flash_241125.img ~/Download
    # scp EVM_flash_241125.img park4139@x.x.x.x:/home/pk_system/    # send to galaxybook4_junghoonpark

    # to local
    # to nas
    # to nas
    pass
