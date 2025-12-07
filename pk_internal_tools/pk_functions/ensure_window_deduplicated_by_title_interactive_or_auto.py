import logging
import traceback
from typing import List, Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.ensure_process_deduplicated import ensure_process_deduplicated
from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
from pk_internal_tools.pk_functions.get_values_sanitize_for_cp949 import get_values_sanitize_for_cp949


@ensure_seconds_measured
def ensure_window_deduplicated_by_title_interactive_or_auto(
    deduplicated_window_titles_to_kill: Optional[List[str]] = None
) -> None:
    """
    지정된 창 제목 목록에 대해 중복을 제거하거나,
    목록이 주어지지 않으면 fzf를 사용하여 사용자가 선택한 창의 중복을 제거합니다.

    Args:
        deduplicated_window_titles_to_kill (Optional[List[str]]):
            중복 제거할 창 제목들의 목록. None이면 fzf로 선택합니다.
    """
    func_n = get_caller_name()
    logging.debug(f"'{func_n}' 함수 실행 시작")

    try:
        titles_to_process: List[str] = []

        if deduplicated_window_titles_to_kill is None:
            logging.info("중복 제거할 창 제목이 지정되지 않아 fzf로 선택합니다.")
            # 1. 현재 열린 창 제목 목록 확보
            all_window_titles = get_windows_opened_with_hwnd()
            all_window_titles = [get_values_sanitize_for_cp949(title) for title in all_window_titles]
            all_window_titles = sorted(list(set(all_window_titles))) # 중복 제거 및 정렬

            if not all_window_titles:
                logging.info("열려있는 창이 없어 중복 제거할 대상을 찾을 수 없습니다.")
                return

            # 2. fzf를 사용하여 사용자에게 선택 요청
            key_name = "select_window_to_deduplicate"
            selected_titles_raw = ensure_value_completed_2025_10_13_0000(
                key_name=key_name,
                func_n=func_n,
                options=all_window_titles,
                guide_text="중복 제거할 창 제목을 선택하세요 (다중 선택 가능):",
                multi_select=True # 다중 선택 활성화
            )
            
            if selected_titles_raw is None:
                logging.info("사용자가 창 선택을 취소했습니다.")
                return
            
            # ensure_value_completed_2025_10_13_0000는 단일 문자열 또는 리스트를 반환할 수 있음
            if isinstance(selected_titles_raw, str):
                titles_to_process = [selected_titles_raw]
            else:
                titles_to_process = selected_titles_raw

            if not titles_to_process:
                logging.info("선택된 창 제목이 없어 중복 제거를 진행하지 않습니다.")
                return

        else:
            logging.info("지정된 창 제목 목록에 대해 중복 제거를 시작합니다.")
            titles_to_process = deduplicated_window_titles_to_kill
            if not titles_to_process:
                logging.warning("deduplicated_window_titles_to_kill 목록이 비어 있습니다.")
                return

        logging.info(f"다음 창 제목들에 대해 중복 제거를 시도합니다: {titles_to_process}")
        for title in titles_to_process:
            logging.debug(f"창 제목 '{title}'에 대해 중복 제거 중...")
            ensure_process_deduplicated(window_title_seg=title, exact=True)
            # 짧은 대기 추가 (선택 사항, 필요시)
            # from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
            # ensure_slept(milliseconds=100)
        
        logging.info("중복 제거 작업이 완료되었습니다.")

    except Exception as e:
        logging.error(f"중복 제거 중 오류 발생: {e}", exc_info=True)
    finally:
        logging.debug(f"'{func_n}' 함수 실행 종료")

