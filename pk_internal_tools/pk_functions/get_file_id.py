

def get_file_id(key_name, func_n):
    import logging
    logging.debug(f"key_name={key_name}")
    logging.debug(f"func_n={func_n}")
    file_id =  f"{key_name}_via_{func_n}"
    logging.debug(f"file_id={file_id}")
    return file_id

