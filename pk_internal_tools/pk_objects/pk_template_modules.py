
# from base64 import b64decode
# from base64 import b64encode
# from bs4 import BeautifulSoup
# from bs4 import ResultSet
# from collections import Counter
# from collections import defaultdict
# from collections import defaultdict, Counter
# from colorama import Fore
# from colorama import init as pk_colorama_init
# from concurrent.futures import ThreadPoolExecutor
# from Cryptodome.Cipher import AES
# from Cryptodome.Random import get_random_bytes
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from dataclasses import dataclass
# from datetime import date
# from datetime import datetime
# from datetime import datetime, time
# from datetime import datetime, timedelta
# from datetime import timedelta
# from dirsync import sync
# from enum import Enum
# from fastapi import HTTPException
# from functools import lru_cache
# from functools import partial
# from functools import partial as functools_partial
# from functools import wraps
# from glob import glob
# from gtts import gTTS
# from moviepy import VideoFileClip
# from mutagen.mp3 import MP3
# from mysql.connector import connect, Error
# from os import environ
# from os import path
# from os.path import dirname
# from paramiko import SSHClient, AutoAddPolicy
# from passlib.context import CryptContext
# from pathlib import Path
# from PIL import Image
# from PIL import Image, ImageFilter
# from PIL import Image, ImageFont, ImageDraw
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import logging
# from pkg_ps1.system_object.process import ensure_process_killed_by_window_title
# from pk_internal_tools.pk_functions import ensure_pycharm_module_optimize
# from pk_internal_tools.pk_functions import ensure_refactoring_macro_executed
# 
# from pk_internal_tools.pk_functions.backup_workspace import backup_workspace
# from pk_internal_tools.pk_functions.check_min_non_null_or_warn import check_min_non_null_or_warn
# from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
# from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person import ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person
# from pk_internal_tools.pk_functions.does_pnx_exist import does_pnx_exist
# from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
# from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
# from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
# from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
# from pk_internal_tools.pk_functions.ensure_elapsed_time_logged import ensure_elapsed_time_logged
# from pk_internal_tools.pk_functions.ensure_func_info_loaded import ensure_func_info_loaded
# from pk_internal_tools.pk_functions.ensure_func_info_saved import ensure_func_info_saved
# from pk_internal_tools.pk_functions.ensure_pk_exit_silent import ensure_pk_exit_silent
# from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed_v5 import ensure_pk_wrapper_starter_executed_v5
# from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
# from pk_internal_tools.pk_functions.ensure_start_time_logged import ensure_start_time_logged
# from pk_internal_tools.pk_functions.ensure_tmux_pk_session_removed import ensure_tmux_pk_session_removed
# from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
# from pk_internal_tools.pk_functions.ensure_window_to_front_core import ensure_window_to_front_core
# from pk_internal_tools.pk_functions.ensure_window_to_front_v2 import ensure_window_to_front_v2
# from pk_internal_tools.pk_functions.ensure_windows_closed import ensure_windows_closed
# from pk_internal_tools.pk_functions.get_cmd_to_autorun import get_cmd_to_autorun
# from pk_internal_tools.pk_functions.get_d_working import get_d_working
# from pk_internal_tools.pk_functions.get_f_historical import get_f_historical
# from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
# from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
# from pk_internal_tools.pk_functions.get_file_id import get_file_id
# from pk_internal_tools.pk_functions.get_front_window_title import get_front_window_title
# from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
# from pk_internal_tools.pk_functions.get_idx_list import get_idx_list
# from pk_internal_tools.pk_functions.get_list_by_file_id import get_list_by_file_id
# from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
# from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
# from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
# from pk_internal_tools.pk_functions.get_list_removed_element_empty import get_list_removed_empty
# from pk_internal_tools.pk_functions.get_list_removed_none import get_list_removed_none
# from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
# from pk_internal_tools.pk_functions.get_list_striped import get_list_striped
# from pk_internal_tools.pk_functions.get_list_striped_element import get_list_striped_element
# from pk_internal_tools.pk_functions.get_list_without_none import get_list_without_none
# from pk_internal_tools.pk_functions.get_nx import get_nx
# from pk_internal_tools.pk_functions.get_os_n import get_os_n
# from pk_internal_tools.pk_functions.get_p import get_p
# from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
# from pk_internal_tools.pk_functions.get_pk_process_pnxs import get_pk_process_pnxs
# from pk_internal_tools.pk_functions.get_pk_wsl_mount_d import get_pk_wsl_mount_d
# from pk_internal_tools.pk_functions.get_pk_wsl_mount_d_v1 import get_pk_wsl_mount_d_v1
# from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
# from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
# from pathlib import Path
# from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
# from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
# from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
# from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers
# from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
# from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
# from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159v1 import get_pk_time_2025_10_20_1159v1
# from pk_internal_tools.pk_functions.get_txt_highlighted import get_txt_highlighted
# from pk_internal_tools.pk_functions.get_unique_filename import get_unique_filename
# from pk_internal_tools.pk_functions.get_value_by_file_id import get_value_by_file_id
# from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
# from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000_v3 import ensure_value_completed_2025_10_12_0000_v3
# from pk_internal_tools.pk_functions.get_values_from_historical_database_routine import get_values_from_historical_database_routine
# from pk_internal_tools.pk_functions.get_values_from_historical_database_routine_v2 import get_values_from_historical_database_routine_v2
# from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_historical_file
# from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
# from pk_internal_tools.pk_functions.get_filtered_media_files import get_filtered_media_files
# from pk_internal_tools.pk_functions.get_filtered_media_files_v4 import get_filtered_media_files_v4
# from pk_internal_tools.pk_functions.get_webdriver_options_customed import get_webdriver_options_customed
# from pk_internal_tools.pk_functions.get_weekday_as_korean import get_weekday_as_korean
# from pk_external_tools.pk_gui import get_windows_opened_with_hwnd
# from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd_via_win32gui import get_windows_opened_with_hwnd_via_win32gui
# from pk_internal_tools.pk_functions.get_x import get_x
# from pk_internal_tools.pk_functions.guide_pk_error_mssage import guide_pk_error_mssage
# from pk_internal_tools.pk_functions.guide_to_use_pk_process import guide_to_use_pk_process
# from pk_internal_tools.pk_functions.is_d import is_d
# from pk_internal_tools.pk_functions.is_f import is_f
# from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21
# 
# from pk_internal_tools.pk_functions.is_media_file_controller_running_v1 import is_media_file_controller_running_v1
# from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
# from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
# from pk_internal_tools.pk_functions.is_path_like import is_path_like
# from pk_internal_tools.pk_functions.is_url import is_url
# from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
# from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
# from pk_internal_tools.pk_functions.is_window_title_opened import is_window_title_opened
# from pk_internal_tools.pk_functions.kill_losslesscut import kill_losslesscut
# from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
# 
# from pk_internal_tools.pk_functions.load_logged_set import load_logged_set
# from pk_internal_tools.pk_functions.move_window_to_front_via_pid import move_window_to_front_via_pid
# from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
# from pk_internal_tools.pk_functions.ensure_all_import_script_printed import ensure_modules_printed
# from pk_internal_tools.pk_functions.ensure_pk_functionsed import ensure_pk_functionsed
# from pk_internal_tools.pk_functions.ensure_pk_functionsed_v2 import ensure_pk_functionsed_v2
# from pk_internal_tools.pk_functions.ensure_loop_delayed_at_loop_foot import ensure_loop_delayed_at_loop_foot
# from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized

