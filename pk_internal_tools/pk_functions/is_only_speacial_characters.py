def is_only_speacial_characters(text):
    import re
    pattern = "^[~!@#$%^&*()_+|<>?:{}]+$"
    if re.search(pattern, text):
        return 1
    else:
        return 0
