
import urllib
import subprocess
import speech_recognition as sr
import requests
import re

import numpy as np
import colorama
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
from selenium.common.exceptions import ElementClickInterceptedException
from pytube import Playlist
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.set_pk_context_state import set_pk_context_state
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared

from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from enum import Enum
from cryptography.hazmat.primitives import padding
from base64 import b64encode
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pathlib import Path
from pk_internal_tools.pk_functions.is_f import is_f
import logging


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_objects.pk_files import F_MEMO_RAW, F_MEMO_TRASH_BIN_TOML


def ensure_todo_list_guided():
    import re
    from datetime import datetime
    ensure_slept(milliseconds=1000)

    from colorama import init as pk_colorama_init
    ensure_pk_colorama_initialized_once()

    # Path 객체로 직접 사용 (get_pnx_os_style 제거)
    MEMO_DONE_TXT = Path(F_MEMO_RAW) if isinstance(F_MEMO_RAW, str) else F_MEMO_RAW
    MEMO_TODO_TXT = Path(F_MEMO_RAW) if isinstance(F_MEMO_RAW, str) else F_MEMO_RAW
    MEMO_TRASH_BIN_TXT = Path(F_MEMO_TRASH_BIN_TOML) if isinstance(F_MEMO_TRASH_BIN_TOML, str) else F_MEMO_TRASH_BIN_TOML

    # explorer
    # ensure_pnx_opened_by_ext(pnx=MEMO_TODO_TXT)

    # f = rf'{__file__}'

    pnxs = [
        MEMO_TODO_TXT,
        # f,
    ]

    if not is_f(MEMO_TODO_TXT):
        print(f"할일 목록 f을 찾을 수 없습니다 {MEMO_TODO_TXT}")
        return

    # lios
    # todo_lines_list = get_list_from_f(f=memo_todo_txt)
    # todo_lines_list = get_list_removed_element_contain_str(working_list=todo_lines_list, string="#")
    # todo_lines_str = get_str_from_list(working_list=todo_lines_list, item_connector='')
    # print_with_highlighted(txt_whole=todo_lines_str, txt_highlighted_list=['2025'])
    # ensure_pk_memo_texts_found(f=f)

    # bring MEMO_TODO_TXT
    todo_lines_list = get_list_from_f(f=MEMO_TODO_TXT)

    # ## 처리
    move_memo_lines_containing_keywords_to_f(f_from=MEMO_TODO_TXT, f_to=MEMO_TRASH_BIN_TXT, keyword='##')  # useless
    # # 처리
    move_memo_lines_containing_keywords_to_f(f_from=MEMO_TODO_TXT, f_to=MEMO_DONE_TXT, keyword='#')  # done

    # 오름차순 정렬
    # todo_lines_list = get_list_sorted_element(working_list=todo_lines_list)

    # 단어간 간격 정렬
    todo_lines_list = get_list_aligned_words_gap(working_list=todo_lines_list, size=40)

    # todo : ref : 중복지우면 안된다.
    # todo_lines_list = get_list_removed_element_duplicated(working_list=todo_lines_list)

    # rewrite
    ensure_list_written_to_f(working_list=todo_lines_list, f=MEMO_TODO_TXT, mode='w', line_feed_mode=0, head_line_mode=False)

    stamp_todo_task_list = []
    # today_task_list = []
    today_and_past_task_list = []
    while 1:
        try:
            lines = get_list_from_f(f=MEMO_TODO_TXT)

            for line in lines:
                if line.startswith("[todo] "):
                    stamp_todo_task_list.append(line)

            # 오늘 날짜를 'YYYY-MM-DD' 형식으로 가져옴
            today = datetime.now().strftime('%Y-%m-%d')
            pattern_date_and_time = re.compile(r'^\[todo\] (\d{4}-\d{2}-\d{2}) \(\w+\) (\d{2}:\d{2}|__:__)')
            for line in stamp_todo_task_list:
                match = pattern_date_and_time.match(line)
                if match:
                    date_str, time_str = match.groups()
                    if date_str <= today:
                        today_and_past_task_list.append(line)
            task_name = None
            for today_and_past_task in today_and_past_task_list:
                logging.debug(f'''today_and_past_task={today_and_past_task}  ''')
                pattern_date_and_time = re.compile(r'^\[todo\] (\d{4}-\d{2}-\d{2}) \(\w+\) (\d{2}:\d{2}|__:__)')
                match = pattern_date_and_time.match(today_and_past_task)
                date_str, time_str = match.groups()
                pattern_time = r'\b\d{2}:\d{2}\b'
                match = re.search(pattern_time, today_and_past_task)
                if match:
                    stamp_time = match.group()
                    HH = match.group().split(':')[0]
                    mm = match.group().split(':')[1]
                else:
                    stamp_time = "__:__"
                task_name = today_and_past_task.split(stamp_time)[1].split("[")[0].split('"')[1].strip()
                logging.debug(f'{task_name} 수행미션 부여되었습니다 ({date_str} {stamp_time})')
                # speak(f'{task_name} 수행미션 부여되었습니다')
                logging.debug("미션을 완료하셨다면 Enter 키를 눌러주세요...")
                # speak("미션을 완료하셨다면 Enter 키를 눌러주세요...")
                answer = input()
                answer = answer.strip()
                if answer == "":
                    prompt_positive = rf"{task_name.replace("\n", "")}를 수행미션완료 처리합니다"
                    logging.debug(prompt_positive)
                    # speak(prompt_positive)
                    today_and_past_task_list.remove(today_and_past_task)
                    # 해당 줄을 주석 처리
                    line_hashtaged = f"# {today_and_past_task}\n"
                    # f에 변경사항을 저장
                    task_list = get_list_from_f(f=MEMO_TODO_TXT)
                    task_list = get_list_deduplicated(working_list=task_list)
                    task_list.remove(today_and_past_task)
                    task_list.append(line_hashtaged)
                    ensure_list_written_to_f(f=MEMO_TODO_TXT, working_list=task_list, mode="w", line_feed_mode=0)
                # print(rf"{today_task} {today_task.split(':')[:2]}")
            logging.debug("오늘도 모든 미션을 수행하셨습니다. 수고하셨습니다")
            # speak("오늘도 모든 미션을 수행하셨습니다. 수고하셨습니다")
            ensure_slept(seconds=1)
        except KeyboardInterrupt:
            logging.debug("프로그램이 사용자에 의해 종료되었습니다.")
            break
        except Exception as e:
            logging.debug(f"오류가 발생했습니다: {e}")
            ensure_slept(seconds=60)  # 오류 발생 시 1분 후 재시도
