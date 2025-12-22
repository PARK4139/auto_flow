def ensure_chrome_tab_moved_to_url(url_to_move, window_title_seg):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    import logging
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_text_dragged import get_text_dragged
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles

    window_titles = get_window_titles()
    for window_title in window_titles:
        if "Chrome".lower() in window_title.lower():
            ensure_window_to_front(window_title_seg)
            loop_limit = 30
            loop_cnt = 0
            while 1:
                if loop_cnt == loop_limit:
                    return
                loop_cnt = loop_cnt + 1
                ensure_slept(milliseconds=15)
                ensure_pressed("ctrl", "l")
                ensure_slept(milliseconds=15)
                url_dragged = get_text_dragged()
                if url_dragged == url_to_move:
                    logging.debug(f'''url_to_move = "{url_to_move}"''')
                    logging.debug(f'''url_dragged = "{url_dragged}"''')
                    break
                pass
