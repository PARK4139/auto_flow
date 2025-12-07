import random
import logging
from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

# 로깅 초기화는 래퍼 스크립트에서 담당하므로 여기서는 호출하지 않습니다.

def ensure_random_value_printed_between_max_and_min(min_value: int = None, max_value: int = None, num_samples: int = 1) -> list[int] | None:
    """
    지정된 최소값과 최대값 사이의 무작위 정수를 생성하여 출력하고 목록으로 반환합니다.
    인자가 None이면 사용자 입력을 받습니다.

    Args:
        min_value (int, optional): 무작위 숫자의 최소값 (포함). Defaults to None.
        max_value (int, optional): 무작위 숫자의 최대값 (포함). Defaults to None.
        num_samples (int, optional): 생성할 무작위 숫자의 샘플 수. 기본값은 1입니다.

    Returns:
        list[int] | None: 생성된 무작위 숫자 목록을 반환합니다. 오류 발생 시 None을 반환합니다.
    """
    if min_value is None:
        min_value_str = ensure_value_completed_2025_11_11(
            key_name="ensure_random_value_printed_between_max_and_min",
            func_n=get_caller_name(),
            guide_text="최소값을 입력하세요:",
        )
        try:
            min_value_str = min_value_str.strip()
            min_value = int(min_value_str)
        except (ValueError, TypeError):
            logging.error(f"잘못된 최소값입니다: '{min_value_str}'. 숫자를 입력해야 합니다.")
            return

    if max_value is None:
        max_value_str = ensure_value_completed_2025_11_11(
            key_name="ensure_random_value_printed_between_max_and_min",
            func_n=get_caller_name(),
            guide_text="최대값을 입력하세요:",
        )
        try:
            max_value_str = max_value_str.strip()
            max_value = int(max_value_str)
        except (ValueError, TypeError):
            logging.error(f"잘못된 최대값입니다: '{max_value_str}'. 숫자를 입력해야 합니다.")
            return

    # 보정값 (하드코딩)
    보정값 = 50
    logging.info(f"보정값 적용 전: 최소값={min_value}, 최대값={max_value}")
    min_value = min_value + 보정값
    max_value = max_value - 보정값
    logging.info(f"보정값 적용 후: 최소값={min_value}, 최대값={max_value}")

    if min_value > max_value:
        logging.error(f"오류: 보정값 적용 후 최소값({min_value})이 최대값({max_value})보다 클 수 없습니다. 보정값을 조정하거나 입력값을 확인하세요.")
        return

    random_numbers = [] # Added

    logging.info(f"--- {min_value}와 {max_value} 사이의 무작위 숫자 {num_samples}개 생성 ---")

    for i in range(num_samples):

        random_number = random.randint(min_value, max_value)

        logging.info(f"샘플 {i+1}: {random_number}")

        random_numbers.append(random_number) # Added

    logging.info(f"-------------------------------------------------")

    return random_numbers # Added

