# [GEMINI] START: 비동기 음성 출력 보장을 위한 수정
# ensure_spoken 함수의 동기적 대기(wait_for_completion)를 제거하는 대신,
# 프로그램이 정상적으로 종료될 때 모든 음성 출력이 완료되도록 보장하기 위해 atexit 핸들러를 등록합니다.
# 이를 통해 ensure_spoken 함수는 비동기적으로 즉시 반환되면서도, 음성이 중간에 끊기는 문제를 방지할 수 있습니다.
import atexit
import logging  # Moved logging import to top

logging.debug("ensure_spoken.py 모듈 로드 시작.")

from pk_internal_tools.pk_objects.pk_spoken_manager import SpokenManager

pk_spoken_manager = SpokenManager()
atexit.register(pk_spoken_manager.wait_for_completion)


def get_pk_spoken_manager():
    # ensure_python_app_mute_disabled()  # This call is at module level
    return pk_spoken_manager


def ensure_spoken(text="", voice_config=None, verbose=False, wait: bool = False):
    """텍스트를 음성으로 변환하여 재생합니다. 쉼표(,)가 있으면 분리하여 순차적으로 재생합니다."""
    from pk_internal_tools.pk_objects.pk_spoken_manager import VoiceConfig

    return # 의도적 return, 기능필요시 해당 줄 삭제, auto_flow 에서는 주석처리유지.

    # 예외적으로 출력
    if text != "":
        # logging.debug(rf"text={text}")
        logging.debug(rf"{text}")
    if verbose:
        logging.debug(rf"verbose={verbose}")

    manager = get_pk_spoken_manager()
    manager.set_verbose(verbose)  # for logging blocking

    if voice_config:
        if isinstance(voice_config, dict):
            config = VoiceConfig(**voice_config)
            manager.set_voice_config(config)
        elif isinstance(voice_config, VoiceConfig):
            manager.set_voice_config(voice_config)
    else:
        # 기본 voice_config 설정
        default_config = VoiceConfig(gender="male", rate=150, volume=0.8)
        manager.set_voice_config(default_config)

    # 쉼표를 기준으로 텍스트 분리
    if ',' in text:
        segments = [seg.strip() for seg in text.split(',') if seg.strip()]
        for seg in segments:
            manager.speak(seg)
    else:
        manager.speak(text)

    if wait:
        manager.wait_for_completion()

    # [2025-09-03] 비동기 음성 출력이 완료될 때까지 대기
    # SpokenManager는 비동기(백그라운드 스레드)로 동작하므로,
    # 이 함수가 먼저 종료되어 음성이 끊기는 현상을 방지하기 위해 모든 음성 출력이 완료될 때까지 명시적으로 대기합니다.
    # 이 줄을 제거하면 ensure_spoken 함수는 음성 출력을 기다리지 않고 즉시 반환됩니다.
    # manager.wait_for_completion()
