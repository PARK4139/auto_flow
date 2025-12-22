import pyautogui
from pynput import mouse
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front

from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pathlib import Path
from os.path import dirname
from colorama import init as pk_colorama_init

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style


def get_random_pw(length_limit: int):
    import random
    import string
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length_limit))
