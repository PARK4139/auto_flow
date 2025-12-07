import zipfile

import win32com.client
import time
import threading
import subprocess, time
import string
import socket, time
import pyglet
import pyautogui
import pyaudio
import ipdb
import colorama
import clipboard
import chardet
from zipfile import BadZipFile
from urllib.parse import quote
from selenium.webdriver.common.action_chains import ActionChains
from pk_internal_tools.pk_functions.get_f_media_to_load import get_f_media_to_load
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_etc import PkFilter

from pk_internal_tools.pk_objects.pk_files import F_HISTORICAL_PNX
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from paramiko import SSHClient, AutoAddPolicy
from os import path
from mutagen.mp3 import MP3
from gtts import gTTS
from functools import partial as functools_partial
from Cryptodome.Random import get_random_bytes
from bs4 import ResultSet
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def format_selector(ctx):
    """ 최적의 비디오 및 오디오 형식을 선택하는 함수 """
    formats = ctx.get('formats')
    if not formats:
        raise ValueError("No formats available.")

    # 모든 비디오 포맷 가져오기 (MP4 우선)
    video_formats = sorted(
        [fmt for fmt in formats if fmt.get('vcodec') != 'none'],
        key=lambda fmt: (int(fmt.get('height') or 0), int(fmt.get('vbr') or 0)), reverse=True
    )

    # 모든 오디오 포맷 가져오기
    audio_formats = sorted(
        [fmt for fmt in formats if fmt.get('acodec') != 'none'],
        key=lambda fmt: int(fmt.get('abr') or 0), reverse=True
    )

    # MP4 우선, 없으면 다른 확장자도 허용
    for video in video_formats:
        audio_ext = 'm4a' if video.get('ext') == 'mp4' else video.get('ext')
        compatible_audio = next((audio for audio in audio_formats if audio.get('ext') == audio_ext), None)
        if compatible_audio:
            return {
                'format_id': f"{video['format_id']}+{compatible_audio['format_id']}",
                'ext': video['ext'],
                'requested_formats': [video, compatible_audio],
                'protocol': f"{video.get('protocol', '')}+{compatible_audio.get('protocol', '')}"
            }

    # 아무 형식도 찾지 못한 경우
    raise ValueError("No compatible format found. Check if the video is restricted.")
