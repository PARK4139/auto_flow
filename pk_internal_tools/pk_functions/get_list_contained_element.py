def get_list_contained_element(working_list, prefix=None, suffix=None):
    modified_list = []
    for item in working_list:
        if prefix and suffix:
            if item.startswith(prefix) and item.endswith(suffix):
                modified_list.append(item)
        if prefix:
            if item.startswith(prefix):
                modified_list.append(item)
        if suffix:
            if item.endswith(suffix):
                modified_list.append(item)
    return modified_list
