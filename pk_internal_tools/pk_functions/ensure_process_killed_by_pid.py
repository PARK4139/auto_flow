def ensure_process_killed_by_pid(pid, force_kill=False, timeout=10):
    import psutil

    import logging
    """
    이미지명 또는 PID로 프로세스를 종료하는 함수
    
    Args:
        pid (str or int): 프로세스명 또는 PID
        force_kill (bool): 강제 종료 여부 (기본값: False)
        timeout (int): 종료 대기 시간 (초, 기본값: 10)
    
    Returns:
        bool: 종료 성공 여부
    """
    try:
        # target이 숫자인지 확인 (PID인지)
        if isinstance(pid, str) and pid.isdigit():
            pid = int(pid)

        killed_processes = []

        if isinstance(pid, int):
            # PID로 프로세스 종료
            try:
                process = psutil.Process(pid)
                process_name = process.name()
                logging.debug(f"PID {pid} ({process_name}) 종료 시도 중...")

                if force_kill:
                    process.kill()
                    logging.debug(f"강제 종료됨: PID {pid} ({process_name})")
                else:
                    process.terminate()
                    logging.debug(f"정상 종료 요청: PID {pid} ({process_name})")

                killed_processes.append((pid, process_name))

            except psutil.NoSuchProcess:
                logging.debug(f"️ PID {pid} 프로세스가 존재하지 않습니다.")
                return False
            except psutil.AccessDenied:
                logging.debug(f"PID {pid} 프로세스 종료 권한이 없습니다.")
                return False

        else:
            # 이미지명으로 프로세스 종료
            target_name = pid.lower()
            found_processes = []

            # 실행 중인 프로세스 검색
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = proc.info['name'].lower()
                    if target_name in proc_name or proc_name in target_name:
                        found_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            if not found_processes:
                logging.debug(f"️ '{pid}' 프로세스를 찾을 수 없습니다.")
                return False

            logging.debug(f"'{pid}' 프로세스 {len(found_processes)}개 발견, 종료 시도 중...")

            # 발견된 프로세스들 종료
            for proc in found_processes:
                try:
                    proc_name = proc.info['name']
                    proc_pid = proc.info['pid']

                    if force_kill:
                        proc.kill()
                        logging.debug(f"강제 종료됨: {proc_name} (PID: {proc_pid})")
                    else:
                        proc.terminate()
                        logging.debug(f"정상 종료 요청: {proc_name} (PID: {proc_pid})")

                    killed_processes.append((proc_pid, proc_name))

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    logging.debug(f"️ {proc_name} (PID: {proc_pid}) 종료 실패")
                    continue

        # 종료된 프로세스들이 실제로 종료되었는지 확인
        if killed_processes:
            logging.debug(f"프로세스 종료 대기 중... (최대 {timeout}초)")

            for pid, name in killed_processes:
                try:
                    process = psutil.Process(pid)
                    process.wait(timeout=timeout)
                    logging.debug(f"종료 완료: {name} (PID: {pid})")
                except psutil.TimeoutExpired:
                    logging.debug(f"종료 시간 초과: {name} (PID: {pid})")
                except psutil.NoSuchProcess:
                    logging.debug(f"이미 종료됨: {name} (PID: {pid})")
                except psutil.AccessDenied:
                    logging.debug(f"종료 확인 실패: {name} (PID: {pid})")

            return True
        else:
            logging.debug("️ 종료할 프로세스가 없습니다.")
            return False

    except Exception as e:
        logging.debug(f"프로세스 종료 중 오류 발생: {e}")
        return False
