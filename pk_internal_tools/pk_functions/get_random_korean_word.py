import random

from pk_internal_tools.pk_functions.extract_korean_nouns import extract_korean_nouns


def get_random_korean_noun() -> str:
    """
    입력된 텍스트에서 명사를 추출하여 랜덤으로 하나 반환합니다.
    최초 실행 시 명사 목록을 추출하여 캐시하고, 다음 호출부터는 빠르게 작동합니다.

    Args:
        text_content (str): 명사를 추출할 원본 텍스트.

    Returns:
        str: 랜덤 한국어 명사. 오류 발생 시 에러 메시지를 반환합니다.
    """

    # import logging # Already imported at top for lazy import rule

    text_content = (
        "대한민국은 동아시아에 있는 나라입니다. 수도는 서울이며, "
        "아름다운 자연과 풍부한 문화를 가지고 있습니다. "
        "많은 사람들이 한국을 방문하고 싶어 합니다."
    )

    _korean_nouns = extract_korean_nouns(text_content)

    if not _korean_nouns:
        return "추출된 명사가 없거나 명사 추출에 실패했습니다."

    return random.choice(_korean_nouns)


if __name__ == '__main__':
    for i in range(5):
        random_noun = get_random_korean_noun()
        print(f"{i + 1}: {random_noun}")
