def kill_thread(thread_name):
    import threading
    # 종료할 스레드 이름

    # 현재 exec  중인 모든 스레드 가져오기
    current_threads = threading.enumerate()

    # 종료할 스레드 찾기
    target_thread = None
    for thread in current_threads:
        if thread.name == thread_name:
            target_thread = thread
            break

    # 스레드 종료
    if target_thread:
        target_thread.join()
        print(f"{thread_name} 스레드가 종료되었습니다.")
    else:
        print(f"{thread_name} 스레드를 찾을 수 없습니다.")


