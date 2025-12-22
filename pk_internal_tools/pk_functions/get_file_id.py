def get_file_id(key_name: str, func_n):
    import logging
    from pk_internal_tools.pk_functions.get_hash import get_hash
    if func_n is None:
        func_n = get_hash(text=key_name)
    file_id = f"{key_name}_via_{func_n}"
    logging.debug(f"key_name={key_name}")
    logging.debug(f"func_n={func_n}")
    logging.debug(f"file_id={file_id}")
    return file_id
