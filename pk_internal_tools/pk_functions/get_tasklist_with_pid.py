def get_tasklist_with_pid():
    """
    tasklist/ps 명령어의 결과에서 이미지명과 PID를 함께 수집

    Returns:
        list: (이미지명, PID) 튜플 리스트
    """
    import re
    import subprocess
    import logging
    import os # For os.path.basename

    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    try:
        if is_os_windows():
            # Windows tasklist 명령어 실행
            try:
                result = subprocess.run(['tasklist', '/FO', 'CSV'],
                                        capture_output=True,
                                        text=True,
                                        encoding='cp949')
            except UnicodeDecodeError:
                result = subprocess.run(['tasklist', '/FO', 'CSV'],
                                        capture_output=True,
                                        text=True,
                                        encoding='utf-8',
                                        errors='ignore')

            if result.returncode != 0:
                logging.debug(f"tasklist 명령어 실행 실패: {result.stderr}")
                return []

            if not result.stdout:
                logging.debug("️ tasklist 명령어 결과가 비어있습니다.")
                return []

            lines = result.stdout.strip().split('\n')

            # 첫 번째 줄은 헤더이므로 제외
            if lines and lines[0].startswith('"Image Name"'):
                lines = lines[1:]

            processes = []

            for line in lines:
                if line.strip():
                    parts = re.findall(r'"([^"]*)"', line)
                    if len(parts) >= 2:
                        image_name = parts[0].strip()
                        pid = parts[1].strip()
                        if image_name and image_name.lower() != 'image name' and pid.isdigit():
                            processes.append((image_name, int(pid)))

        else:
            # Linux/macOS ps 명령어 실행
            try:
                result = subprocess.run(['ps', 'aux'],
                                        capture_output=True,
                                        text=True,
                                        encoding='utf-8')
            except Exception as e:
                logging.debug(f"ps 명령어 실행 실패: {e}")
                return []

            if result.returncode != 0:
                logging.debug(f"ps 명령어 실행 실패: {result.stderr}")
                return []

            if not result.stdout:
                logging.debug("️ ps 명령어 결과가 비어있습니다.")
                return []

            lines = result.stdout.strip().split('\n')

            # 첫 번째 줄은 헤더이므로 제외
            if lines and 'USER' in lines[0]:
                lines = lines[1:]

            processes = []

            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            pid = int(parts[1])
                            command = parts[10] if len(parts) >= 11 else parts[1]
                            if command and command != 'PID':
                                image_name = os.path.basename(command)
                                if image_name:
                                    processes.append((image_name, pid))
                        except (ValueError, IndexError):
                            continue

        if processes:
            cmd_name = "tasklist" if is_os_windows() else "ps"
            logging.debug(f"{cmd_name}에서 {len(processes)}개의 프로세스를 수집했습니다.")
        else:
            logging.debug("️ 프로세스 목록을 찾을 수 없습니다.")


        return processes

    except Exception as e:
        logging.debug(f"프로세스 목록 처리 중 오류 발생: {e}")
        return []
