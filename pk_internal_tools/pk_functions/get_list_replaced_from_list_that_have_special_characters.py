def get_list_replaced_from_list_that_have_special_characters(target: [str],
                                                             replacement: str):  # from [str] to [str] # 문제있어보임.
    import re

    return [re.sub(pattern=r'[^a-zA-Z0-9가-힣\s]', repl='', string=string) for string in target]
