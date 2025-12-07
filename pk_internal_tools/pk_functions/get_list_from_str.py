

def get_list_from_str(item_str, delimiter='\n'):
    if not isinstance(item_str, str):
        raise ValueError("입력은 문자열이어야 합니다.")

    return [item for item in item_str.split(delimiter)]
