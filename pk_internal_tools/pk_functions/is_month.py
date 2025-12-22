
import uuid
import urllib.parse
import timeit
import sys
import socket
import random
import pyaudio
import paramiko
import nest_asyncio
import importlib
import hashlib
import functools
import easyocr
import datetime
import cv2
import colorama
from zipfile import BadZipFile
from selenium.common.exceptions import WebDriverException
from pynput import mouse
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front




from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pathlib import Path
from gtts import gTTS
from functools import partial as functools_partial
from functools import lru_cache
from fastapi import HTTPException
from enum import Enum
from datetime import datetime
from datetime import date
from dataclasses import dataclass
from cryptography.hazmat.primitives import padding
from collections import Counter
from bs4 import BeautifulSoup
from base64 import b64decode
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def is_month(mm):
    from datetime import datetime
    return datetime.today().month == int(mm)
