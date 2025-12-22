"""
원격 서버용 Kiri 시스템 실행 함수
Xavier 원격 서버에서 실행되는 Kiri 시스템입니다.
호스트용과 동일한 메인 로직을 사용하여 일관성을 유지합니다.
"""
import logging

from pk_internal_tools.pk_kiria.pk_command_mapper import ProcessMatcher
from pk_internal_tools.pk_kiria.pk_kiri_main import run_kiri_main_loop
from pk_internal_tools.pk_objects.pk_kiri_state import KiriState



def ensure_pk_kiria_executed_on_remote_target():
    """
    원격 서버용 Kiri 시스템 실행 함수
    
    Xavier 원격 서버에서 실행되며, 호스트와 동일한 메인 로직을 사용합니다.
    """
    # 상태 초기화
    state = KiriState()
    state.process_matcher = ProcessMatcher()
    
    # 메인 루프 실행 (호스트/원격 공통 로직)
    run_kiri_main_loop(state)
