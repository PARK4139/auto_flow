import logging
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken


def speak_count_down(countdown_limit_upper):  #
    for i in range(0, countdown_limit_upper, -1):
        message = f'count down {i}'
        logging.debug(message)
        ensure_spoken(message)
