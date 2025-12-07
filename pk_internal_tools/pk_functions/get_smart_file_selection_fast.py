from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_smart_file_selection_fast(pk_files, last_selected):
    import logging

    from pk_internal_tools.pk_functions.get_filenames_to_display import get_filenames_to_display
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_value_advanced_fallback_via_input import ensure_value_advanced_fallback_via_input

    """초고속 파일 선택 로직"""
    try:
        display_names = get_filenames_to_display(files=pk_files)

        if last_selected and last_selected in pk_files:
            default_query = get_nx(last_selected)
            logging.debug(f"마지막 선택: {default_query}")

        logging.debug(f"Tab으로 자동완성하여 파일을 선택하세요!")
        logging.debug(f"총 {len(display_names)}개 파일 중에서 선택")

        func_n = get_caller_name()

        key_name = '파일 선택'
        options = display_names
        selected_name = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)

        # selected_name = _ensure_value_completed_2025_10_12_0000_return_core(
        #     message=f"파일 선택",
        #     options=display_names
        # )

        if not selected_name:
            logging.debug(f"선택이 취소되었습니다.")
            return None

        selected_file = next((p for p in pk_files if get_nx(p) == selected_name), None)
        if selected_file:
            logging.debug(f"선택됨: {selected_name}")
            return selected_file
        else:
            logging.debug(f"파일을 찾을 수 없습니다: {selected_name}")
            return None

    except Exception as e:
        logging.debug(f"파일 선택 중 오류: {e}")
        return ensure_value_advanced_fallback_via_input(pk_files, last_selected)
