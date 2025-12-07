def kill_us_keyboard():
    """
    프로세스 간 공유 메모리를 내부에서 초기화하고 사용하도록 변경
    """
    import threading
    from multiprocessing import shared_memory, Lock

    ensure_pk_colorama_initialized_once()

    if get_os_n() == 'windows':
        ensure_chcp_65001()

    shm_name = "flag_to_detect_enter"
    lock = Lock()

    try:
        # 기존 공유 메모리 존재 여부 확인
        shm = shared_memory.SharedMemory(name=shm_name, create=False)
        logging.debug(rf"기존 공유 메모리 발견, 초기화 생략 shm_name={shm_name}")
    except FileNotFoundError:
        logging.debug(rf"새로운 공유 메모리 생성 shm_name={shm_name}")
        shm = shared_memory.SharedMemory(create=True, size=1, name=shm_name)
        shm.buf[0] = 0  # 초기값 False (0)

    def listen_enter():
        """사용자가 Enter 키를 입력하면 flag를 True로 설정"""
        try:
            existing_shm = shared_memory.SharedMemory(name=shm_name)
            flag = existing_shm.buf
        except FileNotFoundError:
            logging.debug("listen_enter: 공유 메모리가 존재하지 않음. 종료.")
            return

        while 1:
            input()  # Enter 입력 대기
            with lock:
                flag[0] = 1  # flag를 True로 변경
                logging.debug("Enter detected! flag 업데이트됨.")

        existing_shm.close()

    def main_loop():
        """flag 값이 True가 되면 특정 작업 수행 후 다시 False로 초기화"""
        try:
            existing_shm = shared_memory.SharedMemory(name=shm_name)
            flag = existing_shm.buf
        except FileNotFoundError:
            logging.debug("main_loop: 공유 메모리가 존재하지 않음. 종료.")
            return

        while 1:
            # exec 할 명령
            f_cmd = rf"{d_pk_external_tools}/ensure_us_keyboard_killed.cmd"
            f_cmd = Path(f_cmd)
            ensure_command_executed(cmd=rf'"{f_cmd}"', encoding=Encoding.CP949)

            # sleep
            sleep_seconds = 3
            for _ in range(sleep_seconds):
                with lock:
                    if flag[0]:  # flag가 True면 리셋 후 루프 재시작
                        logging.debug("Enter detected! Restarting loop...")

                        # pk_ensure_us_keyboard_killed.cmd (run)
                        f_cmd = rf"{d_pk_external_tools}/ensure_us_keyboard_killed.cmd"
                        f_cmd = Path(f_cmd)
                        ensure_command_executed(cmd=rf'"{f_cmd}"', encoding='utf-8')

                        flag[0] = 0  # flag를 다시 False로 초기화
                        logging.debug(f"wait for enter  ")
                        break
                ensure_slept(seconds=1)

        existing_shm.close()

    # thread run (in background)
    thread = threading.Thread(target=listen_enter, daemon=True)
    thread.start()

    # main loop run
    main_loop()

    # 공유 메모리 해제 (필요하면 exec )
    shm.close()
    # shm.unlink()  # 주석 해제하면 공유 메모리 삭제됨 (프로세스 간 공유 유지하려면 유지)


