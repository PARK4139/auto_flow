def get_list_striped_element(working_list, mode='strip'):
    if working_list is None:
        working_list = []
    if mode == 'lstrip':
        return [item.lstrip() for item in working_list]
    elif mode == 'rstrip':
        return [item.rstrip() for item in working_list]
    else:
        return [item.strip() for item in working_list]
