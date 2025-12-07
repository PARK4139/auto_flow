import yt_dlp



import webbrowser
import uuid
import undetected_chromedriver as uc
import tqdm
import tomllib
import toml
import threading
import sys
import subprocess
import string
import sqlite3
import speech_recognition as sr
import socket, time
import secrets
import re


import pyaudio
import pickle
import paramiko
import os, inspect
import numpy as np
import nest_asyncio
import mysql.connector
import mutagen
import ipdb
import hashlib
import colorama
import clipboard

import asyncio
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from urllib.parse import quote
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from PySide6.QtWidgets import QApplication
from pynput import mouse
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical


from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
import logging

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state

from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from passlib.context import CryptContext
from os.path import dirname
from os import path
from mysql.connector import connect, Error
from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from functools import partial as functools_partial
from functools import partial
from functools import lru_cache
from fastapi import HTTPException
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from cryptography.hazmat.backends import default_backend
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from collections import Counter
from base64 import b64decode

from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, d_pk_root_hidden, d_pk_external_tools
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
from pk_internal_tools.pk_functions.is_d import is_d

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def get_target_nvidia_serial_via_scp (target_device_data):
    remote_device_target_config = {}
    remote_device_target_config['ip'] = target_device_data.target_device_ip
    remote_device_target_config['port'] = target_device_data.target_device_port
    remote_device_target_config['user_n'] = target_device_data.target_device_user_n
    remote_device_target_config['local_ssh_private_key'] = target_device_data.target_device_local_ssh_private_key
    ensure_command_to_remote_os(cmd='todo', **remote_device_target_config)
    nvidia_serial = target_device_data.target_device_nvidia_serial
    return nvidia_serial
