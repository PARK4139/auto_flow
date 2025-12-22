

import win32com.client
import timeit
import sys
import requests
import pywintypes
import keyboard
from telegram import Bot, Update
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PySide6.QtWidgets import QApplication
from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern

from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from PIL import Image
from os.path import dirname
from enum import Enum
from datetime import timedelta
from cryptography.hazmat.backends import default_backend
from colorama import init as pk_colorama_init
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS

from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


def delete_empty_d_list():
    import os

    def _delete_tree(root_path: str):
        """
        주어진 디렉토리(root_path)를 후위 순회로 삭제합니다.
        """
        # 먼저 하위 항목들 처리
        for entry in os.scandir(root_path):
            path = entry.path
            if entry.is_dir(follow_symlinks=False):
                # 서브디렉토리 재귀 삭제
                _delete_tree(path)
            else:
                # 파일 삭제
                os.remove(path)
        # 하위 항목까지 다 비워졌으면 자신(빈 디렉토리)도 삭제
        os.rmdir(root_path)

    options = [D_PK_WORKING, D_PK_ROOT, D_DOWNLOADS]
    d_working = ensure_value_completed(
        key_name='d_working=',
        options=options
    )

    if not os.path.isabs(d_working):
        raise ValueError(f"절대경로를 입력해야 합니다: {d_working!r}")
    if not os.path.isdir(d_working):
        return

    _delete_tree(d_working)
