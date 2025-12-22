
import re
import logging

def get_str_removed_bracket_hashed_prefix(item: str) -> str:
    """
    주어진 문자열에서 "[hash]" 형식의 해시 접두사를 제거합니다.

    Args:
        item (str): 해시 접두사가 포함될 수 있는 문자열.

    Returns:
        str: 해시 접두사가 제거된 문자열.
    """
    if not isinstance(item, str):
        item = str(item)

    # "[hash]" 패턴을 제거하는 정규 표현식
    # 예: "[abcdef] original_item" -> "original_item"
    cleaned_item = re.sub(r'^\[[a-f0-9]+\]\s*', '', item).strip()
    logging.debug(f"get_str_removed_bracket_hashed_prefix: removed hash: '{item}' -> '{cleaned_item}'")
    return cleaned_item

