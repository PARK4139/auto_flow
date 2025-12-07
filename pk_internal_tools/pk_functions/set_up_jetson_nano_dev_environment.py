import zlib
import tomllib
import tomllib
import toml
import subprocess
import socket
import random, math

import pyaudio
import os.path
import json
import ipdb
import importlib
import functools
import cv2
import colorama
import chardet
from tkinter import UNDERLINE
from telegram import Bot
from selenium.webdriver.common.keys import Keys
from queue import Queue, Empty
from PySide6.QtWidgets import QApplication

from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_etc import PkFilter


from paramiko import SSHClient, AutoAddPolicy
from os import path
from mutagen.mp3 import MP3
from functools import partial
from enum import Enum
from datetime import timedelta
from datetime import date
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from bs4 import ResultSet
from base64 import b64encode
from base64 import b64decode
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools

from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing

import logging


def set_up_jetson_nano_dev_environment():
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # winget # fail # windows 11 부터 시도해보자. 10 지원 끝난듯.
    # winget 윈도우에서 마소 official 패키지 매니저
    # winget --version
    # winget search Google Chrome
    # winget install Google.Chrome --silent
    # winget install Microsoft.VisualStudio --silent

    # choco # fail
    # console_title="choco install"
    # run_powershell_as_admin()
    # ensure_writen_like_human(string=rf"$host.ui.RawUI.WindowTitle='{console_title}'  ", interval=0.005)
    # press("enter")
    # ensure_writen_like_human(string=rf"$Host.UI.RawUI.BufferSize=New-Object Management.Automation.Host.Size(1000, 1000) ", interval=0.005)
    # press("enter")
    # ensure_writen_like_human(string=rf"$Host.UI.RawUI.WindowSize=New-Object Management.Automation.Host.Size(1000, 1000)  ", interval=0.005)
    # press("enter")
    # ensure_writen_like_human(string=rf" Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol=[System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')) ", interval=0.005)
    # press("enter")
    # choco search usbipd-win
    # choco list #설치된 패키지 확인

    # usbipd
    # chdir(pnx=DOWNLOADS)
    # ensure_writen_like_human(string=rf"  choco install usbpid-win --silent ", interval=0.005)
    # press("enter")
    # cmd=rf'curl -O "https://github.com/dorssel/usbipd-win/releases/download/v4.3.0/usbipd-win_4.3.0.msi" ' #fail 왜안되나 손으로 클릭하면 되는데
    # cmd=rf'explorer "https://github.com/dorssel/usbipd-win/releases/tag/v4.3.0" '
    # cmd_run(cmd=cmd)
    # ensure_slept(milliseconds=1200)
    # click_text_coordinates_via_easy_ocr(string="usbipd-win_4.3.0.msi")
    # cmd=rf'explorer "{DOWNLOADS}\usbipd-win_4.3.0.msi" '
    # cmd_run(cmd=cmd)
