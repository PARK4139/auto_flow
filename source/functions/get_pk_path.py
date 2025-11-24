import sys
import traceback
from pathlib import Path

from pk_system.pk_system_sources.pk_system_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_system_sources.pk_system_objects.pk_system_directories import get_pk_system_root


def get_pk_path():
    """
    pk_system의 루트 경로를 반환합니다.
    pk_system 기능을 활용하여 구현했습니다.
    
    Returns:
        Path: pk_system 루트 디렉토리 경로
    """
    try:
        pk_path = get_pk_system_root()
        return pk_path
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return None


if __name__ == "__main__":
    pk_path = get_pk_path()
    if pk_path:
        print(f"pk_system 경로: {pk_path}")
    else:
        print("오류: pk_system 경로를 찾을 수 없습니다.")