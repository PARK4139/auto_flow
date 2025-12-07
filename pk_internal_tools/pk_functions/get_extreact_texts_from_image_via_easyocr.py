def get_extreact_texts_from_image_via_easyocr(image):
    import inspect
    import easyocr
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # EasyOCR 객체 생성
    reader = easyocr.Reader(['en', 'ko'])  # 영어와 한글을 동시에 처리하려면 'en', 'ko' 지정
    result = reader.readtext(image)
    return result
