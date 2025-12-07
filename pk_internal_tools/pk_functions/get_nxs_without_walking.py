

def get_nxs_without_walking(mode=None, d_src=None):
    import os
    if d_src is None:
        d_src = os.getcwd()  # 현재 작업 d로 설정

    # 절대경로로 변환
    d_src = os.path.abspath(d_src)

    # 리스트로 결과를 받기 위한 변수
    f_list = []
    d_list = []

    # os.scandir() 사용하여 더 빠르게 항목 탐색
    try:
        with os.scandir(d_src) as it:
            for entry in it:
                if entry.is_dir():  # d일 경우
                    d_list.append(entry.name)  # d 이름 추가
                elif entry.is_file():  # f일 경우
                    f_list.append(entry.name)  # f 이름 추가
    except FileNotFoundError:
        print(f"d '{d_src}'을 찾을 수 없습니다.")
        return []

    # 원하는 mode에 따라 f, d, 혹은 둘 다 반환
    if mode == "f":
        return f_list
    elif mode == "d":
        return d_list
    else:
        return f_list + d_list
