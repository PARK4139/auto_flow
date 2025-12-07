

def get_str_from_list(working_list, item_connector=", ", prefix="", suffix=""):
    # item_connector means delimiter
    if not isinstance(working_list, list):
        raise ValueError("Input must be a list.")

    if not all(isinstance(item, str) for item in working_list):
        raise ValueError("All elements in the list must be strings.")

    return f"{prefix}{item_connector.join(working_list)}{suffix}"
