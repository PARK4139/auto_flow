import urllib
import tomllib
import mutagen

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from dataclasses import dataclass
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.is_f import is_f
import logging

import logging


def classify_pnx_list_to_pn_dir(d_working):
    import os

    for pnx_nx in os.listdir(d_working):
        pnx_item = os.path.join(d_working, pnx_nx)
        if is_f(pnx_item):
            logging.debug(f'''pnx_item={pnx_item}''')
            f_n_d = os.path.join(d_working, pnx_nx)
            f_n_d_pn = get_pn(f_n_d)

            if not os.path.exists(f_n_d_pn):
                os.makedirs(f_n_d_pn)

            # shutil.move(pnx_item, f_n_d_pn) # 중복있으면 에러로 처리됨
            ensure_pnx_moved(pnx=pnx_item, d_dst=f_n_d_pn)  # 중복있으면 timestamp를 붙여 이동됨
