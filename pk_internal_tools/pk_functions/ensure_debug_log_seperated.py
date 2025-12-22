import logging
from functools import wraps

from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_objects.pk_etc import PK_DEBUG_LINE
from pk_internal_tools.pk_functions import ensure_console_cleared
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_log_seperated_by_pk_debug_line(func):
    if not QC_MODE:
        return func

    func_name = get_caller_name()

    @wraps(func)
    def wrapper(*args, **kwargs):
        # ensure_console_cleared() # pk_option
        logging.info(get_text_yellow(PK_DEBUG_LINE))
        # logging.debug(rf"{PK_DEBUG_LINE}{PkColors.YELLOW}")

        result = func(*args, **kwargs)

        logging.info(get_text_yellow(PK_DEBUG_LINE))
        # logging.debug(rf"{PkColors.RESET}{PK_DEBUG_LINE}")
        ensure_paused(text=f'paused for checking debugging info at {func_name}()')
        return result

    return wrapper
