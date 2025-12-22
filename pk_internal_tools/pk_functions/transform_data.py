

def transform_data(data, replacements):
    """
    주어진 데이터에서 주석(#)을 remove하고,
    "단어    [" 또는 "단어[" 패턴을 추출하여 지정된 매핑에 따라 개별적으로 치환합니다.
    닫는 인용부호(")는 그대로 유지합니다.

    Args:
        data (str): 변환할 원본 데이터 문자열.
        replacements (dict): 치환할 단어와 대체 문자열의 매핑 딕셔너리.
                             sample: {'음악틀기': ' ', '물먹기': '%%%BAR%%%'}

    Returns:
        str: 변환된 데이터 문자열.
    """
    import re

    transformed_lines = []
    lines = data.split('\n')

    # 정규 표현식 패턴
    # 패턴 1: "단어    [ 또는 "단어[ 패턴을 매칭하여 치환
    pattern_start = r'"([^"\[]+?)\s*\['

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            # 주석인 줄은 무시하고 변환 결과에 포함시키지 않음
            continue
        else:
            # 패턴 1 적용: "단어    [ 또는 "단어[ ->> "단어["
            match = re.search(pattern_start, line)
            if match:
                original_word = match.group(1).strip()
                # 치환할 단어가 replacements 딕셔너리에 있는지 확인
                if original_word in replacements:
                    replacement_word = replacements[original_word]
                    # 치환 수행: 원래 단어를 대체 단어로 교체
                    # sample: "음악틀기    [ ->> " [
                    transformed_line = re.sub(
                        r'"' + re.escape(original_word) + r'\s*\[',
                        f'"{replacement_word}[',
                        line
                    )
                else:
                    # 치환할 단어가 없으면 원래 라인을 그대로 유지
                    transformed_line = line
                transformed_lines.append(transformed_line)
            else:
                # 패턴에 매칭되지 않으면 원래 라인을 그대로 유지
                transformed_lines.append(line)

    # 변환된 모든 줄을 다시 하나의 문자열로 결합
    transformed_data = '\n'.join(transformed_lines)

    return transformed_data
