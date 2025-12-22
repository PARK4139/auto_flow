import zlib

import win32con
import urllib.parse
import tomllib
import time
import threading
import tarfile
import speech_recognition as sr
import shlex
import requests
import random

import pyglet
import pygetwindow
import pyaudio
import psutil
import pickle
import pandas as pd
import mysql.connector
import inspect
import easyocr
import cv2
import clipboard
import calendar
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from urllib.parse import urlparse
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pytube import Playlist
from pynput import mouse
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list


from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE, F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from PIL import Image
from os import path
from mutagen.mp3 import MP3
from functools import partial as functools_partial
from functools import partial
from fastapi import HTTPException
from datetime import datetime, time
from cryptography.hazmat.primitives import padding
from bs4 import ResultSet

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.is_d import is_d


from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def is_year(yyyy):
    from datetime import datetime
    return datetime.today().year == int(yyyy)
