import logging
import traceback

# @ensure_seconds_measured
def is_window_opened_via_window_title(window_title: str, verbose=False) -> bool:
    try:
        if window_title is None:
            logging.debug(f"is_window_opened_via_window_title: window_title is None. Returning False.")
            return False

        from pk_internal_tools.pk_functions.log_aligned import log_aligned
        from pk_internal_tools.pk_functions.get_windows_opened import get_windows_opened

        window_title = window_title.strip()

        titles = get_windows_opened()
        for title in titles:
            title = title.strip()
            if verbose:
                operator_literal = " 같다 " if len(window_title) == len(title) else " 다르다 "
                key = f"'{window_title}' 와 '{title}' 길이비교결과"
                value = rf"{len(window_title)}와 {len(title)}는 {operator_literal}"
                gap = 1
                log_aligned(key=key, value=value, gap=gap, seperator='')
            if window_title == title:
                logging.debug(f"Window found: '{title}'")
                return True
        logging.debug(f'''{window_title} is not opened ''')
        return False
    except Exception as e:
        logging.error(f"Error in is_window_opened_via_window_title for window_title '{window_title}': {e}")
        traceback.print_exc()
        return False
