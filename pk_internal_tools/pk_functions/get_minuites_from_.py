

def get_minuites_from_(
        seconds):  # 큰단위로 단위변환 시 숫자는 작아지니 숫자가 작아지도록 약속된 숫자를 곱하면 된다. # seconds ->> min  인 경우 큰단위로 변환되고 있고 약속된 숫자는 60 이다. 작은 숫자를 생성 위해서 1/60 을 곱한다.
    return round(seconds / 60, 2)
