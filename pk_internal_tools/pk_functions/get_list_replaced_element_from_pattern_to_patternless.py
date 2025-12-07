






def get_list_replaced_element_from_pattern_to_patternless(working_list, pattern):
    import re
    return [re.sub(pattern, "", item) for item in working_list]
