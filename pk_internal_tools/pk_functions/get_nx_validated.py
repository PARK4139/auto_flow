import yt_dlp
import winreg

import tomllib
import toml
import sys
import sqlite3
import socket
import shlex
import random

import pyglet
import pyaudio
import paramiko
import pandas as pd
import os.path
import numpy as np
import mysql.connector
import math
import hashlib
import functools
import clipboard
from urllib.parse import quote
from tkinter import UNDERLINE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_etc import PkFilter
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from os.path import dirname
from functools import partial as functools_partial
from functools import partial
from datetime import timedelta
from datetime import datetime
from datetime import date
from cryptography.hazmat.primitives import padding
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from bs4 import ResultSet
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_nx_validated(nx):
    nx = nx.strip()
    if any(char in nx for char in r'\/:*?"<>|'):
        logging.debug("Char not allowed in f_n/d_n. Retry.")
        raise
    return nx
