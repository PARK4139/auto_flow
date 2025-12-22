from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_flow_executed_py_as_not_child_process():
    import logging

    from pk_internal_tools.pk_objects.pk_directories import D_PK_WRAPPERS
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_files import F_UV_ACTIVATE_BAT, F_UV_PYTHON_EXE

    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    target_file = Path(D_PK_WRAPPERS) / "pk_ensure_pk_flow_executed.py"
    if target_file.exists():
        cmd = rf'start "" cmd /c "cd /d "{D_PK_ROOT}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{target_file}"'
        logging.debug(rf'cmd={cmd}')
        return ensure_command_executed(cmd,
                                      mode='a')




