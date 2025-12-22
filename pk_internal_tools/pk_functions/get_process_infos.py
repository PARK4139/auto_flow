def get_process_infos(unique: bool = True, sort: bool = True) -> list:
    """
    현재 실행 중인 모든 프로세스의 상세 정보 목록을 반환합니다.
    각 프로세스는 이름, 실행 경로, 커맨드 라인, 부모 프로세스 정보를 포함합니다.

    :param unique: True일 경우 이름이 같은 프로세스 중복 제거 (가장 먼저 발견된 프로세스 유지)
    :param sort: True일 경우 프로세스 이름을 기준으로 정렬
    :return: 프로세스 정보 딕셔너리 리스트
    """
    import psutil
    processes_data = []
    seen_names = set()

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'ppid']):
        try:
            pinfo = proc.info
            name = pinfo.get('name')
            exe = pinfo.get('exe')
            cmdline_list = pinfo.get('cmdline')
            if cmdline_list and isinstance(cmdline_list, list):
                cmdline = ' '.join(cmdline_list)
            else:
                cmdline = 'N/A'
            ppid = pinfo.get('ppid')
            parent_name = None

            if ppid:
                try:
                    parent_proc = psutil.Process(ppid)
                    parent_name = parent_proc.name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    parent_name = "N/A"

            if name:
                if unique and name in seen_names:
                    continue
                
                processes_data.append({
                    'name': name,
                    'pid': pinfo.get('pid', 0),
                    'path': exe if exe else 'N/A',
                    'command_line': cmdline if cmdline else 'N/A',
                    'parent': parent_name if parent_name else 'N/A',
                    'ppid': ppid if ppid is not None else 0
                })
                seen_names.add(name)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if sort:
        # Sort by PPID, then PID, then Name for a more structured view
        processes_data.sort(key=lambda x: (x['ppid'], x['pid'], x['name']))

    return processes_data


