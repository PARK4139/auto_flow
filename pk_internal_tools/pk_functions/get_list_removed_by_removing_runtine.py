def get_list_removed_by_removing_runtine(working_list):
    from pk_internal_tools.pk_functions.get_list_removed_element_empty import get_list_removed_empty
    from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
    from pk_internal_tools.pk_functions.get_list_replaced_element_from_str_to_str import get_list_replaced_element_from_str_to_str
    from pk_internal_tools.pk_functions.get_list_striped_element import get_list_striped_element
    from pk_internal_tools.pk_functions.get_list_without_none import get_list_without_none
    if working_list is None:
        return None
    working_list = get_list_deduplicated(working_list)
    working_list = get_list_without_none(working_list)
    working_list = get_list_removed_empty(working_list)
    working_list = get_list_replaced_element_from_str_to_str(working_list, "\n", "")
    working_list = get_list_striped_element(working_list)
    return working_list
