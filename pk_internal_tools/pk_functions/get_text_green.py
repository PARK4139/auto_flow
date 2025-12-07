
def get_text_green(text: str) -> str:
    """
    주어진 텍스트를 ANSI 이스케이프 코드를 사용하여 초록색으로 반환합니다.
    콘솔 출력을 위한 색상 지정에 사용됩니다.
    """
    try:
        import logging
        from pk_internal_tools.pk_objects.pk_files import ensure_pk_log_initialized
        ensure_pk_log_initialized(__file__)
    except ImportError:
        logging = None

    green_text = f"\033[92m{text}\033[0m"
    if logging:
        logging.debug(f"텍스트 '{text}'를 초록색으로 변환했습니다: {green_text}")
    return green_text
