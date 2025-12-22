import winreg
import webbrowser
import pyglet
import pygetwindow
import psutil
import json
from selenium.common.exceptions import WebDriverException
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from colorama import init as pk_colorama_init
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows



def is_only_no(text):
    import re
    pattern = "^[0-9]+$"
    if re.search(pattern, text):
        return 1
    else:
        return 0