# from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
# from pk_internal_tools.pk_functions.ensure_pressed_v2 import ensure_pressed_v2
# import logging
# from pk_internal_tools.pk_functions.print_once import print_once
# from pk_internal_tools.pk_functions.ensure_state_printed import ensure_state_printed
# from pk_internal_tools.pk_functions.replace_file_nxs_from_old_text_to_new_text import replace_file_nxs_from_old_text_to_new_text
# from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
# from pk_internal_tools.pk_functions.sleep_v2 import sleep_v2
# 
# from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
# from pk_internal_tools.pk_functions.ensure_spoken_v2 import ensure_spoken_v2
# from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
# from pk_internal_tools.pk_functions.ensure_typed_v2 import ensure_typed_v2
# from pk_internal_tools.pk_functions.print_and_save_log_to_file import print_and_save_log_to_file
# from pk_internal_tools.pk_functions.print_green import print_green
# from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
# from pk_internal_tools.pk_functions.print_light_black import print_light_black
# from pk_internal_tools.pk_functions.print_light_blue import print_light_blue
# from pk_internal_tools.pk_functions.print_light_white import print_light_white
# from pk_internal_tools.pk_functions.print_magenta import print_magenta
# from pk_internal_tools.pk_functions.print_pk_ls import print_pk_ls
# from pk_internal_tools.pk_functions.print_pk_ls_v4 import print_pk_ls_v4
# from pk_internal_tools.pk_functions.print_pk_ver import print_pk_ver
# from pk_internal_tools.pk_functions.print_text_via_colorama import print_text_via_colorama
# from pk_internal_tools.pk_functions.print_red import print_red
# from pk_internal_tools.pk_functions.print_yellow import print_yellow
# 
# from pk_internal_tools.pk_functions.restore_workspace_from_latest_archive import restore_workspace_from_latest_archive
# from pk_internal_tools.pk_functions.ensure_losslesscut_ran import ensure_losslesscut_ran
# from pk_internal_tools.pk_functions.run_pk_process_by_path import run_pk_process_by_path
# from pk_internal_tools.pk_functions.get_sanitized_file_path import get_sanitized_file_path
# from pk_internal_tools.pk_functions.save_logged_set import save_logged_set
# from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
# from pk_internal_tools.pk_functions.set_values_to_historical_file import set_values_to_historical_file
# from pk_internal_tools.pk_functions.split_by_top_level_def import split_by_top_level_def
# from pk_internal_tools.pk_functions.switch_to_keyboard_mode_to_english_at_windows import switch_to_keyboard_mode_to_english_at_windows
# from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
# from pk_internal_tools.pk_functions.ensure_str_writen_to_f import ensure_str_writen_to_f
# from pk_external_tools.pk_colorful_cli_util import print, print_magenta, print_light_white, ColoramaUtil, print_ment_via_colorama, print_success, prijnt_as_log, print_yellow
# from pk_external_tools.pk_core_constants import USERPROFILE, HOSTNAME, UNDERLINE, BLANK, BIGGEST_PNXS, SMALLEST_PNXS, PLAYING_SOUNDS, COUNTS_FOR_GUIDE_TO_SLEEP,VIDEO_IDS_ALLOWED, AUDIO_IDS_ALLOWED, STORAGE_VIDEOES_MERGED, PROJECT_PARENTS_D, DESKTOP, DOWNLOADS, pk_external_tools, PKG_DPL, PKG_CACHE_PRIVATE
# from pk_external_tools.pk_gui import PkGui, get_display_info, ensure_printed_as_gui, should_i_do
# 
# 
# from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
# 
# 
# from pk_internal_tools.pk_objects.performance_logic import ensure_seconds_measured, pk_measure_memory
# from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
# from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

