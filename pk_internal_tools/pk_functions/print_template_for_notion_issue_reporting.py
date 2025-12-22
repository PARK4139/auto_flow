import zlib

import toml
import string
import shutil
import pyaudio
import platform
import mysql.connector
import inspect
import cv2
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from PIL import Image
from functools import partial
from dirsync import sync
from collections import Counter
from bs4 import BeautifulSoup

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def print_template_for_notion_issue_reporting(line_order, issues_list_csv):
    logging.debug(rf'''노션 이슈발생 템플릿  ''')
    collect_row_data = collect_row_data_from_csv(line_order=line_order, issues_list_csv=issues_list_csv)
    logging.debug(string=f'''차량 : {collect_row_data["차량"]}''')
    logging.debug(string=f'''지역 : {collect_row_data["지역"]}''')
    logging.debug(string=f'''코스 : {collect_row_data["코스"]}''')
    logging.debug(string=f'''운전자 : {collect_row_data['Crew']}''')
    # logging.debug(string=f'''문제점 상세 : \n{collect_row_data["문제점 상세"].replace("\n\n","\n")}''')
    logging.debug(string=f'''문제점 상세 : \n{collect_row_data["문제점 상세"].replace("\n", "")}''')
    logging.debug(string=f'''''')
    logging.debug(string=f'''SW 버전 : {collect_row_data["SW 버전"]}''')
    f위치 = collect_row_data["_f_ 위치"]
    if isinstance(f위치, float):
        f위치 = ""
    logging.debug(string=f'''_f_명 : {f위치}''')
