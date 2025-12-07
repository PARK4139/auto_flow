import winreg
import webbrowser
import shutil
import psutil
import pandas as pd
import cv2
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern

from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from functools import partial as functools_partial
from fastapi import HTTPException
from dirsync import sync
from cryptography.hazmat.primitives import padding
from bs4 import ResultSet
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

import logging


def make_version_new_v_1_0_1(via_f_txt=False, working_list=None, debug_mode=True):
    import inspect
    import os
    import re
    import shutil

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    from pk_internal_tools.pk_objects.pk_directories import d_pk_config
    f_func_n_txt = d_pk_config / f'{func_n}.txt'
    ensure_pnx_made(pnx=f_func_n_txt, mode='f')
    ensure_pnx_opened_by_ext(pnx=f_func_n_txt)

    def get_next_versioned_nx(f_nx, debug_mode=True):
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        name, ext = os.path.splitext(f_nx)
        files = os.listdir("pkg_friday")

        # 정규표현식으로 "v1.x.y" 형태의 버전을 찾기
        versioned_files = [f for f in files if re.match(fr"{re.escape(name)}_v\d+\.\d+\.\d+{re.escape(ext)}", f)]

        if versioned_files:
            latest_version = max(versioned_files, key=lambda x: list(map(int, re.findall(r"\d+", x)[-3:])))
            major, minor, patch = map(int, re.findall(r"\d+", latest_version)[-3:])
            patch += 1
            next_version = f"{major}.{minor}.{patch}"
        else:
            next_version = "1.0.0"
        next_versioned_pnx = f"{name}_v{next_version}{ext}"
        logging.debug(f'''next_versioned_pnx="{next_versioned_pnx}" ''')
        return next_versioned_pnx

    def cp_and_mv_with_version(src, debug_mode=True):
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        # make new version
        # cp
        if not is_pnx_existing(src):
            logging.debug(f"{src} f을 찾을 수 없습니다.")
            return
        src_nx = get_nx(src)
        f_next_versioned_nx = get_next_versioned_nx(src_nx)
        shutil.copy2(src, f_next_versioned_nx)
        logging.debug(f'''src="{src}"''')
        logging.debug(f'''f_next_versioned_nx="{f_next_versioned_nx}"''')
        logging.debug(f"''{src}'를  {f_next_versioned_nx}'로 copied.")
        f = src
        f_nx = get_nx(f)
        f_n = get_n(f)
        f_x = get_x(f)

        files = os.listdir("pkg_friday")

        dst = rf"{D_DOWNLOADS}\deprecated"
        os.makedirs(dst, exist_ok=True)

        # mv
        # 버전 f만 추출 #최신버전 원본제외
        f_list_versioned_required = files
        f_list_versioned_required = get_list_leaved_element_contain_prompt(working_list=f_list_versioned_required,
                                                                           prompt=f_n)
        f_list_versioned_required.remove(f_nx)  # 원본제외
        f_list_versioned_required.remove(f_next_versioned_nx)  # 최신버전제외
        ensure_iterable_log_as_vertical(item_iterable=f_list_versioned_required, item_iterable_n="f_list_versioned_required")

        logging.debug(f'''f="{f}"''')
        logging.debug(f'''f_n="{f_n}"''')
        logging.debug(f'''f_x="{f_x}"''')
        logging.debug(f'''len(f_list_versioned_required)={len(f_list_versioned_required)}''')
        logging.debug(f'''len(f_list_versioned_required) >= 1="{len(f_list_versioned_required) >= 1}"''')
        if len(f_list_versioned_required) > 1:
            for f in f_list_versioned_required:
                shutil.move(f, dst)
                logging.debug(f"'{f}' moved to '{dst}'")

    if via_f_txt == True and working_list is None:
        working_list = get_list_from_f(f=f_func_n_txt)
        working_list = get_list_removed_element_contain_prompt(working_list=working_list, prompt="#")
        working_list = get_list_replaced_element_from_str_to_str(working_list=working_list, from_str='\n', to_str='')
        for item_str in working_list:
            item_str = get_str_replaced_from_str_to_str_new(item_str=item_str, from_str='PROJECT_D', to_str=d_pk_root)
            # item=get_pnx_windows_style(pnx=item)
            item_str = get_pnx_unix_style(pnx=item_str)
            logging.debug(f'''item_str="{item_str}"''')
            cp_and_mv_with_version(item_str)
    if via_f_txt is not True and working_list is not None:
        for f in working_list:
            cp_and_mv_with_version(f)
