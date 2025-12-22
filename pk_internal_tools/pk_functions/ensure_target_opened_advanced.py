import logging
from pathlib import Path


def ensure_target_opened_advanced(target_path):
    from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
    from pk_internal_tools.pk_functions.ensure_url_opened import ensure_url_opened
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext

    ensure_pk_system_log_initialized(__file__)


    if not isinstance(target_path, str) or not target_path:
        logging.error("유효하지 않은 타겟 경로가 입력되었습니다.")
        return

    # URL Check
    if target_path.startswith('http://') or target_path.startswith('https://'):
        logging.debug(f"타겟 '{target_path}'는 URL로 분류되었습니다. 'ensure_url_opened'로 엽니다.")
        ensure_url_opened(target_path)
        return

    # File/Directory Check
    p = Path(target_path)
    if p.exists():
        if p.is_dir():
            classification = "디렉토리"
        else:
            classification = "파일"

        logging.debug(f"타겟 '{target_path}'는 {classification}(으)로 분류되었습니다. 'ensure_pnx_opened_by_ext'로 엽니다.")
        ensure_pnx_opened_by_ext(target_path)
    else:
        logging.error(f"타겟 '{target_path}'는 존재하지 않는 파일 또는 디렉토리입니다.")
