import logging
from pathlib import Path

def ensure_split_text_for_tts(text: str, delimiters: list[str] = None) -> list[str]:
    """
    텍스트를 지정된 구분자(기본값: 쉼표)를 기준으로 분리합니다.
    분리된 각 구문은 공백이 제거됩니다.
    """
    if delimiters is None:
        delimiters = [',', '，'] # 기본 구분자: 쉼표 (한글, 영어)

    parts = [text]
    for delimiter in delimiters:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(delimiter))
        parts = new_parts
    
    # 각 부분의 앞뒤 공백 제거 및 빈 문자열 제거
    cleaned_parts = [part.strip() for part in parts if part.strip()]
    
    logging.debug(f"Original text: '{text}' split into: {cleaned_parts}")
    return cleaned_parts
