

def get_list_removed_none(items):
    if items is not None:
        return [x for x in items if x is not None]
    return None


