from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_history_file_path(file_id):
    import logging
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    history_file = D_PK_ROOT_HIDDEN / "pk_history" / f"{file_id}.history"
    logging.debug(f'''history_file={history_file} ''')
    ensure_pnx_made(pnx=history_file, mode="f")
    return history_file
