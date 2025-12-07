from pk_internal_tools.pk_functions.get_text_green import get_text_green
from pk_internal_tools.pk_functions.get_text_red import get_text_red
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_files import F_PK_LOG


def ensure_test_log_updated(func):
    import logging

    from pk_internal_tools.pk_functions import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_str_writen_to_f import ensure_str_writen_to_f

    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            test_result_msg = get_text_green(f"{PkTexts.SUCCEEDED}")
        else:
            test_result_msg = get_text_red(f"{PkTexts.FAILED}")

        test_logging_file = F_PK_LOG
        ensure_pnx_made(test_logging_file, mode='f')
        ensure_str_writen_to_f(f"Test function executed: {test_result_msg:7} {func.__name__}()\n", f=test_logging_file)
        logging.debug(f"Test function executed: {test_result_msg:7} {func.__name__}()", )
        return result

    return wrapper
