

import win32con
import tarfile
import sqlite3
import socket, time
import re
import random, math
import pywintypes
import pyautogui
import pyaudio
import psutil
import pandas as pd
import os
import numpy as np
import nest_asyncio
import mysql.connector
import mutagen
import functools
import clipboard
import calendar
import asyncio

from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_texts import PkTexts



from PIL import Image
from functools import partial
from fastapi import HTTPException
from dirsync import sync
from datetime import datetime
from cryptography.hazmat.primitives import padding
from concurrent.futures import ThreadPoolExecutor
from base64 import b64encode
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux


import logging


def is_prompt_on_screen(prompt):
    # OCR을 통해 텍스트 추출
    screenshot = get_screenshot()
    extreact_texts = get_extreact_texts_from_image_via_easyocr(screenshot)
    text_extracted = " ".join([r[1] for r in extreact_texts])

    if is_prompt_in_text(prompt=prompt, text=text_extracted):
        return 1
    else:
        return 0
