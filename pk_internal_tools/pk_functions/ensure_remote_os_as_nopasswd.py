import zlib
import zipfile
import webbrowser
import urllib.parse
import traceback
import tqdm
import toml
import toml
import re

import pythoncom
import pyglet
import os
import numpy as np
import nest_asyncio
import chardet
import calendar
from urllib.parse import quote
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
from pk_internal_tools.pk_functions.get_f_loading_nx_by_pattern import get_f_loading_nx_by_pattern
from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
import logging


from pk_internal_tools.pk_objects.pk_files import F_POT_PLAYER_EXE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

from os.path import dirname
from mutagen.mp3 import MP3
from dirsync import sync
from datetime import datetime, time
from dataclasses import dataclass
from colorama import init as pk_colorama_init
from collections import Counter
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pathlib import Path
from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
from pk_internal_tools.pk_functions.is_d import is_d
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style
from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs
from pk_internal_tools.pk_functions.get_d_working import get_d_working


def ensure_remote_os_as_nopasswd(**remote_device_target_config):
    import inspect
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000

    import logging

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_command_to_remote_os import ensure_command_to_wireless_target
    from pk_internal_tools.pk_functions.get_wsl_distro_port import get_wsl_distro_port
    from pk_internal_tools.pk_functions.ensure_dockerfile_writen import ensure_dockerfile_writen
    from pk_internal_tools.pk_functions.ensure_remote_os_as_nopasswd import ensure_remote_os_as_nopasswd
    from pk_internal_tools.pk_functions.ensure_ssh_public_key_to_remote_os import ensure_ssh_public_key_to_remote_os
    from pk_internal_tools.pk_functions.ensure_wsl_distro_enabled import ensure_wsl_distro_enabled
    from pk_internal_tools.pk_functions.ensure_wsl_distro_session import ensure_wsl_distro_session
    from pk_internal_tools.pk_functions.get_n import get_n
    from pk_internal_tools.pk_functions.get_wsl_distro_names_installed import get_wsl_distro_names_installed
    from pk_internal_tools.pk_functions.get_wsl_ip import get_wsl_ip
    from pk_internal_tools.pk_functions.get_wsl_pw import get_wsl_pw
    from pk_internal_tools.pk_functions.get_wsl_user_n import get_wsl_user_n
    from pk_internal_tools.pk_objects.pk_directories import D_PK_FASTAPI, d_pk_root, D_USERPROFILE
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    import os

    try:

        local_ssh_public_key = remote_device_target_config['local_ssh_public_key']
        local_ssh_private_key = remote_device_target_config['local_ssh_private_key']
        ip = remote_device_target_config['ip']
        port = remote_device_target_config['port']
        user_n = remote_device_target_config['user_n']
        pw = remote_device_target_config['pw']
        # public_key = remote_device_target_config['public_key']

        cmd = f"sudo grep -n '{user_n} ALL=(ALL:ALL) NOPASSWD:ALL' /etc/sudoers"
        std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
        signature = f"{user_n} ALL=(ALL:ALL) NOPASSWD:ALL"
        for std_out_str in std_outs:
            if signature in std_out_str:
                logging.debug("THE ENTRY IS ALREADY PRESENT")
                return 1
            else:
                cmd = f"echo '{pw}' | sudo -S bash -c \"echo '{user_n} ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers\""
                std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
                if not len(std_err_list) == 0:
                    for std_err_str in std_err_list:
                        logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
                if not len(std_outs) == 0:
                    for std_out_str in std_outs:
                        logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')
                cmd = f"sudo visudo -c"
                std_outs, std_err_list = ensure_command_to_remote_os_with_pubkey(cmd=cmd, **remote_device_target_config)
                if not len(std_err_list) == 0:
                    for std_err_str in std_err_list:
                        logging.debug(rf'{"[ REMOTE ERROR ]"} {std_err_str}')
                if not len(std_outs) == 0:
                    for std_out_str in std_outs:
                        logging.debug(rf'{"[ REMOTE DEBUG ]"} {std_out_str}')
    except:
        import traceback
        logging.debug(rf"{traceback.format_exc()}   ")
