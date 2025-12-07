

def get_word_set_from_f_list(d_working):
    import os
    import re

    # n. 디렉토리 내 파일만 추출
    filenames = [
        f for f in os.listdir(d_working)
        if os.path.isfile(os.path.join(d_working, f))
    ]

    # 2) 숫자 접두사가 있을 땐 (0,숫자), 없으면 (1,이름) 으로 키 생성
    def sort_key(name: str):
        m = re.match(r'^(\d+)', name)
        if m:
            return (0, int(m.group(1)))
        return (1, name.lower())

    # 3) 정렬
    filenames_sorted = sorted(filenames, key=sort_key)

    # 4) 토큰 추출 & set에 추가
    tokens = set()
    for fname in filenames_sorted:
        parts = re.split(r'[.\s]+', fname)
        for p in parts:
            if p:
                tokens.add(p)

    return tokens
