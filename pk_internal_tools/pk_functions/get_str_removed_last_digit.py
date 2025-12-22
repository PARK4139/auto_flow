def get_str_removed_last_digit(string, debug_mode=True):
    import inspect
    import re
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    return re.sub(r'\d+\s*$', '', string)
