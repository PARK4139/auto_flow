import threading
import requests
import keyboard
import ipdb
from tkinter import UNDERLINE
from pytube import Playlist
from pynput import mouse
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list

import logging

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE

from PIL import Image
from bs4 import ResultSet
from base64 import b64decode
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def do_random_schedules():
    import inspect
    import random
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    int_random = random.randint(0, 7)
    # pk_Tts.speak(f'랜덤숫자 {int_random} 나왔습니다')
    # mkmk
    if int_random == 0:
        pass
    elif int_random == 1:
        pass
    elif int_random == 2:
        pass
    elif int_random == 3:
        pass
    elif int_random == 4:
        pass
    elif int_random == 5:
        pass
    elif int_random == 6:
        pass
    elif int_random == 7:
        pass
