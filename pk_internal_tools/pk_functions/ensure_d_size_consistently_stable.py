


def ensure_d_size_consistently_stable(d_monitored, seconds_interval=0.1, check_times=30):
    """
    d_working _d_의 크기를 seconds_interval 초 동안 check_times 번 측정하고, 모든 측정 결과가 동일하면 True를 반환.

    :param d_monitored: 모니터링할 _d_의 절대경로
    :param seconds_interval: 측정 간격 (기본값 0.1초, 총 3초 동안 30번 측정)
    :param check_times: 총 측정 횟수 (기본값 30번)
    :return: 크기가 변하지 않으면 True, 변하면 False
    """

    import os
    def get_d_size(path):
        """_d_의 총 크기(바이트)를 반환하는 함수"""
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    # 첫 번째 측정
    initial_size = get_d_size(d_monitored)
    for _ in range(check_times):
        ensure_slept(seconds=seconds_interval)
        current_size = get_d_size(d_monitored)
        if current_size != initial_size:
            return 0  # 크기가 변하면 False 반환
    return 1  # 30번 동안 크기가 동일하면 True 반환
