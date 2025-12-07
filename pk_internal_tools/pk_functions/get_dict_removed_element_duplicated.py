

def get_dict_removed_element_duplicated(item_dict):
    seen_values = set()
    unique_dict = {}
    for key, value in item_dict.items():
        if value not in seen_values:
            unique_dict[key] = value
            seen_values.add(value)
    return unique_dict
