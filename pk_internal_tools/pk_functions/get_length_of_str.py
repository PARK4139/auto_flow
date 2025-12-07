from typing import Union

def get_length_of_str(text: Union[str, None]) -> int:
    """
    주어진 문자열의 길이를 반환합니다.
    만약 입력이 None이거나 문자열이 아니면 0을 반환합니다.

    Args:
        text (Union[str, None]): 길이를 계산할 문자열.

    Returns:
        int: 문자열의 길이.
    """
    if not isinstance(text, str):
        return 0
    return len(text)
