from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_windows_os_env_var(windows_env_var_expression: str):
    try:
        import logging
        from os import environ
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

        if windows_env_var_expression.startswith('%') and windows_env_var_expression.endswith('%'):
            windows_env_var = environ.get(windows_env_var_expression)
        else:
            logging.warning(f'{windows_env_var_expression} is not a valid windows environment variable')
            logging.warning(f'this expression needs to be formatted like "%{windows_env_var_expression}%"')
            return None
        if windows_env_var is None:
            logging.warning(f'{windows_env_var_expression} is not registered as a windows environment variable')
            return None
        return windows_env_var
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
