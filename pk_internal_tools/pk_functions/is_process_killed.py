import logging
from pk_internal_tools.pk_functions.get_window_title import get_window_title


def is_process_killed(window_title_seg: str, timeout: float = 1.0) -> bool:
    """
    주어진 window_title_seg에 해당하는 CMD 프로세스가 종료되었는지 확인하고 종료 시도.
    :param window_title_seg: 윈도우 제목 일부 문자열
    :param timeout: 종료 대기 시간 (초)
    :return: True (모두 종료됨), False (하나라도 종료 실패)
    """
    import psutil
    import os

    def get_pids_by_title_seg(windows_title_seg: str) -> list[int]:
        matches = get_window_title(windows_title_seg)
        if not matches:
            return []

        # 첫 번째 매칭된 타이틀을 기준으로 process 검색
        target = os.path.splitext(os.path.basename(matches[0]))[0].lower()
        return [
            proc.info['pid']
            for proc in psutil.process_iter(['pid', 'name', 'cmdline'])
            if proc.info['name'].lower() == 'cmd.exe'
               and target in " ".join(proc.info.get('cmdline', [])).lower()
        ]

    try:
        pids = get_pids_by_title_seg(window_title_seg)

        if not pids:
            logging.debug(f"[SKIP] No matching process found for '{window_title_seg}'")
            return True  # 이미 종료된 것으로 간주

        all_killed = True

        for pid in pids:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                try:
                    proc.wait(timeout=timeout)
                except psutil.TimeoutExpired:
                    proc.kill()
                    try:
                        proc.wait(timeout=timeout)
                    except psutil.TimeoutExpired:
                        logging.debug(f"PID={pid} 종료 실패 (TIMEOUT)")
                        all_killed = False
                        continue

                if proc.is_running():
                    logging.debug(f"️ PID={pid} 여전히 실행 중")
                    all_killed = False
                else:
                    logging.debug(f"PID={pid} 종료 확인됨")

            except psutil.NoSuchProcess:
                continue
            except Exception as e:
                logging.debug(f"예외 발생 PID={pid}, error={e}")
                all_killed = False

        return all_killed

    except Exception as e:
        logging.warning(f"전체 종료 확인 실패: {e}")
        return False
