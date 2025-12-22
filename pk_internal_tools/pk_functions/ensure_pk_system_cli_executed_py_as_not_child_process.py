from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_system_cli_executed_py_as_not_child_process():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_files import F_UV_ACTIVATE_BAT, F_PK_ENSURE_pk_STARTED_PY, \
        F_UV_PYTHON_EXE

    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT

    return ensure_command_executed(
        rf'start "" cmd /c "cd /d "{D_PK_ROOT}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{F_PK_ENSURE_pk_STARTED_PY}"',
        mode='a')
