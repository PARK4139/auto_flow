from pk_internal_tools.pk_functions import ensure_spoken


def ensure_text_clicked_via_ocr(text, doubleclick_mode=False):
    from pk_internal_tools.pk_functions.does_text_bounding_box_exist_via_easy_ocr import \
        does_text_bounding_box_exist_via_easy_ocr
    from pk_internal_tools.pk_functions.click_mouse_left_btn import click_mouse_left_btn
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    import time
    time_limit = 20
    time_s = time.time()
    msg = rf"광학 문자 인식을 통하여 클릭할 텍스트를 찾습니다."
    ensure_spoken(msg)
    while 1:
        if time.time() - time_s > time_limit:
            break
        if does_text_bounding_box_exist_via_easy_ocr(string=text):
            click_mouse_left_btn(doubleclick_mode=doubleclick_mode)
            break
        ensure_slept(seconds=0.5)
