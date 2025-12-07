from enum import Enum
from typing import List


class KiriMode(Enum):
    """Kiri 모드 열거형"""
    VOICE_CONVERSATION = "음성대화모드"
    KEYBOARD_CONVERSATION = "키보드대화모드"
    HYBRID = "하이브리드모드"
    DEBUG = "디버그모드"
    SILENT = "조용한모드"


class ProcessMatcher:
    """프로세스 매칭 클래스"""

    def __init__(self):
        pass

    def find_dynamic_matches(self, command: str) -> List[str]:
        # 동적 매칭 로직 구현
        return []

    def print_dynamic_mapping(self, command: str):
        # 동적 매핑 출력 로직 구현
        pass


class KiriState:
    """Kiri 상태 관리 클래스"""

    def __init__(self):

        from pk_internal_tools.pk_functions.check_microphone_available import check_microphone_available

        import logging

        # 마이크 사용 가능 여부에 따라 초기 모드 결정
        if check_microphone_available():
            self.current_mode = KiriMode.VOICE_CONVERSATION
            logging.debug("마이크가 감지되어 음성 대화 모드로 시작합니다.")
        else:
            self.current_mode = KiriMode.KEYBOARD_CONVERSATION
            logging.debug("️ 키보드 대화 모드로 시작합니다.")

        self.is_running = False
        self.last_command_time = None
        self.command_history = []
        self.alerted_blocks = set()
        self.last_cleared_hour = -1
        # 새로운 필드들 추가
        self.command_cache = {}  # 명령어 실행 결과 캐시
        self.process_cache = {}  # 프로세스 목록 캐시
        self.cache_timestamp = None
        self.cache_duration = 300  # 5분 캐시
        self.microphone_available = check_microphone_available()  # 마이크 상태 저장
        self.process_matcher = ProcessMatcher()  # 프로세스 매칭기

        # 음성 인식 오류 카운터 추가
        self.voice_recognition_error_count = 0
        self.max_voice_errors = 30  # 30번 오류 후 CLI 모드로 전환

    def switch_mode(self, new_mode: KiriMode):

        import logging

        """모드 전환 - 마이크 상태 확인"""
        old_mode = self.current_mode

        # 음성 대화 모드로 전환하려면 마이크가 필요
        if new_mode in [KiriMode.VOICE_CONVERSATION, KiriMode.HYBRID]:
            if not self.microphone_available:
                logging.debug("마이크가 연결되지 않아 음성 대화 모드로 전환할 수 없습니다.")
                return old_mode

        self.current_mode = new_mode
        logging.debug(f"Kiri 모드 변경: {old_mode.value} → {new_mode.value}")
        return old_mode

    def add_command_to_history(self, command: str):
        from datetime import datetime

        """명령어 히스토리에 추가"""
        self.command_history.append({
            'command': command,
            'timestamp': datetime.now(),
            'mode': self.current_mode.value
        })
        # 최근 100개만 유지
        if len(self.command_history) > 100:
            self.command_history.pop(0)

    def get_cached_processes(self):
        from datetime import datetime

        import logging
        from pk_internal_tools.pk_functions.get_sorted_pk_files import get_excutable_pk_wrappers

        """캐시된 프로세스 목록 반환"""
        now = datetime.now()
        if (self.cache_timestamp is None or
                (now - self.cache_timestamp).seconds > self.cache_duration):
            try:
                self.process_cache = get_excutable_pk_wrappers()
                self.cache_timestamp = now
            except Exception as e:
                logging.debug(f"️ 프로세스 목록 캐시 오류: {e}")
        return self.process_cache

    def check_microphone_status(self):
        from pk_internal_tools.pk_functions.is_mic_device_connected_2025_10_20 import is_mic_device_connected_2025_10_20
        """마이크 상태 재확인 - 기존 함수 활용"""
        self.microphone_available = bool(is_mic_device_connected_2025_10_20())
        return self.microphone_available

    def increment_voice_error_count(self):

        import logging

        """음성 인식 오류 카운터 증가 및 키보드 대화 모드 전환 체크"""
        self.voice_recognition_error_count += 1
        logging.debug(f"음성 인식 오류 {self.voice_recognition_error_count}/{self.max_voice_errors}")

        # 디버깅 정보 추가
        if self.current_mode == KiriMode.DEBUG:
            logging.debug(f"[DEBUG] 현재 모드: {self.current_mode.value}, 마이크 상태: {self.microphone_available}")

        if self.voice_recognition_error_count >= self.max_voice_errors:
            logging.debug(f"️ 음성 인식 오류가 {self.max_voice_errors}번 발생하여 키보드 대화 모드로 자동 전환합니다.")
            self.switch_mode(KiriMode.KEYBOARD_CONVERSATION)
            self.voice_recognition_error_count = 0  # 카운터 리셋
            return True
        return False

    def reset_voice_error_count(self):

        import logging

        """음성 인식 오류 카운터 리셋"""
        old_count = self.voice_recognition_error_count
        self.voice_recognition_error_count = 0
        logging.debug(f"음성 인식 성공! 오류 카운터 리셋: {old_count} → 0")
