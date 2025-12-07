def get_d_size_and_f_cnt(d_working):
    """_d_ f개수 크기 반환"""
    import os
    total_size = 0
    f_cnt = 0
    with os.scandir(d_working) as it:
        for entry in it:
            try:
                if entry.is_file():
                    total_size += entry.stat().st_size
                    f_cnt += 1
                elif entry.is_dir():
                    sub_size, sub_count = get_d_size_and_f_cnt(entry.path)
                    total_size += sub_size
                    f_cnt += sub_count
            except FileNotFoundError:
                pass  # 이동 중 삭제된 f 처리
    return total_size, f_cnt
