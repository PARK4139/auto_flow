from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_python_file_executed_advanced(file_path, not_child_process_mode=True):
    import logging

    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_files import F_UV_ACTIVATE_BAT, F_UV_PYTHON_EXE

    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    target_file = Path(file_path)
    if target_file.exists():
        if not_child_process_mode == True:
            cmd = rf'start "" cmd /D /K "cd /d "{D_PK_ROOT}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{target_file}"'
            logging.debug(rf'cmd={cmd}')
            return ensure_command_executed(cmd, mode='a')
        else:
            ensure_not_prepared_yet_guided()
