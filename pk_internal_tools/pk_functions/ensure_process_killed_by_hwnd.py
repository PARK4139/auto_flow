from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_process_name_by_pid import get_process_name_by_pid


@ensure_seconds_measured
def ensure_process_killed_by_hwnd(hwnd: int) -> bool:
    from pk_internal_tools.pk_functions.get_pid_from_hwnd import get_pid_from_hwnd
    import logging
    import psutil
    try:
        pid = get_pid_from_hwnd(hwnd)
        process_name = get_process_name_by_pid(pid)
        logging.debug(rf"pid={pid}")
        logging.debug(rf"process_name={process_name}")
        input()
        if not pid:
            logging.warning(f"HWND {hwnd} 로 PID를 찾을 수 없음")
            return False

        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            logging.info(f"PID {pid} 프로세스 없음 (이미 종료됨)")
            return True

        logging.info(f"프로세스 종료 시도: PID={pid}, name={proc.name()}")
        proc.terminate()
        try:
            proc.wait(timeout=5)
            logging.info(f"프로세스 {pid} 정상 종료됨")
        except psutil.TimeoutExpired:
            logging.warning(f"프로세스 {pid} 종료 지연 → 강제 kill")
            proc.kill()

        return True

    except Exception as e:
        logging.error(f"ensure_process_killed_by_hwnd 실패: {e}")
        return False
