import urllib
import toml
import requests
import random
import pygetwindow
import nest_asyncio
import colorama

from yt_dlp import YoutubeDL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException

from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

from PIL import Image
from enum import Enum
from Cryptodome.Cipher import AES
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def xcopy_with_overwrite(pnx, pnx_future):
    import inspect
    import subprocess
    import traceback

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    try:
        result = ensure_command_executed_like_human_as_admin(rf'echo a | xcopy "{pnx}" "{pnx_future}" /e /h /k /y')
        if result == subprocess.CalledProcessError:
            if is_f(pnx):
                ensure_command_executed_like_human_as_admin(rf'echo f | xcopy "{pnx}" "{pnx_future}" /e /h /k /y')
            else:
                ensure_command_executed_like_human_as_admin(rf'echo d | xcopy "{pnx}" "{pnx_future}" /e /h /k /y')
    except Exception:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
