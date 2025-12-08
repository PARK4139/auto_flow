# @ensure_seconds_measured
def ensure_pk_wrapper_suicided(file_path):
    import logging
    from pk_internal_tools.pk_functions.ensure_process_killed_by_window_title import ensure_process_killed_by_window_title
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pathlib import Path
    logging.debug(f'''file_path={file_path} ''')
    ensure_process_killed_by_window_title(window_title=get_nx(Path(file_path)))
