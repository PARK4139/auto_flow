def get_img_when_img_recognized_succeed(img_abspath, recognize_loop_limit_cnt=0, is_zoom_toogle_mode=False):
    import pyautogui
    import logging

    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_objects.pk_gui import PkGui

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # speak("화면 이미지 분석을 시도합니다")
    PkGui.pop_up_as_complete(title="화면이미지분석 시도 전 보고", ment="화면 이미지 분석을 시도합니다", auto_click_positive_btn_after_milliseconds=1)

    ensure_pressed('ctrl', '0')  # 이미지 분석 시 크롬 zoom 초기화(ctrl+0)

    # 고해상도/다크모드 에서 시도
    for i in range(0, 9):
        ensure_pressed('ctrl', '+')

    chrome_zoom_step = 0

    # 루프카운트 제한 n번 default 0번 으로 설정
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    loop_cnt = 0
    # recognize_loop_limit_cnt=recognize_loop_limit_cnt
    if recognize_loop_limit_cnt == 0:
        while 1:
            # 인식률 및 속도 개선 시도
            # pip install opencv-python # 이것은 고급 기능이 포함되지 않은 Python용 OpenCV의 미니 버전입니다. 우리의 목적에는 충분합니다.
            # confidence=0.7(70%)유사도를 낮춰 인식률개선시도, region 낮춰 속도개선시도, grayscale 흑백으로 판단해서 속도개선시도,
            # open cv 설치했는데 적용안되고 있음. 재부팅도 하였는 데도 안됨.
            # xy_infos_of_imgs=pyautogui.locateOnScreen(img_abspath, confidence=0.7, grayscale=True)
            # debug_as_gui(xy_infos_of_imgs is None)
            logging.debug("화면 이미지 인식 시도 중...")
            loop_cnt = loop_cnt + 1
            try:
                img = pyautogui.locateOnScreen(img_abspath, confidence=0.7, grayscale=True)
                logging.debug(type(img))
                logging.debug(img)
                logging.debug(img is not None)
                if img is not None:
                    return img
                else:
                    logging.debug(f"화면 이미지 분석 중...")
                    logging.debug(img_abspath)
                    ensure_slept(milliseconds=15)
                    if is_zoom_toogle_mode:
                        if chrome_zoom_step == 14:
                            chrome_zoom_step = 0
                        elif chrome_zoom_step < 7:
                            ensure_pressed('ctrl', '-')
                            chrome_zoom_step = chrome_zoom_step + 1
                        elif 7 <= chrome_zoom_step:
                            ensure_pressed('ctrl', '+')
                            chrome_zoom_step = chrome_zoom_step + 1
            except pyautogui.ImageNotFoundException:
                logging.debug(f"{loop_cnt}번의 화면인식시도를 했지만 인식하지 못하였습니다")
                pass
    else:
        while 1:
            loop_cnt = loop_cnt + 1
            logging.debug("화면 이미지 인식 시도 중...")
            if recognize_loop_limit_cnt == loop_cnt:
                logging.debug(f"{loop_cnt}번의 화면인식시도를 했지만 인식하지 못하였습니다")
                return None
            try:
                img = pyautogui.locateOnScreen(img_abspath, confidence=0.7, grayscale=True)
                logging.debug(type(img))
                logging.debug(img)
                logging.debug(img is not None)
                if img is not None:
                    return img
            except Exception as e:
                logging.debug(img_abspath)
                ensure_slept(milliseconds=10)
                if is_zoom_toogle_mode == True:
                    if chrome_zoom_step == 14:
                        chrome_zoom_step = 0
                    elif chrome_zoom_step < 7:
                        ensure_pressed('ctrl', '-')
                        chrome_zoom_step = chrome_zoom_step + 1
                    elif 7 <= chrome_zoom_step:
                        ensure_pressed('ctrl', '+')
                        chrome_zoom_step = chrome_zoom_step + 1
