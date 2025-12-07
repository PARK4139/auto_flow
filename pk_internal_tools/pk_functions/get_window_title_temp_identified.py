def get_window_title_temp_identified(__file__):
    from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
    from pk_internal_tools.pk_functions.get_hash import get_hash
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_sanitized_file_path import get_sanitized_file_path
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    path_sanitized = get_sanitized_file_path(__file__)
    hash = get_hash(get_nx(path_sanitized))
    if QC_MODE:
        print(f'__file__={__file__}')
        print(f'path_sanitized={path_sanitized}')
        print(f'hash={hash}')
    # ensure_console_paused()
    return rf"{get_window_title_temp()} {hash}"
