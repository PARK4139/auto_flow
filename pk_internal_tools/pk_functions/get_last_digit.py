import win32con
import toml
import toml
import timeit
import random
import cv2
import colorama
import clipboard
from urllib.parse import quote
from selenium.webdriver.chrome.service import Service
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
import logging


from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT


from PIL import Image
from os import path
from functools import partial as functools_partial
from datetime import timedelta
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor
from colorama import init as pk_colorama_init
from collections import Counter
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_last_digit(prompt):
    # todo : get_front_digit() 도 만드는 게 좋겠다.
    import inspect
    import re

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    match = re.search(r'\d+\b$', prompt.strip())  # 끝에 위치한 모든 연속된 숫자를 찾음
    if match:
        return match.group(0)  # 매칭된 숫자 반환
    return "00"  # 숫자를 찾지 못한 경우 기본값 "00" 반환
