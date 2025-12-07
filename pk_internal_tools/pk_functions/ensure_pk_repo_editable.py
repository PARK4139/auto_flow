from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_repo_editable(__file__, repo_to_edit):
    import logging
    import traceback
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_objects.pk_directories import D_PK_MEMO_REPO
    from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_directories import D_AUTO_FLOW_REPO, d_pk_root

    try:
        ensure_command_executed(cmd=f'start "{get_window_title_temp_identified(__file__)}" pycharm "{repo_to_edit}"')
    except:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
