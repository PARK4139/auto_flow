import undetected_chromedriver as uc
import tqdm
import toml
import threading
import pyaudio
import mutagen
from selenium.webdriver.chrome.options import Options
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.get_list_sorted import get_list_sorted
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from datetime import timedelta
from bs4 import BeautifulSoup
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def get_random_id(length_limit: int):
    import random
    import string

    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length_limit))
