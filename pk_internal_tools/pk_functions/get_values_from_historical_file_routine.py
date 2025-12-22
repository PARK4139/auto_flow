def get_values_from_historical_file_routine(file_id: str, key_hint: str, options=[], editable=False) -> str:
    
    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
    import logging
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.set_values_to_historical_file import set_values_to_historical_file
    from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_history_file
    history_file = get_history_file_path(file_id=file_id)
    if QC_MODE:
        logging.debug(f'''history_file={history_file} ''')
    if not history_file.exists():
        ensure_pnx_made(pnx=history_file, mode='f')
    if editable:
        if not is_window_opened(window_title_seg=str(history_file)):
            ensure_pnx_opened_by_ext(pnx=history_file)
            ensure_window_to_front(get_nx(history_file))
    options = get_list_calculated(origin_list=options, plus_list=get_values_from_history_file(f_historical=history_file))
    selected = ensure_value_completed(key_name=key_hint, options=options)
    options = get_list_calculated(origin_list=[selected], plus_list=options)
    set_values_to_historical_file(f_historical=history_file, values=options)
    return selected
