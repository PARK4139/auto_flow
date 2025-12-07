from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_python_file_executed_in_uv_venv_windows(python_file):
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE, F_UV_ACTIVATE_BAT

    # return ensure_command_executed(rf'start "" cmd /c "cd /d "{d_pk_system}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{python_file}"', mode='a')
    return ensure_command_executed(rf'start "" cmd /D /K "cd /d "{d_pk_root}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{python_file}"', mode='a')
