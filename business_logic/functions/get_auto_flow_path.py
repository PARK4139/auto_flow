def get_auto_flow_path():
    import traceback

    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    try:
        func_n = get_caller_name()
        auto_flow_path = ensure_env_var_completed(
            key_name="auto_flow_path",
            func_n=func_n,
        )
        return auto_flow_path
    except Exception:
        ensure_debug_loged_verbose(traceback)
        return None
