def is_containing_kor(text):
    import re
    pattern = "[ㄱ-ㅎ가-힣]"
    if re.search(pattern, text):
        return 1
    else:
        return 0
