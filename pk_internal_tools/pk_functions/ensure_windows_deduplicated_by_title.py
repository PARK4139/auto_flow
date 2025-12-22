from collections import defaultdict
from typing import List, Optional

from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed


def ensure_windows_deduplicated_by_title(title_to_deduplicate: Optional[str] = None, auto_mode=False) -> bool:
    import logging
    from pk_internal_tools.pk_functions.ensure_iterable_data_printed import ensure_iterable_data_printed
    from pk_internal_tools.pk_functions.ensure_process_deduplicated import ensure_process_deduplicated
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_values_sanitize_for_cp949 import get_values_sanitize_for_cp949
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    func_n = get_caller_name()

    try:
        titles_to_process: List[str] = []

        if title_to_deduplicate is not None:
            # 자동 방식: 인자로 받은 제목을 처리
            titles_to_process.append(title_to_deduplicate)
        else:
            # 수동 방식: 중복 창 감지 후 fzf로 선택
            # ① 열린 창 목록 확보 및 CP949 대응 처리
            values = get_windows_opened_with_hwnd()
            logging.debug(f"열린 창 개수: {len(values)}") # Debug log
            values = [get_values_sanitize_for_cp949(v[0]) for v in values]

            # ② 제목별로 그룹핑 (윈도우 제목 기준)
            grouped = defaultdict(list)
            for title in values:
                grouped[title].append(title)

            # 중복된 제목만 추출 (1개 초과)
            duplicate_titles = [title for title, instances in grouped.items() if len(instances) > 1]
            logging.debug(f"감지된 중복 창 제목 개수: {len(duplicate_titles)}") # Debug log

            if not duplicate_titles:
                logging.info("중복 창이 발견되지 않았습니다. False 반환.") # Info log
                return False

            ensure_iterable_data_printed(iterable_data=sorted(duplicate_titles), iterable_data_n="중복 감지된 창 제목들")

            if auto_mode:
                if len(duplicate_titles) > 0:
                    window_to_deduplicate = sorted(duplicate_titles)[0]
            else:
                window_to_deduplicate = ensure_values_completed(
                    key_name="window_to_deduplicate",
                    func_n=func_n,
                    options=sorted(duplicate_titles),
                    guide_text="중복 제거할 창 제목을 선택하세요 (다중 선택 가능):",
                    history_reset=True,
                )

            if window_to_deduplicate is None:
                logging.info("사용자가 창 선택을 취소했습니다.")
                return

            # ensure_value_completed는 단일 문자열 또는 리스트를 반환할 수 있음
            if isinstance(window_to_deduplicate, str):
                titles_to_process = [window_to_deduplicate]
            else:
                titles_to_process = window_to_deduplicate

        if not titles_to_process:
            logging.info("중복 제거할 창 제목이 없어 작업을 종료합니다.")
            return False # No deduplication attempts
    
        deduplicated_any = False # Initialize flag
    
        logging.info(f"다음 창 제목들에 대해 중복 제거를 시도합니다: {titles_to_process}")
        for window_title in titles_to_process:
            logging.debug(f"[처리 중] 창 제목='{window_title}' 중복 제거")
            # Assuming ensure_process_deduplicated performs an action if needed
            ensure_process_deduplicated(window_title_seg=window_title, exact=True)
            deduplicated_any = True # If we reach here, at least one attempt was made
            ensure_slept(milliseconds=200)  # 너무 빠르게 반복되지 않도록 약간 대기
    
        logging.info("중복 제거 작업이 완료되었습니다.")
        return deduplicated_any # Return true if any window was processed
            
    except Exception as e:
        logging.error(f"중복 제거 중 오류 발생: {e}", exc_info=True)
        return False # Indicate failure
