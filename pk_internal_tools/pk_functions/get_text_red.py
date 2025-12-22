def get_text_red(text: str) -> str:
    """
    주어진 텍스트를 ANSI 이스케이프 코드를 사용하여 빨간색으로 반환합니다.
    콘솔 출력을 위한 색상 지정에 사용됩니다.
    """
    # lazy import로 순환 import 문제 해결
    try:
        import logging
        from pk_internal_tools.pk_objects.pk_files import ensure_pk_system_log_initialized
        ensure_pk_system_log_initialized(__file__)
    except ImportError:
        # fallback: 직접 경로 계산
        logging = None

    red_text = f"\033[91m{text}\033[0m"
    if logging:
        logging.debug(f"텍스트 '{text}'를 빨간색으로 변환했습니다: {red_text}")
    return red_text