# from pk_internal_tools.pk_objects.pk_alias_keyboard_map import pk_alias_keyboard_map
# from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
# from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
# from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
# from pk_internal_tools.pk_objects.pk_directories import D_DESKTOP
# from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS
# from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, d_pk_root_hidden
# from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, d_pk_root_hidden, d_pk_external_tools
# from pk_internal_tools.pk_objects.pk_directories import D_PKG_ARCHIVED
# from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
# from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
# from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools, D_PKG_ARCHIVED
# from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
# from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden, D_PK_WORKING
# from pk_internal_tools.pk_objects.pk_directories import D_PK_FUNCTIONS
# from pk_internal_tools.pk_objects.pk_directories import D_PK_FUNCTIONS, D_PKG_ARCHIVED
# from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
# from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS
# from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, d_pk_root_hidden
# from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, d_pk_root_hidden, d_pk_external_tools
# from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_DOWNLOADS, d_pk_external_tools
# from pk_internal_tools.pk_objects.pk_directories  import d_pk_system
# from pk_internal_tools.pk_objects.pk_encodings import Encoding
# from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
# from pk_internal_tools.pk_objects.pk_etc import PkFilter
# # # from pk_internal_tools.pk_objects.pk_etc import PkFilter, PK_UNDERLINE
# from pk_internal_tools.pk_objects.pk_files import F_FFMPEG
# from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
# from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT
# from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_MINI_64
# from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_MINI_64, F_HISTORICAL_PNX
# from pk_internal_tools.pk_objects.pk_files import F_TEMP_TXT

