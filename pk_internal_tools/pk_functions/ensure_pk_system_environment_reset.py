import os
import logging
import traceback

from pk_internal_tools.pk_objects.pk_messages import PK_UNDERLINE, ANSI_COLOR_MAP
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def ensure_pk_system_environment_reset():
    """
    pk_system과 관련된 시스템 환경 변수를 초기화합니다.
    현재는 D_PK_ROOT 환경 변수를 삭제합니다.
    """
    try:
        logging.info(PK_UNDERLINE)
        logging.info(f"{ANSI_COLOR_MAP['BRIGHT_CYAN']}pk_system 환경 변수 초기화 시작{ANSI_COLOR_MAP['RESET']}")
        
        env_var_to_delete = "D_PK_ROOT"
        
        if env_var_to_delete in os.environ:
            del os.environ[env_var_to_delete]
            logging.info(f"환경 변수 '{env_var_to_delete}'를 삭제했습니다.")
        else:
            logging.info(f"환경 변수 '{env_var_to_delete}'가 존재하지 않아 삭제할 필요가 없습니다.")
            
        logging.info(f"{ANSI_COLOR_MAP['BRIGHT_CYAN']}pk_system 환경 변수 초기화 완료{ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)

    except Exception as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        logging.error(f"pk_system 환경 변수 초기화 중 오류 발생: {e}")
