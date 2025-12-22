from typing import Any, Tuple, Optional

def get_str_from_tuple(input_tuple: Optional[Tuple[Any, ...]], separator: str = "") -> str:
    """
    주어진 튜플의 모든 요소를 문자열로 변환한 후, 지정된 구분자로 이어붙여 하나의 문자열로 반환합니다.
    기본 구분자는 빈 문자열("")입니다.

    - 튜플이 아니거나 None인 경우, 입력값 자체를 문자열로 변환하여 반환합니다.
    - 튜플이 비어있으면 빈 문자열을 반환합니다.
    - 각 요소는 str()을 통해 문자열로 변환됩니다.

    Args:
        input_tuple: 처리할 튜플.
        separator: 요소들을 이어붙일 때 사용할 구분자 문자열. 기본값은 "".

    Returns:
        모든 요소가 이어붙여진 최종 문자열.
    """
    import logging

    if not isinstance(input_tuple, tuple):
        logging.debug(f"입력값이 튜플이 아닙니다. 받은 값: {input_tuple}. 전체를 문자열로 변환합니다.")
        return str(input_tuple) if input_tuple is not None else ""

    # 각 요소를 str()로 변환한 후, separator로 join
    return separator.join(map(str, input_tuple))
