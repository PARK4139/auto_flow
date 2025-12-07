def get_list_contained_element_that_added_prefix_suffix(working_list, prefix="", suffix=""):
    modified_list = []
    for item in working_list:
        item_added_prefix_and_suffix = f"{prefix}{item}{suffix}"
        modified_list.append(item_added_prefix_and_suffix)
    return modified_list
