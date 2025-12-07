from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_flow_executed_py_as_not_child_process():
    import logging

    from pk_internal_tools.pk_functions import is_pnx_existing
    from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_files import F_UV_ACTIVATE_BAT, F_UV_PYTHON_EXE

    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    target_file = Path(d_pk_wrappers) / "pk_ensure_pk_flow_executed.py"
    if is_pnx_existing(target_file):
        cmd = rf'start "" cmd /c "cd /d "{d_pk_root}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{target_file}"'
        logging.debug(rf'cmd={cmd}')
        return ensure_command_executed(cmd,
                                      mode='a')




