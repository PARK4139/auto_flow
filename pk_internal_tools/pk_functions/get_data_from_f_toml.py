import win32com.client
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from bs4 import ResultSet
import logging


def get_data_from_f_toml(f):
    import tomllib
    with open(f, "rb") as f_obj:
        data = tomllib.load(f_obj)
    return data
