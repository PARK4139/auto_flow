def remove_special_characters(text):
    import re
    # pattern=r"[^\w\s]" #  \s(whitespace characters=[" ", "\t", "\n", ".", "\n", "_" ])      # space=" " #공백
    # pattern=r"[^\w.,]" # \w(알파벳, 숫자, 밑줄 문자)와 "." 그리고 ","를 제외한 모든문자를 선택, \t, \n, _ 도 삭제되는 설정
    pattern = r"[~!@#$%^&*()_+|<>?:{}]"
    return re.sub(pattern, "", text)
