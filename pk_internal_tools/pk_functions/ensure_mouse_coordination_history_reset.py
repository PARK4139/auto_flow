import logging

from pk_internal_tools.pk_functions.ensure_slept_by_following_history import get_pk_env_var_id
from pk_internal_tools.pk_objects.pk_directories import D_MOUSE_CLICK_COORDINATION_HISTORY


def ensure_mouse_coordination_history_reset(key_name: str, func_n: str) -> bool:
    """
    주어진 key_name과 func_n에 해당하는 마우스 좌표 기록 파일을 삭제합니다.
    """
    file_id = get_pk_env_var_id(key_name, func_n)
    history_dir = D_MOUSE_CLICK_COORDINATION_HISTORY
    history_file = history_dir / f"{file_id}.txt"

    if history_file.exists():
        try:
            history_file.unlink()  # 파일을 삭제합니다.
            logging.debug(f"마우스 좌표 기록 파일이 성공적으로 삭제되었습니다: {history_file}")
            return True
        except Exception as e:
            logging.error(f"마우스 좌표 기록 파일 삭제 중 오류 발생: {e}")
            return False
    else:
        logging.debug(f"마우스 좌표 기록 파일이 존재하지 않습니다: {history_file}")
        return False
