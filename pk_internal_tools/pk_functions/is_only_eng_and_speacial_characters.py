def is_only_eng_and_speacial_characters(text):
    import re
    pattern = "^[a-zA-Z~!@#$%^&*()_+|<>?:{}]+$"
    if re.search(pattern, text):
        return 1
    else:
        return 0
