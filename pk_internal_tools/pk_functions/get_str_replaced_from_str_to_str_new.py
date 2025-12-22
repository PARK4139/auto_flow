
from tkinter import UNDERLINE
from selenium.webdriver.chrome.options import Options


import logging
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from gtts import gTTS
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

import logging


def get_str_replaced_from_str_to_str_new(item_str, from_str, to_str):
    logging.debug(f'''item_str="{item_str}"''')
    logging.debug(f'''from_str="{from_str}"''')
    logging.debug(f'''to_str="{to_str}"''')
    if not isinstance(item_str, str):
        raise TypeError("item_str must be a string.")
    if not isinstance(from_str, str):
        raise TypeError("from_str must be a string.")
    if not isinstance(to_str, str):
        raise TypeError("to_str must be a string.")
    item_str = item_str.replace(from_str, to_str)
    logging.debug(f'''item_str="{item_str}"''')
    return item_str
