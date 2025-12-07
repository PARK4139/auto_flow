def is_only_eng(text):
    import re
    pattern = "^[a-zA-Z]+$"
    if re.search(pattern, text):
        return 1
    else:
        return 0
