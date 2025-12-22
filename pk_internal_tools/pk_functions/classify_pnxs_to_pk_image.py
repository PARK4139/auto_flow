import win32con
import pywintypes
import pythoncom
import platform
import mutagen
import colorama
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementClickInterceptedException
from prompt_toolkit import PromptSession
from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared


from mutagen.mp3 import MP3
from moviepy import VideoFileClip
from functools import lru_cache
from cryptography.hazmat.backends import default_backend
from pk_internal_tools.pk_functions.is_f import is_f


from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def classify_pnxs_to_pk_image(pnx, without_walking=True):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # target_pnx가 유효한 _d_인지 확인
    if is_f(pnx=pnx):
        logging.debug(f"{pnx} 는 정리할 수 있는 _d_가 아닙니다")
        return

    # f과 _d_ get
    txt_to_exclude_list = [
        F_DB_YAML,
        F_SUCCESS_LOG,
        F_LOCAL_PKG_CACHE_PRIVATE,
    ]
    if without_walking == False:
        dir_pnxs, file_pnxs = get_sub_pnx_list(pnx=pnx, txt_to_exclude_list=txt_to_exclude_list)
    else:
        dir_pnxs, file_pnxs = get_sub_pnx_list(pnx=pnx, txt_to_exclude_list=txt_to_exclude_list, without_walking=0)

    # f 처리
    x_allowed = [".png", '.jpg', '.jpeg', '.jfif', '.webp']
    x_allowed = x_allowed + get_list_replaced_element_from_str_to_upper_case(working_list=x_allowed)
    pnx = get_pn(pnx)
    dst = rf"{pnx}\pk_image"
    for file_pnx in file_pnxs:
        file_pnx = file_pnx[0]
        file_p = get_p(file_pnx)
        file_x = get_x(file_pnx).replace(".", "")  # 확장자에서 점(.) remove
        if file_x in [ext.replace(".", "") for ext in x_allowed]:  # x_allowed의 확장자와 비교
            ensure_pnx_made(dst, mode="d")
            ensure_pnx_moved(pnx=file_pnx, d_dst=dst)
            logging.debug(rf'''file_pnx="{file_pnx}"  ''')
    logging.debug(rf'''dst="{dst}"  ''')
