import logging

from pk_internal_tools.pk_functions.get_text_dragged import get_text_dragged
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def  is_gemini_auth_chrome_tab_detected():
    import traceback

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    try:
        auth_chrome_tab_title = None
        auth_chrome_tab_title_pattern = "로그인 - Google 계정"
        for window_title in get_window_titles():
            if auth_chrome_tab_title_pattern in window_title:
                auth_chrome_tab_title = window_title
                break

        if not is_window_title_front(window_title=auth_chrome_tab_title):
            ensure_window_to_front(window_title_seg=auth_chrome_tab_title)

        if is_window_title_front(window_title=auth_chrome_tab_title):
            ensure_spoken("gemini cli 인증창 맨 앞으로 이동")
            ensure_pressed("ctrl", "l")
            ensure_slept(milliseconds=77)
            url = get_text_dragged()
            # signature = "https://developers.google.com/gemini-code-assist/auth"
            # signature = "https://accounts.google.com/o/oauth2/v2/auth"
            signature1 = "google"
            signature2 = "oauth2"
            if signature1 in url:
                if signature2 in url:
                    logging.debug("크롬 제미나이 로그인인증창 탐지")
                    return True

        logging.debug("크롬 제미나이 로그인인증창 미탐지")
        return False
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        ensure_spoken(read_finished_wait_mode=True)
