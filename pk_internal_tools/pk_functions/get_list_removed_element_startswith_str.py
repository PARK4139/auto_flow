

def get_list_removed_element_startswith_str(working_list, string):
    if not isinstance(working_list, list):
        raise ValueError("working_list는 리스트여야 합니다.")
    if not isinstance(string, str):
        raise ValueError("string은 문자열이어야 합니다.")

    # 특정 문자열로 시작하지 않는 요소 필터링
    return [item for item in working_list if not item.strip().startswith(string)]
