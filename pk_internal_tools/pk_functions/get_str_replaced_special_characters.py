def get_str_replaced_special_characters(target: str, replacement: str):  # str to str
    import re

    target_replaced = re.sub(pattern=r'[^a-zA-Z0-9가-힣\s]', repl=replacement,
                             string=target)  # 정규표현식을 사용하여 특수문자(알파벳, 숫자, 한글, 공백을 제외한 모든 문자) remove
    return target_replaced
