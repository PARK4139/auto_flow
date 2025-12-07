def get_added_f_list(previous_state, current_state):
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    return DataStructureUtil.get_elements_that_list1_only_have(list1=current_state, list2=previous_state)
