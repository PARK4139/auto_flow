import logging
import random
import re
from typing import Tuple, Optional

def ensure_LM_100_spindle_test_report_dummy_data_sample_created(
    input_string: str,
    min_interval_len: int,
    offset: int,
    proper_lower_limit: int,
    proper_upper_limit: int,
    seed: Optional[int] = None,
    min_start_gap: int = 0,
    enable_length_jitter: bool = True
) -> Tuple[int, int]:
    """
    LM_100 스핀들 테스트 보고서용 더미 데이터를 생성합니다.
    입력된 단일 '시작값-끝값' 문자열을 기반으로, 지정된 인자들을 활용하여
    새로운 더미 '시작값-끝값' 쌍을 생성합니다.

    Args:
        input_string (str): 단일 '시작값-끝값' 형태의 문자열 (예: "166-254")
        min_interval_len (int): 생성될 더미 데이터의 최소 길이 (끝값 - 시작값).
        offset (int): 시작값과 끝값의 랜덤 범위 조정에 사용될 오프셋 (예: +-offset).
        seed (Optional[int]): random 모듈의 시드. None이면 시드 설정 안 함.
        min_start_gap (int): 생성될 시작값과 끝값 사이의 최소 간격. (현재는 min_interval_len과 유사하게 사용)
        enable_length_jitter (bool): 생성될 길이(차이값)에 약간의 변동을 줄지 여부.

    Returns:
        Tuple[int, int]: 생성된 더미 '시작값', '끝값' 쌍.
    """
    if seed is not None:
        random.seed(seed)

    match = re.match(r'(\d+)-(\d+)', input_string)
    if not match:
        raise ValueError(f"유효하지 않은 입력 문자열 형식: {input_string}. '시작값-끝값' 형식이 필요합니다.")

    start_in = int(match.group(1))
    end_in = int(match.group(2))

    logging.debug(f"입력: {start_in}-{end_in}, min_interval_len: {min_interval_len}, offset: {offset}")

    attempts = 0
    max_attempts = 1000 # 무한 루프 방지를 위한 최대 시도 횟수

    while attempts < max_attempts:
        # 시작값 범위 조정
        # lower_limit와 upper_limit를 고려하여 범위 설정
        start_out_min = max(proper_lower_limit, start_in - offset)
        start_out_max = min(proper_upper_limit - min_interval_len, start_in + offset) # 끝값이 upper_limit를 넘지 않도록
        
        # start_out_min이 start_out_max보다 커지는 경우를 방지
        if start_out_min > start_out_max:
            attempts += 1
            continue # 유효한 범위가 아니므로 다시 시도

        start_out = random.randint(start_out_min, start_out_max)

        # 끝값 범위 조정
        # lower_limit와 upper_limit를 고려하여 범위 설정
        end_out_min = max(start_out + min_interval_len, end_in - offset)
        end_out_max = min(proper_upper_limit, end_in + offset)
        
        # end_out_min이 end_out_max보다 커지는 경우를 방지
        if end_out_min > end_out_max:
            attempts += 1
            continue # 유효한 범위가 아니므로 다시 시도

        end_out = random.randint(end_out_min, end_out_max)

        # 최종 유효성 검사: 생성된 값이 proper_lower_limit와 proper_upper_limit 내에 있는지 확인
        if (proper_lower_limit <= start_out < end_out <= proper_upper_limit) and \
           (end_out - start_out) >= min_interval_len:
            logging.debug(f"생성된 더미: {start_out}-{end_out}")
            return start_out, end_out
        
        attempts += 1
    
    logging.warning(f"입력 ({input_string})에 대해 유효한 더미 데이터를 {max_attempts}번 시도 후 생성하지 못했습니다. 대신, 전체 유효 범위 내에서 랜덤한 더미를 생성하여 반환합니다.")
    
    # 유효한 더미 데이터를 생성하지 못한 경우, 전체 유효 범위 내에서 랜덤한 더미를 생성하여 반환
    # 이 경우에도 min_interval_len을 만족해야 함
    fallback_attempts = 0
    max_fallback_attempts = 1000
    while fallback_attempts < max_fallback_attempts:
        fallback_start = random.randint(proper_lower_limit, proper_upper_limit - min_interval_len)
        fallback_end = random.randint(fallback_start + min_interval_len, proper_upper_limit)
        
        if (proper_lower_limit <= fallback_start < fallback_end <= proper_upper_limit) and \
           (fallback_end - fallback_start) >= min_interval_len:
            logging.debug(f"폴백 더미 생성: {fallback_start}-{fallback_end}")
            return fallback_start, fallback_end
        fallback_attempts += 1
    
    # 폴백 더미 생성도 실패한 경우 (매우 드물지만), 예외 발생
    raise RuntimeError(f"폴백 더미 데이터 생성 실패: {input_string}. 유효한 범위 내에서 더미를 생성할 수 없습니다.")

# 이 함수는 래퍼 스크립트에서 호출되므로, if __name__ == "__main__": 블록은 포함하지 않습니다.
# 로깅 초기화도 래퍼 스크립트에서 담당합니다.