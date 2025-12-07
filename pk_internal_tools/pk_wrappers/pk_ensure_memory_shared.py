'''
프로세스 간 데이터 공유를 위해서 작성
기존방식 : 파일 기반 데이터 공유
신규방식 : shared memory 기반 데이터 공유
'''

# todo : chore : 중복 초기화 예방

import multiprocessing
import time
from multiprocessing import shared_memory


def process_a(shm_name, lock):
    """프로세스 A: flag를 확인하는 역할"""
    time.sleep(2)

    try:
        existing_shm = shared_memory.SharedMemory(name=shm_name)
    except FileNotFoundError:
        print("프로세스 A: 공유 메모리가 존재하지 않음. 종료.")
        return

    flag = existing_shm.buf[0]  # 공유 메모리의 첫 번째 바이트 값을 가져옴

    with lock:
        if flag:
            print(f"프로세스 A: flag 값 확인 → {flag} (이미 초기화됨)")
        else:
            print("프로세스 A: flag가 아직 초기화되지 않음")

    existing_shm.close()


if __name__ == "__main__":
    shm_name = "flag_to_detect_enter"

    try:
        # 기존 공유 메모리가 있는지 확인하고 없으면 새로 생성
        shm = shared_memory.SharedMemory(name=shm_name, create=False)
        print("기존 공유 메모리 발견, 초기화 생략")
    except FileNotFoundError:
        print("새로운 공유 메모리 생성")
        shm = shared_memory.SharedMemory(create=True, size=1, name=shm_name)
        shm.buf[0] = 0  # 초기값 False (0)

    lock = multiprocessing.Lock()

    pA = multiprocessing.Process(target=process_a, args=(shm_name, lock))

    pA.start()
    pA.join()

    # 공유 메모리 해제 (첫 번째 exec 에서는 삭제하지 않음)
    shm.close()
    # shm.unlink()  # 공유 메모리를 유지하려면 이 줄을 주석 처리
