

def get_str_replaced_from_pattern_to_patternless(text_working, pattern):
    import re
    return re.sub(pattern, "", text_working)
