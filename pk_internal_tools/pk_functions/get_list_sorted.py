from typing import List


def get_list_sorted(origins: List, mode_asc: bool = True):
    # TODO : working_list 의 요소가 Path 일 수 있어서, str() 처리 필요.
    if mode_asc:
        return sorted(origins)  # 오름차순 정렬
    elif not mode_asc:
        return sorted(origins, reverse=True)  # 내림차순 정렬
    else:
        raise ValueError("Invalid order. Use 'asc' or 'desc'.")
