import random
import pygetwindow
import chardet
from pytube import Playlist
from pk_internal_tools.pk_functions.get_d_working import get_d_working
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from passlib.context import CryptContext
from colorama import init as pk_colorama_init

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def report_target_issue_discovered():
    logging.debug(f'''vpc issue is discovered ''')
