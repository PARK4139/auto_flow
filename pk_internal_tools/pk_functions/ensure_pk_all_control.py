
import logging
import os
import subprocess
from pathlib import Path
import re

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers


def ensure_pk_all_control():
    """
    fzf 창에 타겟 목록을 표시하고 사용자가 선택하여 제어(이동/실행/종료)할 수 있도록 합니다.
    """
    # lazy imports
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_objects.pk_directories import d_pk_internal_tools
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized

    ensure_pk_log_initialized(__file__)
    
    func_n = get_caller_name()

    def get_targets():
        try:
            import psutil
            import pygetwindow
        except ImportError as e:
            logging.error(f"필수 라이브러리가 설치되지 않았습니다: {e}")
            logging.error("pip install psutil pygetwindow 를 실행해주세요.")
            return []

        targets = []
        running_processes = {}
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline']:
                    cmd_line = ' '.join(proc.info['cmdline'])
                    running_processes[cmd_line] = proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # n. pk_system 래퍼 파일 목록
        wrappers_dir = d_pk_wrappers
        wrapper_files = list(wrappers_dir.glob("pk_ensure_*.py"))

        for wrapper_file in wrapper_files:
            is_running = False
            pid = None
            matched_cmd = ""
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline_list = proc.info['cmdline']
                    if not cmdline_list:
                        continue

                    # 실행 파일이 python인지 확인
                    executable = Path(cmdline_list[0]).name.lower()
                    if 'python' not in executable:
                        continue

                    # 실행 인자에 wrapper_file.name이 직접 포함되는지 확인
                    for arg in cmdline_list[1:]:
                        if wrapper_file.name == Path(arg).name:
                            is_running = True
                            pid = proc.info['pid']
                            matched_cmd = ' '.join(cmdline_list)
                            break
                    
                    if is_running:
                        break # 일치하는 프로세스를 찾았으므로 내부 루프 종료
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if is_running:
                targets.append(f"(Running, PID: {pid}) {wrapper_file.name} | Reason: {matched_cmd}")
            else:
                targets.append(f"(Not Running) {wrapper_file.name}")

        # n. Chrome 창 목록
        try:
            chrome_windows = pygetwindow.getWindowsWithTitle('Chrome')
            for window in chrome_windows:
                if window.title and "Chrome" in window.title:
                    # 긴 제목은 자르기
                    title = (window.title[:70] + '..') if len(window.title) > 70 else window.title
                    targets.append(f"(Chrome Window) {title}")
        except Exception as e:
            logging.warning(f"Chrome 창 목록을 가져오는 데 실패했습니다: {e}")

        # 실행 중인 항목을 최상단으로 정렬
        targets.sort(key=lambda x: "(Running" not in x)

        return targets

    options = get_targets()
    for option in options:
        logging.debug(option)
    if not options:
        logging.warning("제어할 타겟을 찾을 수 없습니다.")
        return

    selected_target = ensure_value_completed_2025_10_13_0000(
        key_name="target_to_control",
        func_n=func_n,
        options=options,
        guide_text="제어할 타겟을 선택하세요:",
        history_reset=True
    )

    if not selected_target:
        logging.info("타겟 선택이 취소되었습니다.")
        return

    # 타겟 정보 파싱
    target_name = selected_target.split(' (')[0]
    target_info = selected_target

    action_options = ["이동 (Move to Front)", "실행 (Run/Start)", "종료 (Terminate)"]
    selected_action_raw = ensure_value_completed_2025_10_13_0000(
        key_name="action_to_perform",
        func_n=func_n,
        options=action_options,
        guide_text=f"'{target_name}'에 수행할 작업을 선택하세요:",
    )

    if not selected_action_raw:
        logging.info("작업 선택이 취소되었습니다.")
        return

    selected_action = selected_action_raw.split(' ')[0]

    # 작업 수행
    try:
        import psutil
        import pygetwindow
        from pk_internal_tools.pk_objects.pk_directories import d_pk_internal_tools

        if selected_action == "이동":
            if "Window" in target_info:
                # (Chrome Window) 접두사를 제거하여 실제 창 제목 추출
                actual_title = target_info.replace("(Chrome Window) ", "")
                logging.info(f"'{actual_title}' 창을 앞으로 가져옵니다.")

                # 제목이 길어서 잘렸을 수 있으므로, 'startswith'로 더 유연하게 검색
                search_title = actual_title
                if search_title.endswith('..'):
                    search_title = search_title[:-2]
                
                win_found = None
                for win in pygetwindow.getAllWindows():
                    if win.title.startswith(search_title):
                        win_found = win
                        break
                
                if win_found:
                    win_found.activate()
                else:
                    logging.error(f"'{actual_title}' 창을 찾을 수 없습니다. 이미 닫혔거나 제목이 변경되었을 수 있습니다.")
            else:
                logging.warning("창이 아닌 타겟은 '이동'할 수 없습니다.")

        elif selected_action == "실행":
            if "Not Running" in target_info:
                logging.info(f"'{target_name}' 스크립트를 실행합니다.")
                wrappers_dir = Path(d_pk_internal_tools) / "pk_wrappers"
                script_path = wrappers_dir / target_name
                subprocess.Popen(['python', str(script_path)], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                logging.warning(f"'{target_name}'은(는) 이미 실행 중이거나 실행할 수 없는 타겟입니다.")

        elif selected_action == "종료":
            if "Running" in target_info:
                pid_match = re.search(r"PID: (\d+)", target_info)
                if pid_match:
                    pid = int(pid_match.group(1))
                    logging.info(f"'{target_name}' (PID: {pid}) 프로세스를 종료합니다.")
                    p = psutil.Process(pid)
                    p.terminate()
                else:
                    logging.error("PID를 찾을 수 없어 프로세스를 종료할 수 없습니다.")
            else:
                logging.warning("실행 중이지 않은 타겟은 '종료'할 수 없습니다.")
    except ImportError as e:
        logging.error(f"작업 수행에 필요한 라이브러리가 없습니다: {e}")
    except Exception as e:
        logging.error(f"작업 수행 중 오류 발생: {e}")


if __name__ == '__main__':
    ensure_pk_all_control()
