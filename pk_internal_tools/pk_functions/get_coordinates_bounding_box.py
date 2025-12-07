from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_coordinates_bounding_box(image, search_text):
    import inspect
    import easyocr
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # EasyOCR로 텍스트 및 위치 추출
    reader = easyocr.Reader(['en', 'ko'])  # 영어와 한글을 동시에 처리하려면 'en', 'ko' 지정
    results = reader.readtext(image)

    # 추출된 텍스트와 위치 반환
    for result in results:
        text = result[1]  # result[1]은 텍스트
        if search_text.lower() in text.lower():
            coord_bounding_box = result[0]  # result[0]은 바운딩 박스 좌표
            return coord_bounding_box
    print(f"{search_text}에 대한 바운딩 박스가 화면에 없습니다. ")
