from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_python_file_executed_advanced(file_path, not_child_process_mode=True):
    import logging

    from pk_internal_tools.pk_functions import is_pnx_existing
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_files import F_VENV_ACTIVATE_BAT, F_VENV_PYTHON_EXE

    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    target_file = Path(file_path)
    if is_pnx_existing(target_file):
        if not_child_process_mode == True:
            cmd = rf'start "" cmd /D /K "cd /d "{d_pk_root}" && {F_VENV_ACTIVATE_BAT} && {F_VENV_PYTHON_EXE} "{target_file}"'
            logging.debug(rf'cmd={cmd}')
            return ensure_command_executed(cmd, mode='a')
        else:
            ensure_not_prepared_yet_guided()
