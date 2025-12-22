import win32con
import string
import sqlite3
import re
import random
import os.path
import keyboard
from urllib.parse import urlparse
from urllib.parse import quote
from selenium.webdriver.chrome.options import Options
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from PIL import Image
from os.path import dirname
from os import path
from gtts import gTTS
from functools import partial
from fastapi import HTTPException
from enum import Enum
from datetime import datetime
from base64 import b64decode

from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def set_wake_up_next_HH_mm(HH, mm):
    """
    다음으로 오는 HH:mm 시각에 컴퓨터를 깨우도록 스케줄링합니다.
    - 이미 HH:mm이 지났다면 자동으로 다음 날 같은 시각으로 설정합니다.
    """
    from datetime import datetime, timedelta
    now = datetime.now()

    # 오늘 날짜의 HH:mm 만들기 (초는 0으로 설정)
    target_time = datetime(now.year, now.month, now.day, HH, mm, 0)

    # 이미 HH:mm이 지났다면, 다음 날로 +1일
    if target_time <= now:
        target_time += timedelta(days=1)

    # schtasks에서 "HH:MM" 포맷으로 쓰기 위해 시분만 추출
    wake_time_str = target_time.strftime("%H:%M")

    # schtasks 명령어 구성
    # /sc once 로 한 번만 exec
    # /st HH:MM 으로 exec  시각 지정
    # /f : 덮어쓰기
    # /it : 인터랙티브 모드
    task_name = "WakeComputer"
    cmd = f'schtasks /create /tn "{task_name}" /tr "cmd /c exit" /sc once /st {wake_time_str} /f /it'

    # 실제 os 명령 exec  함수(sample: os.system) 대신 아래처럼 가정
    logging.debug(f'{"[ ️ ]"} CMD: {cmd}')
    # sample: os.system(cmd)

    # 현재 시각과 예약 시각 출력
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    readable_target_str = target_time.strftime("%Y-%m-%d %H:%M:%S")
    logging.debug(f'현재 시간: {current_time_str}, 컴퓨터 깨우기 예약 시각: {readable_target_str} ')
