def get_list_deduplicated(working_list):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    items_removed_duplication: [str] = []
    for item in working_list:
        if item not in items_removed_duplication:
            # if item is not None:
            items_removed_duplication.append(item)
    working_list = items_removed_duplication
    return working_list
