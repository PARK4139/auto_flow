from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

import logging
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.does_pnx_exist import is_pnx_existing


def collect_img_for_autogui():
    import inspect
    import sys
    import traceback

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    server_time = get_pk_time_2025_10_20_1159('%Y_%m_%d_%H_%M_%S')
    func_n_server_time_png = rf'{d_pk_external_tools}\{func_n}_{server_time}.png'
    f = func_n_server_time_png
    f_p = get_p(func_n_server_time_png)
    file_nx = get_nx(func_n_server_time_png)
    ensure_pnx_made(f_p, mode="d")
    try:
        ensure_pressed("win", "shift", "s", interval=0.5)
        key = "ctrl+s"
        if not is_keyboard_pressed_within_time_limit(key_plus_key=key, time_limit=60):
            logging.debug(rf"[red] 클릭감지타임아웃 {key}")
        ensure_slept(milliseconds=500)
        ensure_slept(milliseconds=500)
        ensure_pressed("ctrl", "l", interval=0.5)
        ensure_slept(milliseconds=300)
        ensure_text_saved_to_clipboard(text_working=f_p)
        ensure_slept(milliseconds=300)
        ensure_pressed("enter")
        ensure_slept(milliseconds=300)
        ensure_printed_as_gui(ment="클립보드에 추천f명을 저장해두었습니다")
        key = "left"
        if not is_mouse_button_click_within_time_limit(key="left", time_limit=60):
            ment_error = rf"[red] 클릭감지타임아웃 {key}"
            # raise FridayLogicError(ment_error)
            logging.debug(ment_error)
        ensure_writen_fast(file_nx)
        ensure_slept(milliseconds=300)
        # press("enter")
        ensure_slept(milliseconds=300)
        if is_pnx_existing(pnx=f):
            cmd = rf"taskkill -im ScreenSketch.exe"
        text_editor = 'explorer.exe'
        cmd = f'{text_editor} "{f_p}" '
        ensure_command_executed(cmd=cmd)
    except:
        traceback.print_exc(file=sys.stdout)
