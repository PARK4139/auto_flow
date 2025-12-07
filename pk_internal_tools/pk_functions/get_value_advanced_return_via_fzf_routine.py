from pk_internal_tools.pk_functions.get_value_from_fzf_routine import get_value_from_fzf_routine


def get_value_advanced_return_via_fzf_routine(file_id, editable, options=[], guide_text=None):
    import logging

    from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
    from pk_internal_tools.pk_functions.get_list_calculated import get_list_calculated
    from pk_internal_tools.pk_functions.get_values_from_historical_file import get_values_from_history_file
    from pk_internal_tools.pk_functions.set_values_to_historical_file import set_values_to_historical_file
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    if options == [""]:
        options = []
    # first call 에서 options에 값을 넣고, 이후 호출부터는 init_options = [] 로 해야함, 계속 값이 더해짐
    f_historical = get_history_file_path(file_id=file_id)
    historical_values = get_values_from_history_file(f_historical=f_historical)
    options = get_list_calculated(origin_list=options, plus_list=historical_values)
    logging.debug(f'''options={options} ''')
    options = get_list_calculated(origin_list=options, dedup=True)

    # prompt_label = get_prompt_label(file_id)
    # prompt_label_guide_text = get_prompt_label_guide_text(prompt_label)
    # easy_speakable_prompt_label = get_easy_speakable_text(prompt_label_guide_text)
    # ensure_spoken(easy_speakable_prompt_label, verbose=False)

    selected = get_value_from_fzf_routine(file_id=file_id, options=options, editable=editable, guide_text=guide_text)

    logging.debug(f'''selected={selected} ''')
    selected = selected.strip()
    options = get_list_calculated(origin_list=[selected], plus_list=options)  # 선택값을 맨 앞으로 정렬
    options = get_list_calculated(origin_list=options, dedup=True)
    set_values_to_historical_file(f_historical=f_historical, values=options)
    return selected
