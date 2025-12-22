import secrets
import numpy as np
import easyocr
from zipfile import BadZipFile
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from cryptography.hazmat.backends import default_backend
from pk_internal_tools.pk_functions.get_nx import get_nx


def download_jetson_setup():
    todo('%%%FOO%%%')
