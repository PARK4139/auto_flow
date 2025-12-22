# @ensure_seconds_measured
def calculate_similarity_beteen_window_title_and_target(target: str, window_title: str) -> float:
    """창 제목과 타겟의 유사도 계산 - 완전히 동일한 파일명만 매칭"""
    import os

    target_lower = target.lower()
    title_lower = window_title.lower()

    # 파일명 (확장자 제외)
    target_name = os.path.splitext(target)[0].lower()

    # 가장 엄격한 매칭: 창 제목이 파일명과 정확히 일치하는 경우만
    # n. 창 제목이 파일명과 정확히 일치 (확장자 포함)
    if title_lower == target_lower:
        return 1.0

    # n. 창 제목이 파일명과 정확히 일치 (확장자 제외)
    if title_lower == target_name:
        return 1.0

    # 그 외의 경우는 모두 0.0 (매칭하지 않음)
    # 이전의 광범위한 매칭 제거:
    # - 파일명이 창 제목의 단어 중 하나와 일치하는 경우
    # - 창 제목이 파일명으로 시작/끝나는 경우
    # - 부분 문자열 매칭
    return 0.0
