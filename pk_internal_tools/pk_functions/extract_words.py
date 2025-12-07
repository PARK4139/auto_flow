

def extract_words(data):
    """
    주어진 데이터에서 주석(#)을 remove하고,
    각 줄에서 "단어    [" 또는 "단어[" 패턴에 있는 단어들을 추출합니다.

    Args:
        data (str): 변환할 원본 데이터 문자열.

    Returns:
        list: 추출된 단어들의 리스트.
    """
    import re

    extracted_words = []
    lines = data.split('\n')

    # 정규 표현식 패턴
    # 패턴 설명:
    # - ^[^#]*": 라인이 #으로 시작하지 않으며, "으로 시작하는 부분을 찾음
    # - ([^"\[]+?): "와 [ 사이의 단어를 캡처
    # - \s*\[: 공백이 있을 수도 없을 수도 있고, 그 뒤에 [가 오는 패턴
    pattern = r'^[^#]*"([^"\[]+?)\s*\['

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            # 주석인 줄은 무시
            continue
        # 정규 표현식 매칭 시도
        match = re.search(pattern, line)
        if match:
            word = match.group(1).strip()
            extracted_words.append(word)

    return extracted_words
