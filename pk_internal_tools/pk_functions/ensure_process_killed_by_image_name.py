import logging
import os

import psutil

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def _get_current_pid():
    current_pid = os.getpid()
    return current_pid


def _get_current_process(current_pid):
    return psutil.Process(current_pid)


def get_parent_pid(current_process):
    return current_process.ppid()

@ensure_seconds_measured
def ensure_process_killed_by_image_name(image_name, force_kill=False, timeout=10):
    """프로세스 종료 (현재 프로세스와 테스트 관련 프로세스 제외)"""
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    import psutil

    # 현재 프로세스와 부모 프로세스 보호

    current_pid = _get_current_pid()
    current_process = _get_current_process(current_pid)

    # 현재 프로세스의 부모 프로세스 찾기
    parent_pid = None
    try:
        parent_pid = get_parent_pid(current_process)

    except:
        pass

    logging.debug(f"현재 프로세스 ID: {current_pid}")
    logging.debug(f"부모 프로세스 ID: {parent_pid}")
    logging.debug(f"대상 이미지명: {image_name}")

    # 보호할 프로세스 ID 목록
    protected_pids = set()

    # 현재 프로세스 계열 보호
    pids_to_kill = []

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == image_name:
                proc_pid = proc.info['pid']

                is_protected = False

                # 현재 프로세스나 부모 프로세스는 보호
                if proc_pid == current_pid or proc_pid == parent_pid:
                    protected_pids.add(proc_pid) # Still track for logging
                    logging.debug(f"[ensure_process_killed_by_image_name] [보호] 현재/부모 프로세스: PID {proc_pid}")
                    is_protected = True

                # 부모 프로세스 체인 확인
                if not is_protected: # Only check if not already protected
                    try:
                        parent = proc.parent()
                        if parent and parent.pid == current_pid:
                            protected_pids.add(proc_pid) # Still track for logging
                            logging.debug(f"[ensure_process_killed_by_image_name] [보호] 자식 프로세스: PID {proc_pid}")
                            is_protected = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass # Parent might have exited

                # 테스트 관련 프로세스는 보호
                if not is_protected: # Only check if not already protected
                    cmdline = proc.info['cmdline']
                    if cmdline:
                        cmd_str = ' '.join(cmdline).lower()
                        if any(keyword in cmd_str for keyword in ['test', 'ensure_test', 'benchmark', 'scenario']):
                            protected_pids.add(proc_pid) # Still track for logging
                            logging.debug(f"[ensure_process_killed_by_image_name] [보호] 테스트 관련 프로세스: PID {proc_pid} - {cmd_str}")
                            is_protected = True
                
                if not is_protected:
                    pids_to_kill.append(proc_pid)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    logging.debug(f"[ensure_process_killed_by_image_name] 보호된 프로세스 수: {len(protected_pids)}")
    logging.debug(f"[ensure_process_killed_by_image_name] 보호된 PID 목록: {list(protected_pids)}")
    logging.debug(f"[ensure_process_killed_by_image_name] 종료할 PID 수: {len(pids_to_kill)}")
    logging.debug(f"[ensure_process_killed_by_image_name] 종료할 PID 목록: {pids_to_kill}")


    # 보호할 프로세스가 있다면 개별적으로 종료
    if pids_to_kill: # Use pids_to_kill list
        logging.info(f"[ensure_process_killed_by_image_name] 종료할 프로세스가 있어서 개별 종료 방식 사용")
        killed_count = 0
        for pid_to_kill in pids_to_kill:
            try:
                proc = psutil.Process(pid_to_kill)
                logging.info(f"[ensure_process_killed_by_image_name] [종료] 프로세스: PID {pid_to_kill}")
                proc.terminate()
                killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                logging.debug(f"[ensure_process_killed_by_image_name] PID {pid_to_kill} 종료 실패 (이미 종료되었거나 접근 거부).")
                continue
        logging.info(f"[ensure_process_killed_by_image_name] 종료된 프로세스 수: {killed_count}")
    else:
        logging.info(f"[ensure_process_killed_by_image_name] 보호할 프로세스가 없어서 기존 방식 사용")
        # 모든 프로세스 종료 (기존 방식) - This path is now less likely to be taken if image_name is found
        return ensure_command_executed(f'taskkill /f /im "{image_name}"')

    return True
