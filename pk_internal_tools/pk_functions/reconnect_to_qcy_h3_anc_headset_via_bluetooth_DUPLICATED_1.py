
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front


def reconnect_to_qcy_h3_anc_headset_via_bluetooth():  # toogle_to_qcy_h3_anc_headset_via_bluetooth 이게 더 작명이 나은것..
    import inspect
    import time
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # Bluetooth 설정창 띄우기
    cmd = 'start ms-settings:bluetooth'
    ensure_command_executed_like_human_as_admin(cmd=cmd)
    window_title_seg = "설정"
    time_limit = 10
    time_s = time.time()
    while 1:
        if not is_window_opened(window_title_seg=window_title_seg):
            ensure_window_to_front(window_title_seg)
        else:
            break
        # logging.debug(time.time() - time_s)
        if time.time() - time_s > time_limit:
            break
        ensure_slept(seconds=0.5)

    # string 더블 클릭
    ensure_text_clicked_via_ocr(text="QCY H3 ANC HEADSET", doubleclick_mode=True)

    # string 더블 클릭
    import asyncio
    asyncio.run(shoot_custom_screenshot_via_asyncio())
    # click_img_via_autogui()

    # string 더블 클릭
    # ensure_text_clicked_via_ocr(text="연결", doubleclick_mode=True)
    pass
