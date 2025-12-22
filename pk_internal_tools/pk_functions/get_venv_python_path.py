import platform
import sys
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_venv_python_path(pk_path: Path = None) -> str:
    if pk_path is None:
        # 현재 파일에서 pk_system 루트 경로 자동 감지
        current_file = Path(__file__)
        pk_path = current_file.parent.parent.parent

    if platform.system().lower() == "windows":
        venv_python = pk_path / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = pk_path / ".venv" / "bin" / "python3"

    if venv_python.exists():
        return str(venv_python)
    else:
        # virtual environment 이 없으면 시스템 Python 사용
        return sys.executable