import urllib
import undetected_chromedriver as uc
import tomllib
import toml
import mutagen
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from pytube import Playlist
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f

import logging


def ensure_prepare_data_dir(container: str):
    import os

    data_dir = os.path.join(os.path.expanduser("~"), "Downloads", f"{container}_data")
    os.makedirs(data_dir, exist_ok=True)
    logging.debug(f"Data directory ready: {data_dir}")
    return data_dir
