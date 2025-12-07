def ensure_iterable_log_as_vertical(item_iterable, item_iterable_n=None):
    import inspect
    import logging

    if item_iterable_n is None:
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)
        try:
            call_line = outer_frames[1].code_context[0]
            var_n = call_line.split('(')[1].split(',')[0].strip()
            item_iterable_n = var_n.replace(')', '')
        except Exception:
            item_iterable_n = 'Undefined'  # 실패 시 기본값
        finally:
            del frame

    if isinstance(item_iterable, list):
        STAMP_DATA_TYPE = "[ LIST ]"
        open_bracket, kill_bracket = '[', ']'
    elif isinstance(item_iterable, set):
        STAMP_DATA_TYPE = "[ SET ]"
        open_bracket, kill_bracket = '{', '}'
    elif isinstance(item_iterable, dict):
        STAMP_DATA_TYPE = "[ DICT ]"
        open_bracket, kill_bracket = '{', '}'
    elif isinstance(item_iterable, tuple):
        STAMP_DATA_TYPE = "[ TUPLE ]"
        open_bracket, kill_bracket = '(', ')'
    else:
        STAMP_DATA_TYPE = "[ LIST ]"  # 기본값 설정
        open_bracket, kill_bracket = '[', ']'

    # todo : dict 일때 key 는 나오는데 value 안나옴. value 나오도록 업그레이드
    # logging.debug(f'''item_iterable={item_iterable}''')
    logging.debug(f'''len(item_iterable)={len(item_iterable)}''')
    logging.debug(f'''item_iterable_n={item_iterable_n}''')
    logging.debug(f'''STAMP_DATA_TYPE={STAMP_DATA_TYPE}''')
    for idx, item in enumerate(item_iterable):
        item_str = str(item).replace("\n", "")
        logging.debug(f'''[{idx}]={item_str:200}''')
