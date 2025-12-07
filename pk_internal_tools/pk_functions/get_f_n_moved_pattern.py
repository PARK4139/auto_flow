

import yt_dlp
import time
import threading
import speech_recognition as sr
import random
import platform
import nest_asyncio
import importlib
import easyocr
import chardet
from seleniumbase import Driver
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern


from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load

from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
import logging
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f


from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


from pathlib import Path
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from functools import lru_cache
from datetime import datetime
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging


def get_f_n_moved_pattern(pattern, pnx_working, mode_front):
    import re
    match = re.search(pattern=pattern, string=pnx_working)
    n = get_n(pnx_working)
    p = get_p(pnx_working)
    x = get_x(pnx_working)
    if match:
        pattern = match.group(1)
        if mode_front:
            pnx_working_new = rf"{p}\{pattern}_{n.replace(pattern, '')}{x}"
        else:
            pnx_working_new = rf"{p}\{n.replace(pattern, '')}_{pattern}{x}"
        return pnx_working_new
    else:
        # 패턴이 없으면 원래 f명 반환
        return pnx_working
