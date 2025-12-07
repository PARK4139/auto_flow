def get_list_replaced_element_from_str_to_str(working_list, from_str, to_str, debug_mode=True):
    return [text.replace(from_str, to_str) for text in working_list]
