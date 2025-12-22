from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_remote_pc_controllable_via_chrome_remote_desktop():
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    import logging
    import logging

    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person import ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person

    from pk_internal_tools.pk_functions.decode_via_pk_system import decode_via_pk_system
    from pk_internal_tools.pk_functions.ensure_pk_enabled import PkTexts
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_text_clicked_via_ocr import ensure_text_clicked_via_ocr

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_token_encoded import get_token_encoded
    from pk_internal_tools.pk_functions.ensure_chrome_tab_moved_to_url import ensure_chrome_tab_moved_to_url
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_urls import URL_CHROME_REMOTE

    # chrome remote 열기
    url = URL_CHROME_REMOTE
    ensure_command_executed(cmd=f'explorer "{url}"')
    logging.debug(rf'''url="{url}"  ''')
    window_title_seg = "원격 액세스 - Chrome 원격 데스크톱 - Chrome"
    ensure_window_to_front(window_title_seg)
    ensure_chrome_tab_moved_to_url(url_to_move=url, window_title_seg=window_title_seg)

    if QC_MODE:
        return
    else:
        # remote pc nickname 클릭
        anyang_house_notebook_remote_desktop_nickname = get_token_encoded(token_id="anyang_house_notebook_remote_desktop_nickname")
        logging.debug(f'''anyang_house_notebook_remote_desktop_nickname={anyang_house_notebook_remote_desktop_nickname} ''')

        # 토큰이 None이 아닌 경우에만 실행
        if anyang_house_notebook_remote_desktop_nickname:
            ensure_text_clicked_via_ocr(text=anyang_house_notebook_remote_desktop_nickname)
        else:
            logging.debug(f'''[{PkTexts.WARNING}] 토큰을 가져올 수 없습니다. ''')
            return

        # remote pc pin 입력
        token_chrome_remote_pin = decode_via_pk_system(get_token_encoded(token_id="anyang_house_notebook_remote_desktop_pin"))
        ensure_slept(milliseconds=200)
        ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(token_chrome_remote_pin)
        ensure_pressed("enter")
