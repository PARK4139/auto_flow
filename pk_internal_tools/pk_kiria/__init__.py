"""
PkKiria 음성 비서 모듈

이 모듈은 음성 인식 및 음성 비서 기능을 제공합니다.

구조:
- 새로운 구조: pk_kiria.py (모듈화된 컴포넌트)
- 호스트용: ensure_pk_kiria_enalbled.py (로컬 PC 실행)
- 원격용: ensure_pk_kiria_executed_on_pk_xavier.py (Xavier 원격 서버 실행)
- 모듈화된 컴포넌트:
  - pk_command_mapper.py: 명령어 매핑
  - pk_command_input.py: 입력 처리
  - pk_command_processor.py: 명령어 처리
  - pk_kiri_state_utils.py: 상태 관리 유틸리티
  - pk_kiri_main.py: 메인 루프 (호스트/원격 공통)
"""

# 새로운 구조의 주요 클래스 및 함수들
from pk_internal_tools.pk_kiria.pk_kiria import (
    PkKiria,
    PkKiriaWorkflow,
    ensure_pk_kiria_executed_continuously,
    ensure_pk_kiria_executed_single_command,
)

# 호스트/원격 실행 함수들 (메인 로직 통일)
from pk_internal_tools.pk_kiria.ensure_pk_kiria_enalbled import ensure_pk_kiria_executed_2025_10_10
from pk_internal_tools.pk_kiria.ensure_pk_kiria_executed_on_pk_xavier import ensure_pk_kiria_executed_on_pk_xavier

# 모듈화된 컴포넌트들
from pk_internal_tools.pk_kiria.pk_command_mapper import DynamicCommandMapper, ProcessMatcher
from pk_internal_tools.pk_kiria.pk_command_input import (
    get_cli_command,
    get_user_command_via_mode,
    get_voice_command,
    get_voice_command_with_error_tracking,
)
from pk_internal_tools.pk_kiria.pk_command_processor import (
    execute_pk_process,
    process_command,
    suggest_and_execute_process,
    try_execute_pk_process,
)
from pk_internal_tools.pk_kiria.pk_kiri_main import run_kiri_main_loop
from pk_internal_tools.pk_kiria.pk_kiri_state_utils import (
    alert,
    ensure_greeting_daily,
    is_now_in_time_range,
    parse_time_ranges,
    process_time_based_alerts,
    show_command_history,
    show_current_status,
)

__all__ = [
    # 새로운 구조
    'PkKiria',
    'PkKiriaWorkflow',
    'ensure_pk_kiria_executed_continuously',
    'ensure_pk_kiria_executed_single_command',
    # 호스트/원격 실행 함수들
    'ensure_pk_kiria_executed_2025_10_10',  # 호스트용
    'ensure_pk_kiria_executed_on_pk_xavier',  # 원격용
    # 모듈화된 컴포넌트들
    'DynamicCommandMapper',
    'ProcessMatcher',
    'get_user_command_via_mode',
    'get_cli_command',
    'get_voice_command',
    'get_voice_command_with_error_tracking',
    'process_command',
    'try_execute_pk_process',
    'execute_pk_process',
    'suggest_and_execute_process',
    'run_kiri_main_loop',
    'parse_time_ranges',
    'is_now_in_time_range',
    'show_command_history',
    'show_current_status',
    'alert',
    'ensure_greeting_daily',
    'process_time_based_alerts',
]
