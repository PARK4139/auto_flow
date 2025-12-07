import os


def ensure_terminal_info_retrieved():
    """현재 터미널 환경 정보를 반환합니다."""
    info = []
    
    # OS 정보
    info.append(f"OS: {os.name}")
    
    # 환경 변수
    if 'POWERSHELL_TELEMETRY_OPTOUT' in os.environ:
        info.append("PowerShell 환경 변수 감지됨")
    
    # 프로세스 정보
    try:
        import psutil
        current_process = psutil.Process()
        parent = current_process.parent()
        if parent:
            info.append(f"부모 프로세스: {parent.nick_name()}")
    except:
        info.append("프로세스 정보 확인 불가")
    
    return " | ".join(info)