# from pk_external_tools.refactor.ensure_refactoring_macro_executed import PkMacros
# from pk_external_tools.refactor.pk_ensure_pk_functionsed import restore_workspace_from_latest_archive, split_by_top_level_def, backup_workspace
# from pk_external_tools.refactor.ensure_refactoring_macro_executed import PkMacros
# from pk_external_tools.refactor.pk_ensure_modules_enabled_front import clean_import_block
# from pk_external_tools.workspace import ensure_pycharm_module_optimize
# from prompt_toolkit import prompt
# from prompt_toolkit import PromptSession
# from prompt_toolkit.completion import WordCompleter
# from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
# from prompt_toolkit.shortcuts import CompleteStyle
# from prompt_toolkit.styles import Style
# from pympler import asizeof
# from pynput import mouse
# from PySide6.QtWidgets import QApplication
# from pytube import Playlist
# from queue import Queue, Empty
# from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from seleniumbase import Driver
# from telegram import Bot
# from telegram import Bot, Update
# from telegram.ext import Application, MessageHandler, filters, CallbackContext
# from telethon import TelegramClient, events
# from tkinter import UNDERLINE
# from typing import List
# from typing import TypeVar
# from typing import TypeVar, List
# from urllib.parse import quote
# from urllib.parse import quote, urlparse
# from urllib.parse import unquote, urlparse, parse_qs
# from urllib.parse import urlparse
# from urllib.parse import urlparse, parse_qs, unquote
# from webdriver_manager.chrome import ChromeDriverManager
# from yt_dlp import YoutubeDL
# from zipfile import BadZipFile
# import ast
# import asyncio
# import browser_cookie3
# import calendar
# import chardet
# import clipboard
# import colorama
# import ctypes
# import cv2
# import datetime
# import easyocr
# import functools
# import glob
# import hashlib
# import importlib
# import inspect
# import ipdb
# import json
# import keyboard
# import logging
import logging
# import math
# import mutagen
# import mysql.connector
# import nest_asyncio
# import numpy as np
# import os
# import os, inspect
# import os.path
# import pandas as pd
# import paramiko
# import pickle
# import core_constants
# # import pk_external_tools.pk_objects.static_logic as system_object.static_logic
# import platform
# import psutil
# import pyaudio
# import pyautogui
# import pygetwindow
# import pyglet
# import pythoncom
# import pywintypes
# import random
# import random, math
# import re
# import requests
# import secrets
# import selenium.webdriver as webdriver
# import shlex
# import shutil
# import socket
# import speech_recognition as sr
# import sqlite3
# import statistics
# import string
# import subprocess
# import sys
# import tarfile
# import tempfile
# import threading
# import time
# import timeit
# import toml
# import toml  # toml:    쓰기 기능 추천
# import tomllib  # tomllib: 파싱/읽기 전용, binary 모드로 읽어야 하는 이유?
# import tqdm
# import traceback
# import undetected_chromedriver as uc
# import urllib
# import urllib.parse
# import uuid
# import webbrowser
# import win32api
# import win32com.client
# import win32con
# import win32con # pywin32

 # pywin32

# import winreg
# import yt_dlp
# import zipfile
# import zlib
# from pk_internal_tools.pk_functions.click_mouse_left_btn import click_mouse_left_btn
# from pk_internal_tools.pk_functions.does_text_bounding_box_exist_via_easy_ocr import does_text_bounding_box_exist_via_easy_ocr
# from pk_internal_tools.pk_functions.ensure_slept import ensure_slept