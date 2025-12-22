from typing import List, Optional
from pk_internal_tools.pk_functions.get_value_from_fzf_routine import get_value_from_fzf_routine


def ensure_value_completed_2025_10_13_0000(key_name, func_n, editable=False, options=None, guide_text=None, history_reset=False, multi_select=False, custom_fzf_options: Optional[List[str]] = None):
    import logging
    import os

    from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_last_selected import get_last_selected
    from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
    from pk_internal_tools.pk_functions.get_numbered_items import get_numbered_items
    from pk_internal_tools.pk_functions.get_str_removed_from_numbered_str import get_str_removed_from_numbered_str
    from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_history_file
    from pk_internal_tools.pk_functions.set_values_to_historical_file import set_values_to_historical_file
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    file_id = get_file_id(key_name, func_n)

    options = options or []
    if options == [""]:
        options = []

    f_historical = get_history_file_path(file_id=file_id)

    if history_reset:
        if os.path.exists(f_historical):
            try:
                with open(f_historical, 'w', encoding='utf-8') as f:
                    f.write('')
                logging.info(f"History file has been reset: {f_historical}")
            except IOError as e:
                logging.error(f"Failed to reset history file {f_historical}: {e}")

    historical_values = get_values_from_history_file(f_historical=f_historical)
    options = get_list_calculated(origin_list=options, plus_list=historical_values)
    logging.debug(f'''file_id={file_id} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    options = get_list_calculated(origin_list=options, dedup=True)

    last_selected = get_last_selected(f_historical)
    logging.debug(f'''last_selected={last_selected} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    if last_selected.strip() != "":
        options = get_list_calculated(origin_list=[last_selected], plus_list=options)
        options = get_list_calculated(origin_list=options, dedup=True)

    numbered_options = get_numbered_items(options)
    numbered_selected = get_value_from_fzf_routine(
        file_id=file_id,
        options=numbered_options,
        editable=editable,
        query=last_selected,
        guide_text=guide_text,
        multi_select=multi_select,
        custom_fzf_options=custom_fzf_options # Pass the custom options
    )

    if editable or multi_select: # If multi_select, fzf returns raw input, no numbering to remove
        selected = numbered_selected
    else:
        selected = get_str_removed_from_numbered_str(numbered_selected)
    
    selected = selected.strip() if isinstance(selected, str) else [s.strip() for s in selected]

    if selected:
        if isinstance(selected, str):
            options = get_list_calculated(origin_list=[selected], plus_list=options)
        else: # multi_select case
            options = get_list_calculated(origin_list=selected, plus_list=options)
    options = get_list_calculated(origin_list=options, dedup=True)
    logging.debug(f'''len(options)={len(options)} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    set_values_to_historical_file(f_historical=f_historical, values=options)
    return selected
