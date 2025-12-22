def get_txt_highlighted(txt_whole, config_highlight_dict):
    import re

    from pk_internal_tools.pk_objects.pk_colors import PkColors

    reset_code = PkColors.RESET
    # 색칠할 영역 추출 (위치 정보 포함)
    highlight_spans = []
    for color, keywords in config_highlight_dict.items():
        color_code = PkColors.get(color, PkColors.GREY)
        for kw in keywords:
            for match in re.finditer(re.escape(kw), txt_whole):
                start, end = match.span()
                highlight_spans.append((start, end, color_code))
    # 겹치는 영역 remove: 앞쪽 우선, 긴 단어 우선 적용
    highlight_spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    filtered = []
    last_end = -1
    for start, end, color_code in highlight_spans:
        if start >= last_end:
            filtered.append((start, end, color_code))
            last_end = end
    # 색상 적용
    result = []
    last_idx = 0
    for start, end, color_code in filtered:
        result.append(txt_whole[last_idx:start])
        result.append(f"{color_code}{txt_whole[start:end]}{reset_code}")
        last_idx = end
    result.append(txt_whole[last_idx:])
    return ''.join(result)
