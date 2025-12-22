"""
명령어 입력 관련 함수들
음성/키보드 입력을 처리합니다.
"""
import logging
from typing import Optional

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers
from pk_internal_tools.pk_objects.pk_kiri_state import KiriMode, KiriState

logger = logging.getLogger(__name__)


def get_user_command_via_mode(mode: KiriMode, state: Optional[KiriState] = None) -> str:
    """모드에 따라 사용자 명령어를 받습니다."""
    try:
        if mode == KiriMode.VOICE_CONVERSATION:
            return get_voice_command_with_error_tracking(state)
        elif mode == KiriMode.HYBRID:
            # 하이브리드 모드에서는 음성 우선, 실패시 키보드
            try:
                return get_voice_command_with_error_tracking(state)
            except Exception as e:
                return get_cli_command(state)
        else:  # KEYBOARD_CONVERSATION, SILENT, DEBUG
            return get_cli_command(state)
    except KeyboardInterrupt:
        return "quit"
    except EOFError:
        return "quit"


def get_cli_command(state: Optional[KiriState] = None) -> str:
    """CLI 명령어 입력 받기 - 개선된 자동완성"""
    try:
        # 캐시된 프로세스 목록 사용
        pk_wrappers = state.get_cached_processes() if state else get_excutable_pk_wrappers()

        # 파일명만 추출 (경로 제거)
        import os
        process_names = [os.path.basename(f).replace('.py', '') for f in pk_wrappers]

        # 카테고리별 명령어 그룹화
        command_categories = {
            "모드 전환": [
                "mode keyboard", "keyboard mode", "키보드 모드", "mode cli", "cli mode", "텍스트 모드",
                "mode voice", "voice mode", "음성 모드", "음성 대화 모드",
                "mode hybrid", "hybrid mode", "하이브리드 모드",
                "mode silent", "silent mode", "무음 모드",
                "mode debug", "debug mode", "디버그 모드",
            ],
            "시스템 명령어": [
                "wsl 활성화",
                "history", "히스토리",
                "status", "상태"
            ],
            "PK 프로세스": process_names
        }

        # 모든 옵션 합치기
        all_options = []
        for category, commands in command_categories.items():
            all_options.extend(commands)

        # ensure_value_completed 사용하여 자동완성 기능 제공
        command = ensure_value_completed("command=", all_options)

        if command is None:
            return "quit"  # 사용자가 취소한 경우

        return command.strip()

    except Exception as e:
        # 오류 발생 시 기본 input 사용
        logging.debug(f"️ 자동완성 오류: {e}")
        return input("command=").strip()


def get_voice_command() -> str:
    """음성 명령어 입력 받기 - 개선된 버전"""
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    logging.debug(" 'kiri'라고 부르면 음성 비서가 활성화됩니다...")

    try:
        with sr.Microphone() as source:
            # 노이즈 제거 개선
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recognizer.energy_threshold = 4000  # 음성 감지 임계값 조정
            recognizer.dynamic_energy_threshold = True

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        # 여러 음성 인식 서비스 시도
        command = None
        services = [
            ('google', lambda: recognizer.recognize_google(audio, language="ko")),
            ('google', lambda: recognizer.recognize_google(audio, language="ko-KR")),
        ]

        for service_name, service_func in services:
            try:
                command = service_func()
                logging.debug(f"{service_name} 인식: {command}")
                break
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue

        if command:
            command = command.strip()
            # "kiri" wake word 확인
            if "kiri" in command.lower() or "키리" in command:
                # "kiri" 제거하고 실제 명령어만 반환
                actual_command = command.lower().replace("kiri", "").replace("키리", "").strip()
                if actual_command:
                    logging.debug(f"명령어 감지: {actual_command}")
                    return actual_command
                else:
                    logging.debug(" 무엇을 도와드릴까요")
                    # 추가 명령어 입력 받기
                    return get_voice_command()
            else:
                logging.debug("️ 'kiri'라고 부르지 않았습니다. 다시 시도해주세요.")
                return get_voice_command()
        else:
            logging.debug(" 음성을 인식하지 못했습니다. CLI 모드로 전환합니다.")
            return get_cli_command()

    except Exception as e:
        logging.debug(f"음성 인식 중 오류: {e}")
        return get_cli_command()


