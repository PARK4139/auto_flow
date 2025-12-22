

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

import logging
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def kill_chrome_tab_duplicated():
    chrome_tab_urls_processed = []  # 이미 처리된 URL을 저장하는 리스트
    loop_limit = 10
    loop_out_cnt = 0

    while 1:
        window_title = "Chrome"
        if is_window_opened(window_title_seg=window_title):
            ensure_window_to_front(window_title)

        logging.debug(rf'''loop_out_cnt="{loop_out_cnt}"  ''')
        logging.debug(rf'''loop_limit="{loop_limit}"  ''')

        # 탭을 전환하고 URL을 가져옵니다.
        ensure_pressed("ctrl", "l")
        ensure_slept(milliseconds=5)
        url_dragged = get_text_dragged()

        # 중복 여부 확인
        if url_dragged in chrome_tab_urls_processed:
            logging.debug(rf'''URL already processed: "{url_dragged}"  ''')
            ensure_pressed("ctrl", "tab")  # 다음 탭으로 이동
            loop_out_cnt += 1
            if loop_out_cnt >= loop_limit:
                break
            continue

        # 다음 탭으로 전환 후 URL 가져오기
        ensure_pressed("ctrl", "tab")
        ensure_slept(milliseconds=5)
        ensure_pressed("ctrl", "l")
        ensure_slept(milliseconds=5)
        url_dragged_new = get_text_dragged()

        logging.debug(rf'''url_dragged="{url_dragged}"  ''')
        logging.debug(rf'''url_dragged_new="{url_dragged_new}"  ''')

        # 중복된 URL이면 탭 닫기
        if url_dragged == url_dragged_new:
            logging.debug(rf'''Closing duplicate tab for URL: "{url_dragged}"  ''')
            ensure_pressed("ctrl", "w")  # 탭 닫기
            continue

        # 처리된 URL을 리스트에 추가
        chrome_tab_urls_processed.append(url_dragged)
        logging.debug(rf'''chrome_tab_urls_processed="{chrome_tab_urls_processed}"  ''')

        # 최대 반복 횟수 초과 시 종료
        loop_out_cnt += 1
        if loop_out_cnt >= loop_limit:
            break
