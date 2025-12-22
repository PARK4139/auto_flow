import yt_dlp
import winreg
import webbrowser
import toml
import string
import speech_recognition as sr

import mysql.connector
import math
import ipdb
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote, urlparse
from telegram import Bot
from selenium.webdriver.support.ui import WebDriverWait
from prompt_toolkit.styles import Style
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_filtered_media_files import get_files_filtered_from_db
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from PIL import Image
from os import path
from moviepy import VideoFileClip
from datetime import datetime, time
from Cryptodome.Random import get_random_bytes
from colorama import init as pk_colorama_init
from bs4 import ResultSet
from base64 import b64encode
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS



def get_list_leaved_element_contain_prompt(working_list, prompt):
    return [f for f in working_list if prompt in f]
