from typing import List

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_str_removed_from_numbered_strs(items: List[str]) -> List[str]:
    """ get_numbered_items() 의 반대기능 """
    import re
    import logging
    cleaned_items = []
    for item in items:
        # 정규식으로 앞부분 숫자 + 점 + 공백 제거
        cleaned = re.sub(r'^\d+\.\s*', '', item)
        cleaned_items.append(cleaned)
        logging.debug(f"removed numbering: '{item}' -> '{cleaned}'")
    return cleaned_items
