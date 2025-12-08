import sys
import traceback
import os
import platform
import subprocess
from pathlib import Path

from business_logic.functions.get_auto_flow_path import get_auto_flow_path
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def open_auto_flow_directory():
    """
    Ensures that the pk_system directory is opened in the file explorer.
    pk_system 기능을 최대한 활용하여 구현했습니다.
    """
    try:
        func_n = get_caller_name()
        project_root = get_auto_flow_path()

        if not project_root.exists() or not project_root.is_dir():
            print(f"오류: 디렉토리를 찾을 수 없습니다: {project_root}")
            return False

        print(f"디렉토리 열기: {project_root}")

        system = platform.system()
        if system == "Windows":
            os.startfile(project_root)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(project_root)])
        else:  # Linux
            subprocess.run(["xdg-open", str(project_root)])
        
        ensure_slept(milliseconds=500)  # 파일 탐색기가 열릴 때까지 대기
        return True
        
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return False