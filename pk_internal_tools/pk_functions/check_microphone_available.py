from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def check_microphone_available():
    import logging
    from pk_internal_tools.pk_functions.is_mic_device_connected_2025_10_20 import is_mic_device_connected_2025_10_20
    """마이크 사용 가능 여부 확인 - 기존 함수 활용"""
    try:
        # 기존 마이크 감지 함수 사용
        mic_connected = is_mic_device_connected_2025_10_20()

        if mic_connected:
            logging.debug("마이크가 감지되었습니다.")
            return True
        else:
            logging.debug("마이크가 감지되지 않습니다.")
            return False

    except Exception as e:
        logging.debug(f"마이크 확인 중 오류: {e}")
        return False
