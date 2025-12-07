

def get_minuites_and_remaining_secs(seconds):  # 큰단위로 단위변환 시 숫자는 작아지니 숫자가 작아지도록 약속된 숫자를 곱하면 된다.
    mins = seconds // 60
    secs_remaining = seconds % 60
    return mins, secs_remaining
