from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
def input(text_working, limit_seconds, return_default, get_input_validated=None):
    return ensure_value_completed(key_name=text_working, options=[return_default] if return_default else [])
