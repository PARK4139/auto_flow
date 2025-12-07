

import zlib
import zipfile


import urllib
import tqdm
import tomllib
import tomllib
import toml
import timeit
import time
import subprocess, time
import sqlite3
import speech_recognition as sr
import shlex
import re
import random
import pyglet
import pygetwindow
import psutil
import platform
import paramiko
import pandas as pd
import os.path
import numpy as np
import mysql.connector
import keyboard
import json
import importlib
import easyocr
import datetime
import colorama
import colorama
import clipboard
import calendar

from urllib.parse import quote
from telegram import Bot
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from queue import Queue, Empty
from prompt_toolkit import PromptSession
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
import logging
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden, D_PK_WORKING
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from passlib.context import CryptContext
from paramiko import SSHClient, AutoAddPolicy
from os.path import dirname
from os import path
from mutagen.mp3 import MP3
from functools import partial
from datetime import timedelta
from datetime import datetime
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from bs4 import ResultSet
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def get_ip_available_list():
    return get_ip_available_list_v4()
