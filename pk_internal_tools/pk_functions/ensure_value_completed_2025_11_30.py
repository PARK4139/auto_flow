from typing import Optional

from pk_internal_tools.pk_functions.get_value_from_fzf_routine import get_value_from_fzf_routine
from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme
from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForEnsureValueCompleted20251130


# @ensure_seconds_measured
def ensure_value_completed_2025_11_30(key_name, func_n, editable=False, options=None, guide_text=None, history_reset=False, sort_order: Optional[SetupOpsForEnsureValueCompleted20251130] = SetupOpsForEnsureValueCompleted20251130.HISTORY, fzf_theme: PkFzfTheme = PkFzfTheme(), history_mode: bool = True):
    import logging
    import os

    from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_last_selected import get_last_selected
    from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
    from pk_internal_tools.pk_functions.get_hashed_items import get_hashed_items
    from pk_internal_tools.pk_functions.get_str_removed_bracket_hashed_prefix import get_str_removed_bracket_hashed_prefix
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
    logging.debug(f"Loaded {len(historical_values)} historical values.")
    
    options = get_list_calculated(origin_list=options, plus_list=historical_values)
    logging.debug(f"Combined options with history, total: {len(options)}.")

    logging.debug(f'''file_id={file_id} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    options = get_list_calculated(origin_list=options, dedup=True)
    logging.debug(f"Deduplicated options, final count: {len(options)}.")

    # --- Apply Sorting Logic ---
    if sort_order == SetupOpsForEnsureValueCompleted20251130.ASCENDING:
        options.sort()
        logging.debug(f"Applied ascending sort order to options.")
    elif sort_order == SetupOpsForEnsureValueCompleted20251130.DESCENDING:
        options.sort(reverse=True)
        logging.debug(f"Applied descending sort order to options.")
    elif sort_order == SetupOpsForEnsureValueCompleted20251130.HISTORY:
        # History sorting is handled by placing last_selected at the top
        logging.debug("Applying HISTORY sort order (last selected at top).")
        pass
    else:
        logging.warning(f"Unknown sort_order: {sort_order}. Defaulting to HISTORY sorting.")
        # History sorting is handled by placing last_selected at the top
        pass

    last_selected = get_last_selected(f_historical)
    logging.debug(f'''last_selected='{last_selected}' {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    if last_selected.strip() != "" and sort_order == SetupOpsForEnsureValueCompleted20251130.HISTORY:
        logging.debug("Prioritizing last selected item.")
        options = get_list_calculated(origin_list=[last_selected], plus_list=options)
        options = get_list_calculated(origin_list=options, dedup=True)  # 중복 제거 로직 추가

    hashed_options = get_hashed_items(options)
    logging.debug(f"Passing {len(hashed_options)} hashed options to fzf.")

    numbered_selected = get_value_from_fzf_routine(
        file_id=file_id,
        options=hashed_options,
        editable=editable,
        query=last_selected,
        guide_text=guide_text,
        fzf_theme=fzf_theme,
    )
    logging.debug(f"Raw value from fzf: '{numbered_selected}' (type: {type(numbered_selected)}).")

    selected = get_str_removed_bracket_hashed_prefix(numbered_selected)
    selected = selected.strip()
    logging.debug(f'''Final selected value (stripped and unhashed): '{selected}' ''')

    if selected and history_mode:
        options = get_list_calculated(origin_list=[selected], plus_list=options)
    options = get_list_calculated(origin_list=options, dedup=True)
    logging.debug(f'''len(options)={len(options)} {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    if history_mode:
        set_values_to_historical_file(f_historical=f_historical, values=options)
    return selected
