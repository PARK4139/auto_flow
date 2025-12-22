import toml
import string
import shutil
import shlex
import requests
import pywintypes
import nest_asyncio
import importlib
import hashlib

from urllib.parse import quote, urlparse
from selenium.webdriver.chrome.options import Options
from PySide6.QtWidgets import QApplication
from prompt_toolkit.styles import Style

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from moviepy import VideoFileClip
from gtts import gTTS
from dirsync import sync
from bs4 import ResultSet
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def generate_random_address_kor():
    import random

    street = random.choice(
        ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도', '전라북도',
         '전라남도', '경상북도', '경상남도', '제주특별자치도'])
    city = random.choice(
        ['서초구', '강남구', '송파구', '강동구', '관악구', '강서구', '영등포구', '구로구', '금천구', '양천구', '마포구', '서대문구', '은평구', '동작구', '광진구',
         '성동구', '중랑구', '동대문구', '성북구', '강북구', '도봉구', '노원구', '중구', '종로구'])
    dong = random.choice(
        ['반포동', '삼성동', '청담동', '논현동', '압구정동', '서초동', '잠실동', '천호동', '신림동', '구로동', '영등포동', '신도림동', '여의도동', '목동', '신정동',
         '신촌동', '홍대입구동', '이태원동', '성수동', '왕십리동'])
    street_number = random.randint(1, 200)
    building_name = random.choice(['아파트', '빌라', '주택', '오피스텔'])
    return f"{street} {city} {dong} {street_number}-{random.randint(1, 20)}, {building_name}"
    # return random.choice([generate_random_address_kor() for _ in range(100)])
