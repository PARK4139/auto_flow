def get_list_without_none(working_list):
    if working_list is not None:
        return [x for x in working_list if x is not None]
    return None
