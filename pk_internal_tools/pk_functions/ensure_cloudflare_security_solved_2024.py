def ensure_cloudflare_security_solved_2024(driver):  # fail
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.click_img_via_autogui import click_img_via_autogui
    from pk_internal_tools.pk_functions.does_normal_tab_exist import does_normal_tab_exist
    from pk_internal_tools.pk_functions.edit_browser_url_like_human import edit_browser_url_like_human
    from pk_internal_tools.pk_functions.get_str_url_decoded import get_str_url_decoded
    from pk_internal_tools.pk_functions.kill_tabs_except_current_tab_via_selenium import kill_tabs_except_current_tab_via_selenium
    from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    import logging
    import random

    url = f'https://torrentqq348.com'
    url_decoded = get_str_url_decoded(url)
    logging.debug(rf'''url={url:60s}  url_decoded={url_decoded}  ''')
    driver.get(url_decoded)
    # driver.get(url)
    ensure_slept(milliseconds=random.randint(a=222, b=1333))
    try_cnt_limit = 22
    try_cnt = 0
    tab_title_negative = "잠시만 기다리십시오"
    f_png = rf'{d_pk_external_tools}\collect_img_for_autogui_2024_11_03_19_41_12.png'
    while 1:
        if does_normal_tab_exist(selenium_driver=driver, tab_title_negative=tab_title_negative):
            # move to tab
            window_required = driver.current_window_handle  # 현재 창 핸들 저장
            driver.switch_to.window(window_required)
            break
        try_cnt += 1
        if try_cnt == try_cnt_limit:
            kill_tabs_except_current_tab_via_selenium(driver)
            driver.get(url)
            ensure_slept(milliseconds=random.randint(a=1222, b=2333))
            try_cnt = 0

        # click checkbox
        ensure_window_to_front(tab_title_negative)  # 창을 맨앞으로 가져오기
        ensure_slept(milliseconds=200)
        click_img_via_autogui(f_png, x_cal=random.randint(a=3, b=150))

        # edit url like person
        edit_browser_url_like_human()

        # copy tab
        # copy_tab_like_pserson()
        # open_tab_via_selenium(driver, url)