def get_voice_command_with_error_tracking(state: Optional[KiriState] = None) -> str:
    """오류 추적 기능이 있는 음성 명령어 입력 받기"""
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    logging.debug(" 'kiri'라고 부르면 음성 비서가 활성화됩니다...")

    # 디버깅 정보 추가
    if state and state.current_mode == KiriMode.DEBUG:
        logging.debug(f"[DEBUG] 음성 인식 시작 - 현재 오류 카운터: {state.voice_recognition_error_count}")

    try:
        with sr.Microphone() as source:
            # 노이즈 제거 개선
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            recognizer.energy_threshold = 4000  # 음성 감지 임계값 조정
            recognizer.dynamic_energy_threshold = True

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        # 여러 음성 인식 서비스 시도
        command = None
        services = [
            ('google', lambda: recognizer.recognize_google(audio, language="ko")),
            ('google', lambda: recognizer.recognize_google(audio, language="ko-KR")),
        ]

        for service_name, service_func in services:
            try:
                command = service_func()
                logging.debug(f"{service_name} 인식: {command}")
                # 성공 시 오류 카운터 리셋
                if state:
                    state.reset_voice_error_count()
                break
            except sr.UnknownValueError:
                if state and state.current_mode == KiriMode.DEBUG:
                    logging.debug(f"[DEBUG] {service_name} 서비스에서 음성 인식 실패")
                continue
            except sr.RequestError:
                if state and state.current_mode == KiriMode.DEBUG:
                    logging.debug(f"[DEBUG] {service_name} 서비스 요청 오류")
                continue

        if command:
            command = command.strip()
            # "kiri" wake word 확인
            if "kiri" in command.lower() or "키리" in command:
                # "kiri" 제거하고 실제 명령어만 반환
                actual_command = command.lower().replace("kiri", "").replace("키리", "").strip()
                if actual_command:
                    logging.debug(f"명령어 감지: {actual_command}")
                    return actual_command
                else:
                    logging.debug(" 무엇을 도와드릴까요")
                    # 추가 명령어 입력 받기
                    return get_voice_command_with_error_tracking(state)
            else:
                logging.debug("️ 'kiri'라고 부르지 않았습니다. 다시 시도해주세요.")
                return get_voice_command_with_error_tracking(state)
        else:
            # 음성 인식 실패 시 오류 카운터 증가
            if state:
                state.increment_voice_error_count()
            logging.debug(" 음성을 인식하지 못했습니다.")

            # 30회 미만이면 음성 모드 유지, 30회 이상이면 키보드 모드로 전환
            if state and state.voice_recognition_error_count >= state.max_voice_errors:
                logging.debug("️키보드 대화 모드로 전환합니다.")
                return get_cli_command(state)
            else:
                # 음성 모드 유지하면서 다시 시도
                logging.debug(" 음성 인식을 다시 시도합니다...")
                return get_voice_command_with_error_tracking(state)

    except Exception as e:
        # 음성 인식 오류 시 오류 카운터 증가
        if state:
            state.increment_voice_error_count()
        logging.debug(f"음성 인식 중 오류: {e}")

        # 30회 미만이면 음성 모드 유지, 30회 이상이면 키보드 모드로 전환
        if state and state.voice_recognition_error_count >= state.max_voice_errors:
            logging.debug("️키보드 대화 모드로 전환합니다.")
            return get_cli_command(state)
        else:
            # 음성 모드 유지하면서 다시 시도
            logging.debug(" 음성 인식을 다시 시도합니다...")
            return get_voice_command_with_error_tracking(state)

