def ensure_cmd_exe_deduplicated_once():
    # TODO : 로직검증필요

    import logging
    from pathlib import Path

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_functions.ensure_process_deduplicated import ensure_process_deduplicated
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.get_values_sanitize_for_cp949 import get_values_sanitize_for_cp949
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    values = get_windows_opened_with_hwnd()
    values = [get_values_sanitize_for_cp949(v) for v in values]

    key_name = "window_opened"
    selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=values, editable=False)
    window_opened = selected

    while True:
        window_opened = Path(window_opened)
        logging.debug(f'''window_opened={window_opened} ''')
        ensure_process_deduplicated(window_title_seg=window_opened)
        # ensure_slept(milliseconds=1000)
        ensure_slept(milliseconds=200)
