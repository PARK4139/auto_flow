import logging

from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_console_log_blocked(text=None):
    """
    콘솔 로그를 차단하고 사용자 입력을 대기하는 함수
    
    주의: 이 함수는 로깅을 비활성화하기 전에 사용자 입력을 대기합니다.
    QC_MODE 모드에서는 이 함수가 호출되지 않도록 하는 것이 좋습니다.
    """
    import sys
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    
    # QC_MODE 모드에서는 로깅을 비활성화하지 않고 단순히 대기만 함
    if QC_MODE:
        if text:
            logging.info(get_text_cyan(text))
        else:
            logging.info(get_text_cyan("pk_system logging is now blocked."))
        # 프로젝트 규칙에 따라 ensure_console_paused 사용
        ensure_console_paused("continue:enter")
        return
    
    # 일반 모드: 기존 동작 유지
    logger = logging.getLogger()
    if text:
        # logger.info(get_text_cyan(text))
        # input("") # 비대화형 환경에서 EOFError를 유발하므로 주석 처리
        ensure_console_paused(get_text_cyan(text))
    else:
        # logger.info(get_text_cyan("pk_system logging is now blocked."))
        ensure_console_paused(get_text_cyan("pk_system logging is now blocked."))
    logger.handlers.clear()
    logging.disable(logging.CRITICAL + 1)



