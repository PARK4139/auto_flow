def get_f_n_moved_pattern_to_front(pattern, item_pnx):
    import re
    match = re.search(pattern=pattern, string=item_pnx)
    n = get_n(item_pnx)
    p = get_p(item_pnx)
    x = get_x(item_pnx)
    if match:
        pattern = match.group(1)
        item_pnx_new = rf"{p}\{pattern}_{n.replace(pattern, '')}{x}"
        return item_pnx_new
    else:
        # 패턴이 없으면 원래 f명 반환
        return item_pnx
