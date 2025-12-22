

def get_list_replaced_element_from_str_to_upper_case(working_list):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if not isinstance(working_list, list):
        raise ValueError("Input must be a list.")
    return [item.upper() if isinstance(item, str) else item for item in working_list]
