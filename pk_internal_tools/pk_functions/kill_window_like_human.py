from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
import logging
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def kill_window_like_human(window_title_seg):
    logging.debug(f'''window_title_seg="{window_title_seg}"''')
    logging.debug(
        f'''window_title_seg == ensure_window_to_front(window_title_seg)="{window_title_seg == ensure_window_to_front(window_title_seg)}"''')
    while 1:
        if not ensure_window_to_front(window_title_seg):
            ensure_window_to_front(window_title_seg)
        if ensure_window_to_front(window_title_seg):
            ensure_pressed("alt", "f4")
        if not is_window_opened(window_title_seg=window_title_seg):
            logging.debug(f'''" {window_title_seg} 창를 닫았습니다''')
            return
