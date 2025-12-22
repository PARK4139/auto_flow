def get_image_names_from_tasklist():
    """
    tasklist/ps 명령어의 결과에서 이미지명을 수집하고 중복을 제거한 리스트를 반환

    Returns:
        list: 이미지명 리스트 (중복 제거됨)
    """
    import re
    import subprocess
    import logging
    import os # For os.path.basename

    from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
    from pk_internal_tools.pk_functions.get_list_removed_element_empty import get_list_removed_empty
    from pk_internal_tools.pk_functions.get_list_striped_element import get_list_striped_element
    from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    try:
        if is_os_windows():
            # Windows tasklist 명령어 실행
            try:
                result = subprocess.run(['tasklist', '/FO', 'CSV'],
                                        capture_output=True,
                                        text=True,
                                        encoding='cp949')  # Windows 한국어 인코딩
            except UnicodeDecodeError:
                # cp949 실패 시 기본 인코딩으로 재시도
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

            image_names = []

            for line in lines:
                if line.strip():
                    # CSV 형식에서 첫 번째 컬럼(이미지명) 추출
                    parts = re.findall(r'"([^"]*)"', line)
                    if parts:
                        image_name = parts[0].strip()  # 첫 번째 컬럼이 이미지명
                        if image_name and image_name.lower() != 'image name':
                            image_names.append(image_name)

        elif is_os_linux():
            # Linux ps 명령어 실행
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

            image_names = []

            for line in lines:
                if line.strip():
                    # ps aux 형식에서 마지막 컬럼(명령어) 추출
                    parts = line.split()
                    if len(parts) >= 11:
                        command = parts[10]  # 마지막 컬럼이 명령어
                        if command and command != 'COMMAND':
                            # 경로에서 파일명만 추출
                            image_name = os.path.basename(command)
                            if image_name:
                                image_names.append(image_name)

        else:
            # macOS ps 명령어 실행
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

            image_names = []

            for line in lines:
                if line.strip():
                    # ps aux 형식에서 마지막 컬럼(명령어) 추출
                    parts = line.split()
                    if len(parts) >= 11:
                        command = parts[10]  # 마지막 컬럼이 명령어
                        if command and command != 'COMMAND':
                            # 경로에서 파일명만 추출
                            image_name = os.path.basename(command)
                            if image_name:
                                image_names.append(image_name)

        # 중복 제거 및 정렬
        if image_names:
            # 빈 문자열 제거
            image_names = get_list_removed_empty(image_names)

            # 앞뒤 공백 제거
            image_names = get_list_striped_element(image_names)

            # 중복 제거
            image_names = get_list_deduplicated(image_names)

            # 알파벳 순으로 정렬
            image_names.sort(key=str.lower)

            cmd_name = "tasklist" if is_os_windows() else "ps"
            logging.debug(f"{cmd_name}에서 {len(image_names)}개의 고유한 이미지명을 수집했습니다.")
        else:
            logging.debug("️ 프로세스 목록에서 이미지명을 찾을 수 없습니다.")

        return image_names

    except Exception as e:
        logging.debug(f"프로세스 목록 처리 중 오류 발생: {e}")
        return []
