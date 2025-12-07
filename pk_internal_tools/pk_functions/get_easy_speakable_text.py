from pk_internal_tools.pk_objects.pk_etc import PK_BLANK


def _is_hangul_syllable(ch: str) -> bool:
    """Return True if character is a Hangul syllable (가-힣)."""
    if not ch:
        return False
    code = ord(ch)
    return 0xAC00 <= code <= 0xD7A3


def get_easy_speakable_text(text: str) -> str:
    """
    Detect the first object korean_object_particle ('을' or '를') in Korean text
    and reformat as 'korean_object, korean_object_particle, predicate' for easier speaking.

    Rules:
    - '_' is replaced with PK_BLANK
    - Valid particles: '을', '를'
    - Consider as korean_object_particle only if the preceding char is Hangul syllable (가-힣)

    Examples:
    - '사과를먹다' -> '사과, 를, 먹다'
    - '문장을_을_테스트' -> '문장을 PK_BLANK 을 PK_BLANK 테스트' (not treated as korean_object_particle)
    """
    if not isinstance(text, str) or not text:
        return text

    # n. Replace underscores
    text = text.replace("_", PK_BLANK)

    # 2) Find first korean_object_particle candidate
    for i, ch in enumerate(text):
        if ch not in ("을", "를"):
            continue
        if i == 0:
            continue  # cannot be korean_object_particle at the start
        if not _is_hangul_syllable(text[i - 1]):
            continue  # preceding must be Hangul syllable

        # Split into grammar parts
        korean_object = text[:i].rstrip()
        korean_object_particle = ch
        korean_predicate = text[i + 1:].lstrip()

        return f"{korean_object}{korean_object_particle}, {korean_predicate}"

    # 3) If no korean_object_particle found, return original
    return text
