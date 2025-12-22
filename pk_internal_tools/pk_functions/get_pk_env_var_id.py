def get_pk_env_var_id(key_name, func_n):
    key_name = key_name.upper()
    if func_n is None:
        return f"{key_name}".replace(" ", "_")
    else:
        func_n = func_n.upper()
        return f"{key_name}_{func_n}".replace(" ", "_")
        # return f"{key_name}_{get_hash(text=key_name)}".replace(" ", "_")
