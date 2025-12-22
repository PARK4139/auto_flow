import zipfile
import urllib
import tqdm
import tomllib
import time
import pygetwindow
import pickle
import pandas as pd
import nest_asyncio
import cv2
from urllib.parse import unquote, urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed



from PIL import Image
from moviepy import VideoFileClip
from Cryptodome.Cipher import AES

from pathlib import Path
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def print_and_get_text_converted(text: str, convert_mode=0):
    import inspect

    """
    # str to str

    param str
    return str
    """
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    def convert_mode_1(text):
        text_converted = text
        while (True):
            if "  " in text:
                text_converted = text.replace("  ", " ")
            else:
                break
        text_converted = text_converted.replace(" ", "\",\"")
        text_converted = f"\"{text_converted}\""
        text_converted = f"[{text_converted}]"
        print_magenta(f'''{inspect.currentframe().f_code.co_name}={text_converted}''')
        return text_converted

    def convert_mode_2(text):
        text_converted = text
        while (True):
            if "  " in text:
                text_converted = text.replace("  ", " ")
            else:
                break
        text_converted = text_converted.replace(" ", "\",\"")
        text_converted = text_converted.replace("\"\"", "\"")
        text_converted = f"\"{text_converted}\""
        text_converted = f"[{text_converted}]"
        print_magenta(f'''{inspect.currentframe().f_code.co_name}={text_converted}''')
        return text_converted

    def convert_mode_3(text):
        text = text.replace("  ", " ")
        text_converted = text.replace(" ", ",")
        print_magenta(f'''{inspect.currentframe().f_code.co_name}={text_converted}''')
        return text_converted

    def convert_mode_4(text):
        texts = text.split(" ")
        texts = get_list_striped_element(working_list=texts)
        text_converted = text
        print_magenta(f'''{inspect.currentframe().f_code.co_name}={text_converted}''')
        return text_converted

    def convert_mode_x(text):
        text_converted = text
        if "  " in text:
            text_converted = text.replace("  ", " ")
        text_converted = text.replace(" ", "\",\"")
        text_converted = f"\"{text_converted}\""
        text_converted = f"[{text_converted}]"
        print_magenta(f'''{inspect.currentframe().f_code.co_name}={text_converted}''')
        return text_converted

    def convert_mode_0(text):
        convert_mode_1(text)
        convert_mode_2(text)
        convert_mode_3(text)
        convert_mode_4(text)
        convert_mode_x(text)

    if convert_mode == 0:
        convert_mode_0(text)
        return None

    elif convert_mode == 1:
        return convert_mode_1(text)
    elif convert_mode == 2:
        return convert_mode_2(text)
    else:
        return None
