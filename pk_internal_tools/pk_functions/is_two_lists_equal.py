

def is_two_lists_equal(list1, list2):
    """
    두 리스트의 요소들이 동일한지 확인
    """
    if len(list1) != len(list2):
        return 0
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return 0
    return 1
