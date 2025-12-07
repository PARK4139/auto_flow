
import uuid
import tqdm
import tomllib
import string
import random
import os.path
import ipdb
import inspect
import colorama
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import UNDERLINE
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from os import path
from dirsync import sync
from collections import Counter
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
import logging
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing


def remove_lines_within_keyword_from_f(f: str, keyword: str) -> None:
    import shutil
    from datetime import datetime

    # 변경 전 파일 백업
    # now = datetime.now().strftime("%y%m%d_%H%M")
    now = datetime.now().strftime("%y%m%d_%H")
    backup_path = f"{f}.{now}.bak"
    shutil.copy2(f, backup_path)
    if is_pnx_existing(pnx=backup_path):
        print(f"백업 파일 저장 완료: {backup_path}")

    # 특정 키워드가 포함된 줄 제거
    filtered_lines = []
    with open(f, 'r', encoding='utf-8') as f_obj:
        lines = f_obj.readlines()
        filtered_lines = [line for line in lines if keyword not in line]
    with open(f, 'w', encoding='utf-8') as f_obj:
        f_obj.writelines(filtered_lines)
