
import string
import sqlite3
import random
import pygetwindow
import pyautogui
import platform
import pickle
import paramiko
import os.path
import inspect
import importlib
import calendar
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from PySide6.QtWidgets import QApplication
from pynput import mouse

from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


from os.path import dirname
from gtts import gTTS
from enum import Enum
from dirsync import sync
from datetime import date
from dataclasses import dataclass
from colorama import init as pk_colorama_init
from bs4 import BeautifulSoup
from base64 import b64encode
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
import logging


def truncate_tree(d_src):
    import inspect
    import os
    import shutil
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if os.path.exists(d_src):
        shutil.rmtree(d_src)
    if not os.path.exists(d_src):
        ensure_pnx_made(d_src, mode="d")
