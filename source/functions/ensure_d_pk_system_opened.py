import sys
import traceback
import os
import platform
import subprocess
from pathlib import Path

from pk_system.pk_sources.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_system.pk_sources.pk_objects.pk_system_directories import get_pk_system_root
from pk_system.pk_sources.pk_functions.get_caller_name import get_caller_name
from pk_system.pk_sources.pk_functions.ensure_slept import ensure_slept


def ensure_d_pk_system_opened():
    """
    Ensures that the pk_system directory is opened in the file explorer.
    pk_system 기능을 최대한 활용하여 구현했습니다.
    """
    try:
        func_n = get_caller_name()
        d_pk_system = get_pk_system_root()

        if not d_pk_system.exists() or not d_pk_system.is_dir():
            print(f"오류: 디렉토리를 찾을 수 없습니다: {d_pk_system}")
            return False

        print(f"디렉토리 열기: {d_pk_system}")

        system = platform.system()
        if system == "Windows":
            os.startfile(d_pk_system)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(d_pk_system)])
        else:  # Linux
            subprocess.run(["xdg-open", str(d_pk_system)])
        
        ensure_slept(milliseconds=500)  # 파일 탐색기가 열릴 때까지 대기
        return True
        
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return False