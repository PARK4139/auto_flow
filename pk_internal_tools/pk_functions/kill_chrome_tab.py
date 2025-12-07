



from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def kill_chrome_tab(url_to_close):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    window_titles = get_window_titles()
    loop_limit = 50
    for window_title_seg in window_titles:
        if "chrome".lower() in window_title_seg.lower():
            logging.debug(rf'''window_title="{window_title_seg}"  ''')
            loop_cnt = 0
            while 1:
                ensure_window_to_front(window_title_seg)
                if loop_cnt == loop_limit:
                    break
                loop_cnt = loop_cnt + 1
                ensure_slept(milliseconds=15)
                ensure_pressed("ctrl", "l")
                ensure_slept(milliseconds=15)
                url_dragged = get_text_dragged()
                if url_dragged == url_to_close:
                    logging.debug(rf'''url_to_close="{url_to_close}"  ''')
                    logging.debug(rf'''url_dragged="{url_dragged}"  ''')
                    ensure_pressed("ctrl", "w")
                    # restore_all_windows()
                    return
