def is_containing_special_characters_with_thread(text: str):
    import re
    import threading
    # 비동기 처리 설정 ( advanced  )
    nature_numbers = [n for n in range(1, 101)]  # from 1 to 100
    work_quantity = len(text)
    n = 4  # thread_cnt # interval_cnt
    d = work_quantity // n  # interval_size
    r = work_quantity % n
    start_1 = 0
    end_1 = d - 1
    starts = [start_1 + (n - 1) * d for n in nature_numbers[:n]]  # 등차수열 official
    ends = [end_1 + (n - 1) * d for n in nature_numbers[:n]]
    remained_start = ends[-1] + 1
    remained_end = work_quantity

    # print(rf'nature_numbers : {nature_numbers}')  # 원소의 길이의 합이 11넘어가면 1에서 3까지만 표기 ... 의로 표시 그리고 마지막에서 3번째에서 마지막에서 0번째까지 표기 cut_list_proper_for_pretty()
    # print(rf'work_quantity : {work_quantity}')
    # print(rf'n : {n}')
    # print(rf'd : {d}')
    # print(rf'r : {r}')
    # print(rf'start_1 : {start_1}')
    # print(rf'end_1 : {end_1}')
    # print(rf'starts : {starts}')
    # print(rf'ends : {ends}')
    # print(rf'remained_start : {remained_start}')
    # print(rf'remained_end : {remained_end}')

    # 비동기 이벤트 함수 설정 ( advanced  )
    async def is_containing_special_characters(start_index: int, end_index: int, text: str):
        pattern = "[~!@#$%^&*()_+|<>?:{}]"  # , 는 제외인가?
        if re.search(pattern, text[start_index:end_index]):
            # print(f"쓰레드 {start_index}에서 {end_index}까지 작업 성공 True return")
            result_list.append(True)
            # return 1
        else:
            result_list.append(False)
            # print(f"쓰레드 {start_index}에서 {end_index}까지 작업 성공 False return")
            # return 0

    # 비동기 이벤트 루프 설정
    def run_async_event_loop(start_index: int, end_index: int, text: str):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(is_containing_special_characters(start_index, end_index, text))

    # 스레드 객체를 저장할 리스트 생성
    threads = []

    # 각 스레드의 결과를 저장할 리스트
    # result_list=[None] * work_quantity
    result_list = []

    # 주작업 처리용 쓰레드
    for n in range(0, n):
        start_index = starts[n]
        end_index = ends[n]
        thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index, text))
        thread.start()
        threads.append(thread)

    # 남은 작업 처리용 쓰레드
    if remained_end <= work_quantity:
        start_index = remained_start
        end_index = remained_end
        thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index, text))
        thread.start()
        threads.append(thread)
    else:
        start_index = remained_start
        end_index = start_index  # end_index 를 start_index 로 하면 될 것 같은데 테스트필요하다.
        thread = threading.Thread(target=run_async_event_loop, args=(start_index, end_index, text))
        thread.start()
        threads.append(thread)

    # 모든 스레드의 작업이 종료될 때까지 대기
    for thread in threads:
        thread.join()

    # 먼저 종료된 스레드가 있는지 확인하고, 나머지 스레드 중지
    # for thread in threads:
    #     if not thread.is_alive():
    #         for other_thread in threads:
    #             if other_thread != thread:
    #                 other_thread.cancel()
    #         break

    # 바뀐 부분만 결과만 출력, 전체는 abspaths_and_mtimes 에 반영됨
    # print(rf'result_list : {result_list}')
    # print(rf'type(result_list) : {type(result_list)}')
    # print(rf'len(result_list) : {len(result_list)}')

    if all(result_list):
        # logging.debug("쓰레드 작업결과 result_list의 모든 요소가 True이므로 True를 반환합니다")
        return 1
    else:
        # logging.debug("쓰레드 작업결과 result_list에 False인 요소가 있어 False를 반환합니다")
        pass
