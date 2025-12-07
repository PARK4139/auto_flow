from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def get_str_removed_from_numbered_str(item: str) -> str:
    """
    Remove leading numbering from a single item.
    Accepts str/bytes/dict/others and normalizes to string safely.

    Examples removed:
      '1. Foo'      -> 'Foo'
      '23)  Bar'    -> 'Bar'
      '004 - Baz'   -> 'Baz'
      '7:Qux'       -> 'Qux'
      '  12 Foo'    -> 'Foo'
    """
    import re
    import logging

    original = item

    # 0) None 방지 + 대표 텍스트 추출
    if item is None:
        logging.warning("get_str_removed_from_numbered_str: received None; returning empty string")
        item = ""
    elif not isinstance(item, (str, bytes, bytearray)):
        # dict에서 대표 텍스트 키 추출 시도
        if isinstance(item, dict):
            for k in ("text", "value", "label", "name"):
                v = item.get(k)
                if isinstance(v, (str, bytes, bytearray)):
                    item = v
                    break
                if v is not None and not isinstance(v, (str, bytes, bytearray)):
                    item = str(v)
                    break
            else:
                item = str(item)
        else:
            item = str(item)

    # n. bytes -> str
    if isinstance(item, (bytes, bytearray)):
        try:
            item = item.decode("utf-8", errors="ignore")
        except Exception:
            item = item.decode(errors="ignore")

    # 2) 앞뒤 공백 제거
    s = (item or "").strip()

    # 3) 번호 제거 패턴 강화
    #    - 앞 공백 허용
    #    - 한 자리 이상 숫자
    #    - 구분자: '.', ')', ':', '-', '–', '—' 등 또는 공백
    #    - 뒤 공백 허용
    # ex) "12) ", "3. ", "004 - ", "7: ", "9 — ", "10  "
    cleaned = re.sub(r'^\s*\d+\s*[\.\)\:\-\u2013\u2014]?\s*', '', s)

    logging.debug("get_str_removed_from_numbered_str: removed numbering: %r -> %r", original, cleaned)
    return cleaned
