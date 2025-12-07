from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_venv_python_path_from_files() -> str:
    import platform

    from pk_internal_tools.pk_functions.get_venv_python_path import get_venv_python_path
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE

    try:

        if platform.system().lower() == "windows":
            if F_UV_PYTHON_EXE.exists():
                return str(F_UV_PYTHON_EXE)
        else:
            if F_UV_PYTHON_EXE.exists():
                return str(F_UV_PYTHON_EXE)

        # files.py 경로가 없으면 기본 방식 사용
        return get_venv_python_path()

    except ImportError:
        # files.py import 실패 시 기본 방식 사용
        return get_venv_python_path()
