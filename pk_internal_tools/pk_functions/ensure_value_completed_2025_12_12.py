from typing import Optional

from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme
from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureValueCompleted


# @ensure_seconds_measured
def ensure_value_completed_2025_12_12(key_name, func_n, editable=False, options=None, guide_text=None, history_reset=False, sort_order: Optional[PkModesForEnsureValueCompleted] = PkModesForEnsureValueCompleted.HISTORY, fzf_theme: PkFzfTheme = PkFzfTheme(), history_mode: bool = True):
    import logging
    import os
    import traceback

    from pk_internal_tools.pk_functions.get_value_from_fzf_routine import get_value_from_fzf_routine
    from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureValueCompleted

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
                logging.debug(f'f_historical={f_historical}')
            except IOError as e:
                logging.error(f"Failed to reset history file {f_historical}")
                traceback.print_exc()

    historical_options = get_values_from_history_file(f_historical=f_historical)
    options_from_arg = options
    merged_options = get_list_calculated(origin_list=options_from_arg, plus_list=historical_options)
    merged_options = get_list_calculated(origin_list=merged_options, dedup=True)
    logging.debug(f'len(historical_options)={len(historical_options)}')
    logging.debug(f'file_id={file_id}')
    logging.debug(f'len(merged_options)={len(merged_options)}')

    # --- Apply Sorting Logic ---
    if sort_order == PkModesForEnsureValueCompleted.ASCENDING:
        merged_options.sort()
        logging.debug(f"Applied ascending sort order to options.")
    elif sort_order == PkModesForEnsureValueCompleted.DESCENDING:
        merged_options.sort(reverse=True)
        logging.debug(f"Applied descending sort order to options.")
    elif sort_order == PkModesForEnsureValueCompleted.HISTORY:
        # History sorting is handled by placing last_selected at the top
        logging.debug("Applying HISTORY sort order (last selected at top).")
        pass
    else:
        logging.warning(f"Unknown sort_order: {sort_order}. Defaulting to HISTORY sorting.")
        # History sorting is handled by placing last_selected at the top
        pass

    last_selected = get_last_selected(f_historical)
    logging.debug(f'''last_selected='{last_selected}' {'''%%%FOO%%% ''' if QC_MODE else ''}''')

    if last_selected.strip() != "" and sort_order == PkModesForEnsureValueCompleted.HISTORY:
        logging.debug("Prioritizing last selected item.")
        merged_options = get_list_calculated(origin_list=[last_selected], plus_list=merged_options)
        merged_options = get_list_calculated(origin_list=merged_options, dedup=True)  # 중복 제거 로직 추가

    hashed_options = get_hashed_items(merged_options)
    logging.debug(f"Passing {len(hashed_options)} hashed options to fzf.")

    numbered_selected = get_value_from_fzf_routine(
        file_id=file_id,
        options=hashed_options,
        editable=editable,
        query=last_selected,
        guide_text=guide_text,
        fzf_theme=fzf_theme,
    )
    logging.debug(f'numbered_selected={numbered_selected}')
    logging.debug(f'type(numbered_selected)={type(numbered_selected)}')

    selected_option_removed_hash_bracket = get_str_removed_bracket_hashed_prefix(numbered_selected)
    selected_option_removed_hash_bracket = selected_option_removed_hash_bracket.strip()
    logging.debug(f'selected_option_removed_hash_bracket={selected_option_removed_hash_bracket}')
    if selected_option_removed_hash_bracket and history_mode:
        merged_options = get_list_calculated(origin_list=[selected_option_removed_hash_bracket], plus_list=merged_options)
    merged_options = get_list_calculated(origin_list=merged_options, dedup=True)
    logging.debug(f'''len(merged_options)={len(merged_options)} {'''%%%FOO%%% ''' if QC_MODE else ''}''')
    if history_mode:
        set_values_to_historical_file(f_historical=f_historical, values=merged_options)
    return selected_option_removed_hash_bracket
