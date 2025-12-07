from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def save_to_history(contents_to_save: str, history_file):
    import os

    import logging
    logging.debug(f'''contents_to_save={contents_to_save} ''')
    logging.debug(f'''history_file={history_file} ''')
    if os.path.exists(history_file):
        with open(history_file, "w", encoding="utf-8") as f_obj:
            f_obj.write(str(contents_to_save).strip())
