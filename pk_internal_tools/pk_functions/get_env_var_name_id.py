def get_env_var_id(key_name, func_n):
    return f"{key_name.upper()}_{func_n.upper()}".replace(" ", "_")
