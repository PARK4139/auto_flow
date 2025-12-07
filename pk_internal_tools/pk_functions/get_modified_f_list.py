import winreg

import tomllib
import sys
import socket
import re
import pywintypes

import pyglet
import os.path
import importlib
from tkinter import UNDERLINE
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from moviepy import VideoFileClip
from gtts import gTTS
from datetime import timedelta
from cryptography.hazmat.primitives import padding
from Cryptodome.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_modified_f_list(previous_state, current_state):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    return DataStructureUtil.get_different_elements(list1=current_state, list2=previous_state)
