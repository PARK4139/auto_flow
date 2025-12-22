from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_text_coordinates_via_easy_ocr(string):  # 한글인식 잘 안되는 듯하다
    import logging
    from pk_internal_tools.pk_functions.get_center_of_bounding_box import get_center_of_bounding_box
    from pk_internal_tools.pk_functions.get_coordinates_bounding_box import get_coordinates_bounding_box
    from pk_internal_tools.pk_functions.get_screenshot import get_screenshot

    # 화면 캡처
    screenshot = get_screenshot()

    # EsayOCR을 통해 모든텍스트 바운딩박스좌표 추출
    # coordinates_bounding_box = get_all_text_with_coordinates_via_easy_ocr(screenshot)
    # print_list_as_vertical(working_list=coordinates_bounding_box, items_name="coordinates_bounding_box")

    # EsayOCR을 통해 특정텍스트 바운딩박스좌표 추출
    coordinates_bounding_box = get_coordinates_bounding_box(image=screenshot, search_text=string)
    # print_list_as_vertical(working_list=coordinates_bounding_box, items_name="coordinates_bounding_box")

    # 중심 좌표 구하기
    if get_center_of_bounding_box(coordinates_bounding_box) is not None:
        center_x, center_y = get_center_of_bounding_box(coordinates_bounding_box)
        # logging.debug(string = rf'''center_x="{center_x}"  ''')
        # logging.debug(string = rf'''center_y="{center_y}"  ''')
        logging.debug(f'''"text_coordinates = ({center_x}, {center_y})"''')
        return center_x, center_y
    return None
