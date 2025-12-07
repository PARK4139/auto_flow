import random
from typing import List, TypeVar
import logging

T = TypeVar('T')

def ensure_random_value_from_options(options: List[T]) -> T:
    """
    주어진 옵션 리스트에서 무작위 값을 선택하여 반환합니다.

    Args:
        options (List[T]): 선택할 수 있는 값들의 리스트.

    Returns:
        T: 옵션 리스트에서 무작위로 선택된 값.

    Raises:
        ValueError: 옵션 리스트가 비어 있을 경우 발생합니다.
    """
    if not options:
        logging.error("옵션 리스트가 비어 있습니다. 무작위 값을 선택할 수 없습니다.")
        raise ValueError("옵션 리스트가 비어 있습니다.")

    selected_value = random.choice(options)
    logging.debug(f"옵션 리스트에서 무작위 값 선택: {selected_value}")
    return selected_value
