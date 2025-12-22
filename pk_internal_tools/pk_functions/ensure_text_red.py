def ensure_text_red(text: str) -> str:
    """
    주어진 텍스트를 ANSI 이스케이프 코드를 사용하여 빨간색으로 포맷하여 반환합니다.

    Args:
        text (str): 빨간색으로 만들 텍스트.

    Returns:
        str: 빨간색으로 포맷된 텍스트.
    """
    # lazy import
    try:
        import logging
    except ImportError:
        pass # Fallback or handle error if logging is critical

    # ANSI escape code for red text
    RED = "\033[31m"
    RESET = "\033[0m"

    formatted_text = f"{RED}{text}{RESET}"
    if 'logging' in locals():
        logging.debug(f"Formatted text to red: {formatted_text}")
    return formatted_text
