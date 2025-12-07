import logging
import random
import re
from typing import Tuple, List

from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
from pk_internal_tools.pk_functions.get_clipboard_text import get_clipboard_text
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_LM_100_spindle_test_report_dummy_data_sample_created import ensure_LM_100_spindle_test_report_dummy_data_sample_created
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done

    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        while True:
            """
                LM-100 스핀들 테스트 리포트 더미 데이터 샘플을 생성하는 래퍼 함수.
                사용자로부터 여러 범위 문자열을 입력받아 처리하고, 결과를 클립보드에 저장합니다.
                """
            logging.info(PK_UNDERLINE)
            logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}LM-100 스핀들 테스트 리포트 더미 데이터 샘플 생성 시작{PK_ANSI_COLOR_MAP['RESET']}")
            logging.info(PK_UNDERLINE)

            # pk_option
            input_multiple_ranges = get_clipboard_text()
            # input_multiple_ranges = ensure_value_completed_2025_11_11(
            #     key_name="input_multiple_ranges",
            #     func_n=get_caller_name(),
            #     guide_text="예: 166-254 170-230\t116-197  175-253",
            #     history_reset=True,
            # )

            if not input_multiple_ranges or not input_multiple_ranges.strip():
                logging.error("입력된 범위 문자열이 없습니다.")
                input("continue:enter")
                continue

            # 스페이스, 탭, 하이픈 등을 구분자로 사용하여 개별 범위 문자열을 분리
            # 예: "166-254 170-230\t116-197-175-253" -> ["166-254", "170-230", "116-197", "175-253"]
            range_strings = re.findall(r'\d+-\d+', input_multiple_ranges)

            if not range_strings:
                logging.error(f"입력된 문자열에서 유효한 범위 패턴을 찾을 수 없습니다: {input_multiple_ranges}")
                input("continue:enter")
                continue

            all_generated_intervals: List[Tuple[int, int]] = []
            for single_range_str in range_strings:
                try:
                    s, e = ensure_LM_100_spindle_test_report_dummy_data_sample_created(
                        input_string=single_range_str,
                        min_interval_len=100,
                        offset=random.randint(a=55, b=84),

                        # ES#8 AG MODE
                        # proper_lower_limit=87,
                        # proper_upper_limit=385,

                        # ES#8 15000 RPM
                        # proper_lower_limit=210,
                        # proper_upper_limit=297,
                        #
                        # # ES#9 AG MODE
                        # proper_lower_limit=116,
                        # proper_upper_limit=254,
                        #
                        # # ES#9 15000 RPM
                        # proper_lower_limit=217,
                        # proper_upper_limit=324,

                        # # PP AG MODE
                        proper_lower_limit=100,
                        proper_upper_limit=389,
                        #
                        # # PP 15000 RPM
                        # proper_lower_limit=206,
                        # proper_upper_limit=310,

                        seed=None,  # seed can be passed if deterministic behavior is needed
                        min_start_gap=12,
                        enable_length_jitter=True
                    )
                    all_generated_intervals.append((s, e))
                except ValueError as ve:
                    logging.error(f"범위 '{single_range_str}' 처리 중 오류 발생: {ve}")
                except Exception as e:
                    logging.error(f"예상치 못한 오류 발생: {e}", exc_info=True)

            if all_generated_intervals:
                parts_out = [f"{s}-{e}" for (s, e) in all_generated_intervals]
                row_text = "\t".join(parts_out)
                ensure_text_saved_to_clipboard(row_text)
                logging.info(f"생성된 모든 범위: {row_text}")
                logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}생성된 더미 데이터가 클립보드에 복사되었습니다.{PK_ANSI_COLOR_MAP['RESET']}")
            else:
                logging.warning("생성된 유효한 범위가 없습니다.")

            logging.info(PK_UNDERLINE)
            logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}LM-100 스핀들 테스트 리포트 더미 데이터 샘플 생성 완료{PK_ANSI_COLOR_MAP['RESET']}")
            logging.info(PK_UNDERLINE)
            input("continue:enter")

    except Exception as exception:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, D_PK_ROOT=D_PK_ROOT)
