"""
Kiri 메인 루프
호스트와 원격에서 공통으로 사용되는 메인 로직
"""
import logging
from datetime import datetime

from pk_internal_tools.pk_kiria.pk_command_input import get_user_command_via_mode
from pk_internal_tools.pk_kiria.pk_command_processor import process_command
from pk_internal_tools.pk_kiria.pk_kiri_state_utils import (
    ensure_greeting_daily,
    parse_time_ranges,
    process_time_based_alerts,
)
from pk_internal_tools.pk_objects.pk_kiri_state import KiriMode, KiriState
from pk_internal_tools.pk_objects.pk_texts import PkTexts

logger = logging.getLogger(__name__)


def run_kiri_main_loop(state: KiriState, time_blocks_config: dict = None):
    """
    Kiri 메인 루프 실행
    
    Args:
        state: KiriState 객체
        time_blocks_config: 시간 블록 설정 딕셔너리
            예: {
                "sleep": ["00:12-05:30"],
                "lunch": ["12:00-13:00"],
                "break": ["15:00-15:15"],
                "exercise": ["18:30-18:50"]
            }
    """
    state.is_running = True

    # 시간 블록 설정
    if time_blocks_config is None:
        time_blocks_config = {
            "sleep": ["00:12-05:30"],
            "lunch": ["12:00-13:00"],
            "break": ["15:00-15:15"],
            "exercise": ["18:30-18:50"]
        }

    all_time_blocks = []
    for block_list in time_blocks_config.values():
        all_time_blocks.extend(parse_time_ranges(block_list))

    # 대화형 루프
    while state.is_running:
        try:
            ensure_greeting_daily(state)

            # 사용자 입력 받기
            user_input = get_user_command_via_mode(state.current_mode, state)

            if user_input:
                # 명령어 히스토리에 추가
                state.add_command_to_history(user_input)
                state.last_command_time = datetime.now()

            # 명령어 처리
            if not process_command(user_input, state):
                break

            logging.debug("-" * 50)

        except KeyboardInterrupt:
            logging.debug("️ 사용자가 중단했습니다.")
            break
        except Exception as e:
            error_msg = f" {PkTexts.ERROR_OCCURRED}: {e}"
            logging.debug(error_msg)
            if state.current_mode != KiriMode.SILENT:
                from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
                ensure_spoken(f"{PkTexts.ERROR_OCCURRED}")

        # 시간 기반 알림 처리
        now = datetime.now()
        process_time_based_alerts(now, state, all_time_blocks)

    # 종료 처리
    state.is_running = False
    logging.debug("Kiri를 종료합니다.")

