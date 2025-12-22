from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_venv_python_executed(pk_path: Path = None) -> None:
    import os
    import sys

    from pk_internal_tools.pk_functions.get_venv_python_path import get_venv_python_path
    venv_python = get_venv_python_path(pk_path)

    if venv_python != sys.executable and os.path.exists(venv_python):
        print(f"virtual environment Python으로 재실행: {venv_python}")
        try:
            os.execv(venv_python, [venv_python] + sys.argv)
        except OSError:
            # execv 실패 시 (Windows 등) 경고만 출력
            print(f"경고: virtual environment Python으로 재실행할 수 없습니다. 시스템 Python을 사용합니다.")
