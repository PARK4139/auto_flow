


import subprocess
import keyboard
import hashlib
from yt_dlp import YoutubeDL
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from prompt_toolkit import PromptSession


import logging
from moviepy import VideoFileClip
from functools import lru_cache
from dataclasses import dataclass
from Cryptodome.Cipher import AES
from colorama import init as pk_colorama_init
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

from pk_internal_tools.pk_functions.get_d_working import get_d_working


def collect_row_data_from_csv(line_order, issues_list_csv):
    df = get_df_from_issues_list_csv(issues_list_csv)
    columns_required = df.columns.tolist()

    data_required = {}
    line_order = int(line_order)
    nth_row = get_nth_row(df, n=line_order)

    if nth_row is not None:
        for col in columns_required:
            if col in df.columns:
                data_required[col] = nth_row[col]

    return data_required
