def get_count_none_of_list(list):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # count=sum(element is None for element in list)
    Nones = list
    None_count = Nones.count(None)
    return None_count
