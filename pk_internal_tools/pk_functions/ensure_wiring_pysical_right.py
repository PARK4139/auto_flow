import zlib

import win32com.client
import urllib
import tomllib
import toml
import toml
import subprocess
import sqlite3
import shutil
import shlex
import re

import pyglet
import paramiko
import os.path
import mysql.connector
import math
import json
import ipdb
import inspect
import importlib
import hashlib
import datetime
import colorama
import clipboard
from zipfile import BadZipFile
from urllib.parse import urlparse, parse_qs, unquote
from urllib.parse import urlparse
from urllib.parse import quote
from telegram import Bot
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
import logging
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from paramiko import SSHClient, AutoAddPolicy
from gtts import gTTS
from fastapi import HTTPException
from Cryptodome.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor
from bs4 import ResultSet
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def ensure_wiring_pysical_right (target_device_data):
    target_device_identifier = target_device_data.device_identifier

    # bring_NO_flash_kit_from_warehouse()  # zipper bag
    ensure_usb_cable_connected_right()  # HOST_PC 에서 EVM(origin)로 ACCESS      # without_usb_hub
    ensure_lan_cable_connected_right()  # HOST_PC 에서 EVM(origin) LAN6(하단케이스에 적힌) 포트에

    if 'no' in target_device_identifier:

        pass
    elif 'nx' in target_device_identifier:
        pass
    elif 'xc' in target_device_identifier:
        pass
    elif 'evm' in target_device_identifier:
        pass
    else:
        logging.debug(f'''unknown target_device_identifier ({target_device_data.device_identifier}) ''',
                      print_color='yellow')
        raise
