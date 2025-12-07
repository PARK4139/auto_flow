

import tomllib
import shlex
import pygetwindow
import psutil
import pandas as pd
import nest_asyncio
import easyocr
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE

from os import path
from base64 import b64encode
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def download_issue_log_f(issue_log_index_data, original_log=False):
    import re

    # 전처리
    if isinstance(issue_log_index_data["_f_ 위치"], float):
        issue_log_index_data["_f_ 위치"] = ""

    issue_file_name = issue_log_index_data["_f_ 위치"].split('/')[-1]

    def get_origin_log_file_name(issue_file_name):
        # 정규식 패턴 정의: "_숫자(최대 2자리)_VIDEO"
        pattern = r"_\d{1,2}_VIDEO"
        original_filename = re.sub(pattern, "", issue_file_name)
        return original_filename

    origin_log_file_name = get_origin_log_file_name(issue_file_name)
    issue_log_index_data["주행일자"] = issue_log_index_data["_f_ 위치"].split('/')[0]
    issue_log_index_data["_f_ 위치"] = issue_log_index_data["_f_ 위치"].replace("/", f"\\")

    src = rf"\\192.168.1.33\01_Issue\{issue_log_index_data["_f_ 위치"]}"
    logging.debug(rf'''src="{src}"  ''')
    if original_log == True:
        src = rf"\\192.168.1.33\02_Orignal\{issue_log_index_data["차량"]}\{issue_log_index_data["지역"]}\{issue_log_index_data["주행일자"]}\{issue_log_index_data["코스"]}\{origin_log_file_name}"
        logging.debug(rf'''src="{src}"  ''')
        return

    # pause()
    dst = rf"C:\log"
    cmd = rf"copy {src} {dst}"
    src_nx = get_nx(pnx=src)
    src_new = rf"{dst}\{src_nx}"

    while 1:
        if is_pnx_existing(pnx=src_new):
            logging.debug(rf'''{src_new} 가 이미 있습니다."  ''')
            break
        else:
            if not is_pnx_existing(pnx=src_new):
                ensure_command_executed(cmd=cmd, mode="a")
                logging.debug(rf'''이슈데이터 다운로드 완료 "{src_new}"  ''')
                return
