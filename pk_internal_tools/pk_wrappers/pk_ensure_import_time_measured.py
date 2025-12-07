import logging
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE


def measure_time_to_import_module_via_time():
    modules = [
        # 기본 라이브러리
        "asyncio", "datetime", "inspect", "json", "os", "platform", "random", "re", "shutil", "string", "subprocess", "sys", "threading", "time", "traceback", "urllib", "webbrowser", "zipfile", "collections.Counter", "functools.partial", "typing.TypeVar", "typing.List", "urllib.parse.quote", "urllib.parse.urlparse", "zipfile.BadZipFile",

        # 외부 라이브러리
        "chardet", "clipboard", "cv2", "easyocr", "ipdb", "keyboard", "mutagen", "numpy as np", "pandas as pd", "psutil", "pyaudio", "pyautogui", "pygetwindow", "pyglet", "pywintypes", "requests", "selenium.webdriver as webdriver", "send2trash", "speech_recognition as sr", "tqdm", "win32con", "win32gui", "win32process", "PIL.Image", "PIL.ImageFont", "PIL.ImageDraw", "PIL.ImageFilter",
        "playwright.sync_api as sync_playwright", "bs4.BeautifulSoup", "bs4.ResultSet", "dirsync.sync", "fastapi.HTTPException", "gtts.gTTS", "moviepy.VideoFileClip", "pynput.mouse", "pytube.Playlist", "selenium.webdriver.chrome.options as Options", "selenium.webdriver.common.by as By",

        # 사용자 정의 모듈
        "legacy.CustomErrorUtil", "legacy.DataStructureUtil", "pk_external_tools.interface_cmd_line.logging.debug", "pk_external_tools.interface_cmd_line.print_light_black", "pk_external_tools.interface_cmd_line.print_cyan", "pk_external_tools.interface_cmd_line.print_with_underline", "pk_external_tools.interface_cmd_line.print_red", "pk_external_tools.interface_cmd_line.print_magenta", "pk_external_tools.interface_cmd_line.print_light_white",
        "pk_external_tools.interface_cmd_line.ColoramaUtil", "pk_external_tools.interface_cmd_line.print_ment_via_colorama",
        "pk_external_tools.interface_cmd_line.print_success", "pk_external_tools.interface_cmd_line.print_light_yellow", "pk_external_tools.interface_cmd_line.print_yellow",
        "pk_external_tools.constants.USERPROFILE", "pk_external_tools.constants.HOSTNAME", "pk_external_tools.constants.PK_UNDERLINE",
        "pk_external_tools.constants.BLANK", "pk_external_tools.constants.BIGGEST_PNXS", "pk_external_tools.constants.SMALLEST_PNXS",
        "pk_external_tools.constants.PLAYING_SOUNDS", "pk_external_tools.constants.COUNTS_FOR_GUIDE_TO_SLEEP",
        "pk_external_tools.constants.[]", "pk_external_tools.constants.VIDEO_IDS_ALLOWED",
        "pk_external_tools.constants.AUDIO_IDS_ALLOWED", "pk_external_tools.constants.STORAGE_VIDEOES_MERGED",
        "pk_external_tools.constants.PROJECT_PARENTS_DIRECTORY", "pk_external_tools.constants.DESKTOP",
        "pk_external_tools.constants.DOWNLOADS", "pk_external_tools.constants.pk_external_tools", "pk_external_tools.constants.PKG_DPL",
        "pk_external_tools.constants.PKG_CACHE_PRIVATE", "pk_external_tools.constants.CLASSIFYING", "pk_external_tools.constants.RECYCLE_BIN",
        "pk_external_tools.constants.LOCAL_PKG_CACHE_PRIVATE_FILE", "pk_external_tools.constants.SUCCESS_LOG", "pk_external_tools.constants.SCHECLUER_YAML", "pk_external_tools.constants.YT_DLP_CMD",
        "pk_external_tools.constants.JQ_WIN64_EXE", "pk_external_tools.constants.FFMPEG_EXE", "pk_external_tools.constants.DB_YAML",
        "pk_external_tools.constants.USELESS_FILE_NAMES_TXT", "pk_external_tools.constants.SILENT_MP3",
        "pk_external_tools.constants.PKG_IMAGE_AND_VIDEO_AND_SOUND_POTPLAYER64_DPL", "pk_external_tools.constants.PKG_VIDEO_POTPLAYER64_DPL",
        "pk_external_tools.constants.MERGED_EXCEL_FILE", "pk_external_tools.constants.PROJECT_D",
        "pk_external_tools.constants.YES", "pk_external_tools.constants.NO", "pk_external_tools.constants.NOT_PREPARED_YET",
        "pk_external_tools.gui.PkGui", "pk_external_tools.gui.get_display_info", "times.get_pk_time_2025_10_20_1159"
    ]
    import time
    test_result_list = []
    for module in modules:
        start_time = time.time()
        try:
            exec(f"import {module}")
            test_result_list.append(f"in {time.time() - start_time:.4f} seconds  {module:60s} imported")
        except Exception as e:
            test_result_list.append(f"in {time.time() - start_time:.4f} seconds  {module:60s} FAILED ({e})")

    test_result_list = sorted(test_result_list)
    print("".join(test_result_list))


def function_to_test():
    pass



def ensure_seconds_measured_to_exec_function_via_time():
    import time
    import inspect
    func_n = get_caller_name()
    logging.debug(rf'''{PK_UNDERLINE}{func_n}() s %%%FOO%%%''')
    debug_mode = True
    total_start = time.time()
    try:
        start = time.time()
        function_to_test()
        print(f"function_to_test() took {time.time() - start:.2f} seconds")
    except Exception as e:
        print(f"Exception occurred: {e}")
    print(f"Total execution time: {time.time() - total_start:.2f} seconds")
    logging.debug(rf'''{PK_UNDERLINE}{func_n}() e %%%FOO%%%''')




if __name__ == '__main__':
    debug_mode = True
    try:
        # todo
        # ipdb.set_trace()
        measure_time_to_import_module_via_time()
    except Exception as e:
        # debug
        import ipdb

        ipdb.set_trace()
