import tomllib
import speech_recognition as sr
import shutil
import pythoncom
import importlib
import colorama
from zipfile import BadZipFile
from yt_dlp import YoutubeDL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from prompt_toolkit import PromptSession

from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_printed_once import ensure_printed_once

from pk_internal_tools.pk_objects.pk_etc import PkFilter
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from moviepy import VideoFileClip
from fastapi import HTTPException
from datetime import timedelta
from cryptography.hazmat.backends import default_backend


def find_direction_via_naver_map(destination: str):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    while 1:
        # 배경화면으로 나가기(옵션로직)
        # press("win", "m")
        # press("win", "m")
        # sleep(10)

        # 페이지 열기
        # url="https://map.naver.com/"
        url = "https://map.naver.com/p/directions"
        cmd = f'explorer  "{url}"  >NUL'
        ensure_command_executed_like_human_as_admin(cmd)
        ensure_slept(300)

        # 크롬 창 활성화
        pid_chrome_exe = get_pids(process_img_n="chrome.exe")  # chrome.exe pid 가져오기
        ensure_window_to_front(pid=pid_chrome_exe)
        ensure_slept(30)

        # 반쪽화면 생성(옵션로직)
        # press("alt", "up")
        # press("alt", "left")

        # 출발지 입력 클릭
        f_png = rf"{d_pk_root}\pk_external_tools\find_direction_via_naver_direction.png"
        click_center_of_img_recognized_by_mouse_left(img_pnx=f_png, loop_limit_cnt=100, is_zoom_toogle_mode=True)
        ensure_slept(30)

        # 한가람한양아파트상가 입력
        ensure_writen_fast("한가람한양아파트상가")
        ensure_slept(30)
        ensure_pressed('enter')
        ensure_slept(300)
        ensure_pressed('tab')
        ensure_slept(30)

        # 목적지 입력
        ensure_writen_fast(destination)
        ensure_slept(30)
        ensure_pressed('down')
        ensure_pressed('enter')

        # 길찾기 클릭
        ensure_pressed('tab')
        ensure_pressed('tab')
        ensure_pressed('tab')
        ensure_pressed('enter')

        # 작업마침 알림
        ensure_spoken(text='길찾기가 시도되었습니다')
        break
