def ensure_console_paused(text=None):
    import logging

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    func_n = get_caller_name()
    logging.debug(PK_UNDERLINE)
    if text is None:
        # 부가 정보(함수명)를 노란색으로 출력
        logging.info(get_text_yellow(f"paused by {func_n}()"))
        text = "continue:enter"
    else:
        # text가 이미 노란색 텍스트이거나 일반 텍스트일 수 있음
        # text에 부가 정보가 포함되어 있으면 이미 출력되었을 것으로 가정
        text = f'{text}'
    input(text)
