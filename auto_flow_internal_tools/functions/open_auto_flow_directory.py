import sys
from pathlib import Path
import traceback
import os
import platform
import subprocess

# Add project root to sys.path to resolve ModuleNotFoundError
try:
    project_root_path_for_import = Path(__file__).resolve().parents[2]
    if str(project_root_path_for_import) not in sys.path:
        sys.path.insert(0, str(project_root_path_for_import))
except IndexError:
    # Fallback for when the script is not deep enough
    print("Error: Could not determine project root. Please check script location.")
    sys.exit(1)

from auto_flow_internal_tools.functions.get_auto_flow_path import get_auto_flow_path
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
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
            subprocess.run(['explorer', str(project_root)], check=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", str(project_root)])
        else:  # Linux
            subprocess.run(["xdg-open", str(project_root)])
        
        ensure_slept(milliseconds=2000)  # 파일 탐색기가 열릴 때까지 충분히 대기
        return True
        
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return False