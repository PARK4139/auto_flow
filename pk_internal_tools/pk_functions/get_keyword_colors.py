def get_keyword_colors():
    """
    다중 키워드 하이라이트를 위한 색상 리스트를 반환합니다.
    각 키워드는 다른 색상으로 하이라이트됩니다.
    """
    return [
        '\033[34;47m',  # Blue text on White background
        '\033[35;47m',  # Magenta text on White background  
        '\033[36;47m',  # Cyan text on White background
        '\033[32;47m',  # Green text on White background
        '\033[33;47m',  # Yellow text on White background
    ]


def highlight_multiple_keywords_fast(text, search_keywords):
    """
    텍스트에서 다중 키워드를 하이라이트하는 함수
    
    Args:
        text (str): 하이라이트할 텍스트
        search_keywords (list): 검색할 키워드 리스트
    
    Returns:
        str: 하이라이트가 적용된 텍스트
    """
    import re
    
    if not search_keywords or not text:
        return text
    
    keyword_colors = get_keyword_colors()
    
    # 각 키워드를 순서대로 하이라이트
    highlighted_text = text
    for i, keyword in enumerate(search_keywords):
        if keyword:
            color = keyword_colors[i % len(keyword_colors)]
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            highlighted_text = pattern.sub(lambda m: color + m.group(0) + '\033[0m', highlighted_text)
    
    return highlighted_text 