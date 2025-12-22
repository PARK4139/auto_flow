import winreg

import urllib
import traceback
import tqdm
import toml
import subprocess
import shlex
import requests
import random, math
import random
import pywintypes
import pythoncom
import pygetwindow
import pyautogui
# import pyaudio
# import pandas as pd
import os
import numpy as np
import nest_asyncio
import mysql.connector
import inspect
import importlib
import hashlib
import easyocr
import cv2
from urllib.parse import urlparse
from urllib.parse import quote
from telegram import Bot, Update
from selenium.webdriver.support import expected_conditions as EC
from pynput import mouse
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state


from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING

from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pathlib import Path
from paramiko import SSHClient, AutoAddPolicy
from moviepy import VideoFileClip
from dirsync import sync
from datetime import timedelta
from Cryptodome.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from bs4 import ResultSet
from base64 import b64decode
from pk_internal_tools.pk_functions.get_nx import get_nx

from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated



from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def ensure_remove_and_make_remote_d(d, remote_device_target_config):
    # remove d
    ensure_reensure_pnx_moved_of_remote_os(d=d, **remote_device_target_config)

    # make d
    std_outs, std_err_list = ensure_command_to_remote_os(d=f"mkdir -p {d}", **remote_device_target_config)
    for std_out in std_outs:
        logging.debug(rf'''std_out={std_out}  ''')
        raise
