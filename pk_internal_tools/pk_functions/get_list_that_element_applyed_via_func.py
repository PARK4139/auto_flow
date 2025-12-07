import winreg
import win32con
import webbrowser
import timeit
import time
import shutil
import requests
import random
import pythoncom
import ipdb
import hashlib
import functools
from selenium.webdriver.common.keys import Keys
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from functools import partial as functools_partial
from concurrent.futures import ThreadPoolExecutor
from base64 import b64decode

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def get_list_that_element_applyed_via_func(func, working_list):
    return [func(item) for item in working_list]
