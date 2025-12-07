

import urllib
import traceback
import pandas as pd
import math
import cv2
import asyncio
from pytube import Playlist

from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from mutagen.mp3 import MP3
from gtts import gTTS
from datetime import date
from Cryptodome.Random import get_random_bytes
from base64 import b64decode
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000


def get_d_size_fast(path):
    """_d_의 총 크기를 빠르게 계산하는 함수"""
    import os
    total_size = 0
    with os.scandir(path) as it:
        for entry in it:
            try:
                if entry.is_file():
                    total_size += entry.stat().st_size
                elif entry.is_dir():
                    total_size += get_d_size_fast(entry.path)  # 재귀적으로 크기 계산
            except FileNotFoundError:
                pass  # f이 이동 중이거나 삭제된 경우 무시
    return total_size
