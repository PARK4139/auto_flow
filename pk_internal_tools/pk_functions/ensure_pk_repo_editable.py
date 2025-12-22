from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_files import F_PYCHARM_EXE  # New import


@ensure_seconds_measured
def ensure_pk_repo_editable(__file__, repo_to_edit):
    import logging
    import traceback
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    try:
        pycharm_executable = F_PYCHARM_EXE  # Use predefined path
        # No need to check if not pycharm_executable here, as it's a hardcoded path.
        # If the file doesn't exist, CreateProcess will raise FileNotFoundError,
        # which will be caught by the outer try-except.

        # cmd argument is now a list for shell=False execution
        if pycharm_executable: # Check if PyCharm executable path was found
            cmd_args = [str(pycharm_executable), str(repo_to_edit)]  # Ensure paths are strings
            ensure_command_executed(cmd=cmd_args, mode="async")  # Pass as list
        else:
            logging.warning("PyCharm 실행 파일을 찾을 수 없어 명령을 실행할 수 없습니다.")
    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
