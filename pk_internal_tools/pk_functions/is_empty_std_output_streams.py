import logging


# @ensure_seconds_measured
def is_empty_std_output_streams(std_output_streams):
    # std_output_streams 의 결과가 빈값이 나오면 성공인 부분에 사용하기 위한 함수
    logging.debug(f'std_output_streams={std_output_streams}')
    for idx, std_output_stream in enumerate(std_output_streams):
        if std_output_stream:  # not empty
            logging.debug(f"Non-empty stream found at index {idx}: {std_output_stream}")
            return False
    return True
