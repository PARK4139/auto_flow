
import webbrowser
import uuid
import sqlite3
import random
import pythoncom
import mysql.connector
import importlib
import colorama
import calendar
from zipfile import BadZipFile
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from passlib.context import CryptContext
from gtts import gTTS
from functools import partial
from datetime import date
from bs4 import BeautifulSoup
from pathlib import Path
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools


def get_windows_opened_with_hwnd_via_pygetwindow():
    import pygetwindow
    windows = pygetwindow.getAllTitles()
    return windows
