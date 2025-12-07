from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def does_text_bounding_box_exist_via_easy_ocr(string):  # GPU 없으면 동작안함
    from pk_internal_tools.pk_functions import ensure_spoken

    from pk_internal_tools.pk_functions.ensure_mouse_moved import ensure_mouse_moved
    import logging
    from pk_internal_tools.pk_functions.get_text_coordinates_via_easy_ocr import get_text_coordinates_via_easy_ocr
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    text_coordinates = get_text_coordinates_via_easy_ocr(string=string)
    if not text_coordinates:
        msg = rf"{string}"
        ensure_spoken(msg)
        msg = rf"를 찾을 수 없었습니다"
        ensure_spoken(msg)
        print(rf"[not found] {string}")
        return 0
    x_abs, y_abs = text_coordinates
    logging.debug(rf'''x_abs="{x_abs}"  ''')
    logging.debug(rf'''y_abs="{y_abs}"  ''')
    ensure_mouse_moved(x_abs=x_abs, y_abs=y_abs)
    return 1
