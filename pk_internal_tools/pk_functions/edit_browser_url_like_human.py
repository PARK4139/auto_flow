import traceback
import tqdm
import sys
import shlex
import pythoncom
import math
import inspect

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed

from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pathlib import Path
from datetime import datetime
from datetime import date
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from Cryptodome.Random import get_random_bytes
from bs4 import BeautifulSoup
from base64 import b64encode
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


def edit_browser_url_like_human():
    import random
    ensure_pressed("ctrl", "l"
    5)
    ensure_pressed("right"
    5)
    write("/")
    ensure_slept(milliseconds=random.randint(a=12, b=23))
