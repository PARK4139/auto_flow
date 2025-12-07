def get_str_from_file(pnx):
    from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
    from pk_internal_tools.pk_functions.get_list_without_none import get_list_without_none
    import logging

    prompt = ""
    lines = get_list_from_f(f=pnx)
    
    # 디버깅 정보
    logging.debug(f"get_str_from_file - pnx={pnx}")
    logging.debug(f"raw_lines={lines}")
    
    if lines is None:
        logging.debug(f"ERROR: lines is None for pnx={pnx}")
        return None
    
    lines = get_list_without_none(working_list=lines)
    logging.debug(f"cleaned_lines={lines}")
    
    if not lines:
        logging.debug(f"WARNING: no lines found in file {pnx}")
        return ""
    
    for line in lines:
        if line is not None:
            prompt = prompt + str(line) + "\n"
    
    logging.debug(f"final_prompt='{prompt}'")
    return prompt
