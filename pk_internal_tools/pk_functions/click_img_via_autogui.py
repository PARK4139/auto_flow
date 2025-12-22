from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def click_img_via_autogui(img, x_cal=0, y_cal=0):
    import pyautogui
    # confidence=0.7(70%)유사도를 낮춰 인식률개선시도, region 낮춰 속도개선시도, grayscale 흑백으로 판단해서 속도개선시도,

    # 이미지중앙좌표 클릭
    img_finding_loop_cnt = 0
    img_finding_loop_cnt_limit = 10
    while 1:
        img_finding_loop_cnt = img_finding_loop_cnt + 1
        try:
            x, y = pyautogui.locateCenterOnScreen(image=img, confidence=0.7, grayscale=True)
        except pyautogui.ImageNotFoundException:
            logging.debug(rf"{PkTexts.IMAGE_FIND}")
            # logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
            break
        if x is not None and y is not None:
            x_cal = x_cal
            y_cal = y_cal
            x = x - x_cal
            y = y - y_cal

            # 마우스위치 기록
            initial_position = pyautogui.position()

            duration = 1
            ensure_mouse_moved(x_abs=x, y_abs=y, duration=duration)
            pyautogui.click()

            # 마우스위치 원복
            x, y = initial_position
            duration = 0
            ensure_mouse_moved(x_abs=x, y_abs=y, duration=duration)
            # logging.debug(rf"이미지중앙좌표클릭 ({x}, {y})  ")
            break

        logging.debug(f'''{PkTexts.IMAGE_CENTER_CLICK}  ''')
        if img_finding_loop_cnt == img_finding_loop_cnt_limit:
            logging.debug(f'''{PkTexts.IMAGE_CENTER_CLICK}  ''')
            break
