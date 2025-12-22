import logging
import traceback

# 표준 시작 루틴을 사용하여 경로 및 로깅을 포함한 환경을 올바르게 설정합니다.
# 이렇게 하면 수동 sys.path 조작이 필요 없습니다.
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done
from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done

# 프로젝트의 표준 방식을 사용하여 래퍼를 초기화합니다.
try:
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    
    from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
    
    logging.info("Calling alert_as_gui with standard initialization...")
    alert_as_gui(
        text="이것은 표준 초기화 후 호출된 GUI 알림입니다. '확인'을 누르기 전까지 닫히지 않아야 합니다.",
        title="표준 호출 테스트"
    )
    logging.info("alert_as_gui call completed.")

except Exception as e:
    # 표준 예외 처리 루틴을 사용합니다.
    ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)