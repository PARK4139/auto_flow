

def is_containing_special_characters(text: str, ignore_list: [str] = None):
    import re
    pattern = "[~!@#$%^&*()_+|<>?:{}]"  # , 는 제외인가?
    if ignore_list is not None:
        for exception in ignore_list:
            pattern = pattern.replace(exception, "")
    if re.search(pattern, text):
        return 1
