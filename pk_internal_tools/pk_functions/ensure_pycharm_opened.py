from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pycharm_opened():
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_objects.pk_files import f_pycharm64_exe

    ensure_command_executed(cmd=f'start "" {get_text_chain(f_pycharm64_exe, d_pk_root)}', mode='a')
