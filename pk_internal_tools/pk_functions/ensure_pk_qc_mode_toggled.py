import json
import logging
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import D_PK_CONFIG
from pk_internal_tools.pk_objects.pk_qc_mode import _get_qc_mode_status, _get_qc_mode_status_file_path, QC_MODE

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_colors import PkColors


def _set_qc_mode_status(status: bool):
    """
    QC 모드 상태를 qc_mode_status.json 파일에 저장합니다.
    Args:
        status (bool): 설정할 QC 모드 상태.
    """
    func_n = get_caller_name()
    qc_mode_file = _get_qc_mode_status_file_path()
    qc_mode_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    try:
        with open(qc_mode_file, 'w', encoding='utf-8') as f:
            json.dump({"qc_mode": status}, f, ensure_ascii=False, indent=4)
        logging.debug(f"{func_n}: QC mode status saved to {qc_mode_file}: {status}")
    except IOError as e:
        logging.error(f"{func_n}: Failed to save QC mode status to {qc_mode_file}: {e}")
        ensure_debugged_verbose(traceback, e)


def ensure_pk_qc_mode_toggled():
    """
    QC 모드 상태를 토글하고, 변경된 상태를 저장하며 로깅 메시지를 출력합니다.
    """
    func_n = get_caller_name()
    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}QC 모드 토글 시작{PkColors.RESET}")

    current_qc_mode = _get_qc_mode_status()  # pk_qc_mode.py에서 현재 QC_MODE 값을 가져옴
    new_qc_mode = not current_qc_mode

    _set_qc_mode_status(new_qc_mode)

    logging.info(f"{func_n}: QC 모드 상태가 {current_qc_mode}에서 {new_qc_mode}로 변경되었습니다.")
    logging.info(f"{PkColors.BRIGHT_CYAN}QC 모드 토글 완료{PkColors.RESET}")
    logging.info(PK_UNDERLINE)


if __name__ == '__main__':
    # 로깅 설정을 위한 임시 코드 (실제 사용 시 래퍼 스크립트에서 설정)
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent.parent))
    from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
    ensure_pk_system_log_initialized(__file__)

    ensure_pk_qc_mode_toggled()