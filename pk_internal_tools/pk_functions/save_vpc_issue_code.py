import yt_dlp

import urllib.parse
import urllib
import tomllib
import timeit
import subprocess
import socket, time
import pyautogui
import os
import mutagen
import hashlib
import clipboard
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from telegram import Bot
from selenium.webdriver.common.by import By

import logging

from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from PIL import Image, ImageFilter
from functools import partial as functools_partial
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def save_target_issue_code(issue_code):
    logging.debug(f'''issu_code is saved ''')
