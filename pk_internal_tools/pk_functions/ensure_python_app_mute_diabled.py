def ensure_python_app_mute_diabled():
    """
    Python 앱의 음소거 상태를 확인하고, 음소거되어 있다면 해제합니다.
    Windows 환경에서만 작동합니다.
    """
    # All imports moved inside the function as per user's instruction and lazy import rule
    import logging
    import subprocess
    import platform
    import time
    from pathlib import Path
    
    # Lazy import for circular dependency
    try:
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
    except ImportError:
        logging.error("ensure_seconds_measured 모듈을 임포트할 수 없습니다.", exc_info=True)
        return # 또는 다른 적절한 오류 처리

    # Imports for constants
    try:
        from pk_internal_tools.pk_objects.pk_directories import D_PK_LOGS
        from pk_internal_tools.pk_objects.pk_files import F_PK_LOG
    except ImportError:
        logging.error("필수 객체 모듈을 임포트할 수 없습니다.", exc_info=True)
        return # 또는 다른 적절한 오류 처리

    logging.debug("ensure_python_app_mute_diabled 함수 호출됨")

    if platform.system() != "Windows":
        logging.info("Windows 환경이 아니므로 음소거 비활성화 기능을 건너킵니다.")
        return

    try:
        # PowerShell 스크립트 경로
        script_path = Path("C:\\Users\\wjdgn\\Downloads\\pk_system\\pk_external_tools\\pk_os_layer_resources\\pk_windows\\pk_powershell\\ensure_python_app_mute_diabled.ps1")

        # PowerShell 스크립트 실행 (백그라운드에서 실행)
        command = f'powershell.exe -ExecutionPolicy Bypass -File "{script_path}"'
        
        # ensure_seconds_measured를 사용하여 실행 시간 측정
        with ensure_seconds_measured("ensure_python_app_mute_diabled_powershell_script_execution"):
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=10) # 10초 타임아웃

        if process.returncode == 0:
            logging.info(f"Python 앱 음소거 비활성화 스크립트 실행 성공. Stdout: {stdout.strip()}")
        else:
            logging.error(f"Python 앱 음소거 비활성화 스크립트 실행 실패. Stderr: {stderr.strip()}")

    except subprocess.TimeoutExpired:
        logging.error("PowerShell 스크립트 실행 시간 초과. 프로세스를 종료합니다.")
        process.kill()
        stdout, stderr = process.communicate()
        logging.error(f"Timeout Stdout: {stdout.strip()}, Stderr: {stderr.strip()}")
    except Exception as e:
        logging.error(f"음소거 비활성화 중 오류 발생: {e}", exc_info=True)
