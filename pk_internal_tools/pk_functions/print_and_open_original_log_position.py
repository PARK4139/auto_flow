import zipfile

import webbrowser
import tqdm
import tomllib
import shutil
import shlex
import pygetwindow
import pyautogui
import psutil
import platform
from zipfile import BadZipFile
from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_etc import PkFilter
from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from functools import partial as functools_partial
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def print_and_open_original_log_position(area_id, course_id, vehicle_id, steering_date=None):
    import inspect

    # 매개변수가 None이면 빈 문자열을 할당
    foo = "????????"
    vehicle_id = vehicle_id if vehicle_id is not None else foo
    area_id = area_id if area_id is not None else foo
    steering_date = steering_date if steering_date is not None else foo
    course_id = course_id if course_id is not None else foo

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug(rf'''{func_n}()  ''')
    data_required = {}
    data_required["차량"] = vehicle_id
    data_required["지역"] = area_id
    data_required["주행일자"] = steering_date
    data_required["코스"] = course_id

    # def get_origin_log_file_name(issue_file_name):
    #     # 정규식 패턴 정의: "_숫자(최대 2자리)_VIDEO"
    #     pattern = r"_\d{1,2}_VIDEO"
    #     original_filename = re.sub(pattern, "", issue_file_name)
    #     return original_filename

    # 정의
    # issue_file_name = issue_log_index_data["_f_ 위치"].split('/')[-1]
    # origin_log_file_name = get_origin_log_file_name(issue_file_name)
    original_log_position = rf"\\192.168.1.33\02_Orignal\{data_required['차량']}\{data_required['지역']}\{data_required['주행일자']}\{data_required['코스']}"
    logging.debug(rf'''original_log_position="{original_log_position}"  ''')
    if foo not in original_log_position:
        ensure_command_executed(cmd=rf'explorer "{original_log_position}" ')
    else:
        logging.debug(f'''수집한 오리지널 로그_f_의 경로가 온전하지 않습니다.''')
