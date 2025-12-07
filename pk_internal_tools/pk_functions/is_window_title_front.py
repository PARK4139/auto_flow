# @ensure_seconds_measured
def is_window_title_front(window_title, verbose=False):
    import logging

    from pk_internal_tools.pk_functions.get_front_window_title import get_front_window_title
    front_window_title = get_front_window_title()
    if not front_window_title is None:
        # pk_* -> 비교결과
        if verbose:
            compare_result = "같다" if len(window_title) == len(front_window_title) else "다르다"
            compare_title = f"'{window_title}' 와 '{front_window_title}' 길이비교결과"
            compare_condition = rf"{len(window_title)}와 {len(front_window_title)}는"
            gap = 1
            logging.debug(f"{compare_title}, {compare_condition} {compare_result}")

        if window_title == front_window_title:
            if not verbose:
                compare_result = "같다" if len(window_title) == len(front_window_title) else "다르다"
                compare_title = f"'{window_title}' 와 '{front_window_title}' 길이비교결과"
                compare_condition = rf"{len(window_title)}와 {len(front_window_title)}는"
                gap = 1
                logging.debug(f"{compare_title}, {compare_condition} {compare_result}")
            return 1
    return 0
