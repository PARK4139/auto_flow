import logging
import time

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.get_gemini_cli_expected_titles import get_gemini_cli_expected_titles
from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened
from pk_internal_tools.pk_objects.pk_directories import d_pk_internal_tools


@ensure_seconds_measured
def get_gemini_cli_window_title_by_auto(local_gemini_root=None,gemini_cli_titles=None):
    if gemini_cli_titles is None:
        gemini_cli_titles = get_gemini_cli_expected_titles(local_gemini_root)

    logging.debug("Automatic detection attempted.")

    start_time = time.time()
    timeout = 5  # 5초 타임아웃

    while time.time() - start_time < timeout:
        windows_opened = get_windows_opened()
        gemini_cli_window_title = None

        for option in gemini_cli_titles:
            for window_opened in windows_opened:
                if option in window_opened:
                    gemini_cli_window_title = option
                    break
            if gemini_cli_window_title:
                break
        
        if gemini_cli_window_title:
            logging.debug(f'Gemini is opened with title: {gemini_cli_window_title}')
            return gemini_cli_window_title

        logging.debug("Gemini CLI window not found. Retrying...")
        ensure_slept(1000)

    logging.error("Gemini CLI window detection timed out.")
    return None