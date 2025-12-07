# @ensure_seconds_measured
def ensure_pk_wrapper_starter_suicided(file_path):
    import logging
    from pathlib import Path
    from pk_internal_tools.pk_functions.ensure_process_killed_by_window_title import ensure_process_killed_by_window_title
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified

    logging.debug(f'''file_path={file_path} ''')

    ensure_process_killed_by_window_title(get_window_title_temp_identified(__file__))
    ensure_process_killed_by_window_title(window_title=get_nx(Path(file_path)))
