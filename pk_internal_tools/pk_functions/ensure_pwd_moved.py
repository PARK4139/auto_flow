from pathlib import Path
from typing import Union

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pwd_moved(d_destination: Union[str, Path] = None) -> bool:
    """
    현재 작업 디렉토리를 지정된 디렉토리로 이동합니다.

    Args:
        d_destination: 이동할 디렉토리 경로 (str 또는 Path)
    
    Returns:
        bool: 이동 성공 여부
    """
    import logging
    import os
    from pathlib import Path

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    func_n = get_caller_name()

    current_dir = os.getcwd()
    if d_destination is None:
        d_destination_candidates = get_pnxs_from_d_working(d_working=current_dir)
        # Path 객체를 문자열로 변환
        d_destination_candidates_str = [str(path) for path in d_destination_candidates]
        d_destination = ensure_value_completed(key_name='d_destination', func_n=func_n, options=d_destination_candidates_str)
    destination = Path(d_destination)

    if not destination.exists():
        logging.debug(f"⚠️ 대상 디렉토리를 찾을 수 없습니다: {destination}")
        logging.debug(f"⚠️ 현재 디렉토리: {current_dir}")
        return False

    if not destination.is_dir():
        logging.debug(f"⚠️ 대상 경로가 디렉토리가 아닙니다: {destination}")
        return False

    try:
        os.chdir(destination)
        logging.debug(f"✅ 디렉토리로 이동 완료: {os.getcwd()}")
        return True
    except Exception as e:
        logging.error(f"디렉토리 이동 실패: {e}")
        return False
