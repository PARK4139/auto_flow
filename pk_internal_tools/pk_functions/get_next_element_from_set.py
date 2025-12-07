import logging


def get_next_element_from_set(item_set):
    """
    ipdb 와 함께 디버깅용으로 편함.
    """

    # 반복자 생성
    if not hasattr(get_next_element_from_set, "iterator"):
        get_next_element_from_set.iterator = iter(item_set)

    try:
        # 다음 요소 반환
        return next(get_next_element_from_set.iterator)
    except StopIteration:
        # 끝에 도달했을 때 메시지 출력
        logging.debug("다 돌았습니다")
        # 반복자를 새로 생성
        get_next_element_from_set.iterator = iter(item_set)
        return next(get_next_element_from_set.iterator)
