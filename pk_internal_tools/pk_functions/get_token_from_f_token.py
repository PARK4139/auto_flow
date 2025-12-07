import toml
import random
import platform
from prompt_toolkit.styles import Style
import logging
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_token_from_f_token(f_token, initial_str):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    ensure_token_file_generated(f=f_token, initial_str=initial_str)
    logging.debug(rf'''f_token_nx="{get_nx(f_token)}"  ''')
    token = get_str_from_file(pnx=f_token)
    token = token.replace("\n", "")
    token = token.strip()
    logging.debug(rf'''token="{token}"  ''')
    if token == "" or token == "\n":
        logging.debug(rf'''token is empty  ''')
        import ipdb
        ipdb.set_trace()
    return token
