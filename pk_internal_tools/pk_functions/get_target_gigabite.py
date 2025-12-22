import sys
import socket
import pythoncom
import pygetwindow
import pyaudio
import importlib
from selenium.common.exceptions import WebDriverException
import logging

from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from functools import partial
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx


def get_target_gigabite(target_path):
    return get_target_bite(target_path.strip()) / 1024 ** 3
