




def get_txt_highlighted_v2(txt_whole, config_highlight_dict):
    import re
    # mkr.
    # from colorama import init as pk_colorama_init
    # ensure_pk_colorama_initialized_once()
    PkColors = {
        "black": "\033[30m",
        'red': "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "grey": "\033[90m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
    }
    reset_code = "\033[0m"
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
