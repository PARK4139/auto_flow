def ensure_iterable_data_printed(iterable_data, iterable_data_n=None):
    # todo : dict 일때 key 는 나오는데 value 안나옴. value 나오도록 업그레이드
    import inspect
    import logging
    import os
    from textwrap import dedent
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

    if iterable_data_n is None:
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)
        try:
            call_line = outer_frames[1].code_context[0]
            var_n = call_line.split('(')[1].split(',')[0].strip()
            iterable_data_n = var_n.replace(')', '')
        except Exception as e:
            iterable_data_n = 'Undefined'  # 실패 시 기본값
        finally:
            del frame

    if isinstance(iterable_data, list):
        STAMP_DATA_TYPE = "[ LIST ]"
        open_bracket, kill_bracket = '[', ']'
    elif isinstance(iterable_data, set):
        STAMP_DATA_TYPE = "[ SET ]"
        open_bracket, kill_bracket = '{', '}'
    elif isinstance(iterable_data, dict):
        STAMP_DATA_TYPE = "[ DICT ]"
        open_bracket, kill_bracket = '{', '}'
    elif isinstance(iterable_data, tuple):
        STAMP_DATA_TYPE = "[ TUPLE ]"
        open_bracket, kill_bracket = '(', ')'
    else:
        STAMP_DATA_TYPE = "[ LIST ]"  # 기본값 설정
        open_bracket, kill_bracket = '[', ']'

    terminal_width = 80  # Default for safety
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        pass  # Not a TTY, use default

    # Calculate a suitable width for item_str
    prefix_len = 0
    if hasattr(iterable_data, '__len__'):
        if len(iterable_data) > 0:
            # Calculate the length of the string representation of the last index
            last_idx_str_len = len(str(len(iterable_data) - 1))
            prefix_len = last_idx_str_len + len("[]=")  # e.g., for index 9, "[9]=" has length 4
        else:
            prefix_len = len("[0]=")  # For an empty iterable, it might still print "[0]=" for example.
    else:  # If not iterable with len (e.g., generator), assume a reasonable max index length
        prefix_len = len("[999]=")  # Max 3 digits for idx for safety if len is unknown
    dynamic_width = max(10, terminal_width - prefix_len - 5)

    iterable_data_type_parsed = STAMP_DATA_TYPE
    iterable_data_type_parsed = iterable_data_type_parsed.replace(' ', '')
    iterable_data_type_parsed = iterable_data_type_parsed.replace('[', '')
    iterable_data_type = iterable_data_type_parsed.replace(']', '')

    string_to_print = dedent(f"""
        {PK_UNDERLINE}
        # {iterable_data_n} #iterable_data_name
        iterable_data_type_length={len(iterable_data)}
        iterable_data_type={iterable_data_type}
    """)
    for idx, item in enumerate(iterable_data):
        item_str = str(item).replace("\n", "")
        string_to_print += f'''[{idx}]={item_str:<{dynamic_width}}\n'''
    logging.debug(f"\n{string_to_print}")
