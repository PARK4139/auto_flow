import re
import logging

def ensure_ansi_codes_stripped(text: str) -> str:
    """
    주어진 문자열에서 ANSI 이스케이프 코드를 제거합니다.
    """
    if not isinstance(text, str):
        logging.debug(f"ensure_ansi_codes_stripped: 입력이 문자열이 아닙니다. {type(text)}")
        return str(text) # 문자열이 아니면 일단 문자열로 변환 후 반환

    # ANSI 이스케이프 코드 패턴 (예: \x1b[0m, \x1b[31m 등)
    ansi_escape_pattern = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape_pattern.sub('', text)