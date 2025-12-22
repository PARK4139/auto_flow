
import win32con
import toml
import threading
import socket
import shutil
import shlex
import math
import clipboard
from seleniumbase import Driver

from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_objects.pk_files import F_POTPLAYER_EXE
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from os.path import dirname
from cryptography.hazmat.primitives import padding
from bs4 import ResultSet
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style



def install_py_module(module_name):
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
