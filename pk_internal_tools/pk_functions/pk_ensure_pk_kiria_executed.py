import logging
import traceback
from typing import Literal

from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_finally_routine_done import ensure_pk_wrapper_finally_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_kiria.pk_kiria import ensure_pk_kiria_executed_single_command, ensure_pk_kiria_executed_continuously
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def pk_ensure_pk_kiria_executed( # 함수명 변경
        run_once: bool = False,
        func_n: str = get_caller_name()
) -> bool:
    """
    PkKiria 음성 비서를 실행하는 핵심 함수.
    
    Args:
        mode (Literal["continuous", "single"]): Kiria 실행 모드 ("continuous" 또는 "single").
                                                기본값은 "continuous"입니다.
        func_n (str): 호출자 함수 이름. 자동으로 결정됩니다.
        
    Returns:
        bool: PkKiria 실행 성공 여부.
    """
    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}PkKiria 실행 시작{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    success = False
    try:
        ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)

        if run_once:
            logging.info("PkKiria를 'single' 모드로 실행합니다.")
            success = ensure_pk_kiria_executed_single_command()
        else: # run_once is False, so continuous mode
            logging.info("PkKiria를 'continuous' 모드로 실행합니다.")
            success = ensure_pk_kiria_executed_continuously()

    except Exception as e:
        logging.error(f"PkKiria 실행 중 예외 발생: {e}", exc_info=True)
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, traceback=traceback)
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}PkKiria 실행 종료 (성공: {success}){PkColors.RESET}")
        logging.info(PK_UNDERLINE)

    return success


if __name__ == '__main__':
    ensure_pk_system_log_initialized(__file__)
    pk_ensure_pk_kiria_executed(run_once=False)