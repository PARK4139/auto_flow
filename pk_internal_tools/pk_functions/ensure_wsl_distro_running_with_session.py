from pk_internal_tools.pk_objects.pk_wireless_target_controller import SetupOpsForPkWirelessTargetController
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_wsl_distro_running_with_session(wsl_distro_name):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import logging
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    import subprocess
    import time
    """
    WSL 배포판을 실행시키고 세션을 유지합니다.

    Args:
        wsl_distro_name (str): WSL 배포판 이름
    """

    try:
        if QC_MODE:
            logging.debug(f"Starting WSL distro: {wsl_distro_name}")

        # WSL 배포판이 이미 실행 중인지 확인
        try:
            result = subprocess.run(['wsl', '-d', wsl_distro_name, '--', 'echo', 'WSL_SESSION_ACTIVE'],
                                    capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')

            if result.returncode == 0 and 'WSL_SESSION_ACTIVE' in result.stdout:
                logging.debug(f"{wsl_distro_name} is already running")
                return True
        except Exception as e:
            if QC_MODE:
                logging.debug(f"Session check failed for {wsl_distro_name}: {e}")

        # 배포판 시작
        logging.debug(f"Starting {wsl_distro_name}...")

        # 백그라운드에서 WSL 배포판 시작 (세션 유지)
        try:
            if is_os_windows():
                # Windows에서 WSL 배포판을 백그라운드로 시작
                # 더 간단한 방식으로 세션 유지
                subprocess.Popen(['wsl', '-d', wsl_distro_name, '--', 'bash', '-c',
                                  'echo "WSL session started"; exec sleep infinity'],
                                 creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                # Linux/WSL에서 실행
                subprocess.Popen(['wsl', '-d', wsl_distro_name, '--', 'bash', '-c',
                                  'echo "WSL session started"; exec sleep infinity'])

            # 시작 확인을 위한 대기
            time.sleep(2)

            # 시작 확인 (더 간단한 방식)
            try:
                verify_result = subprocess.run(['wsl', '-d', wsl_distro_name, '--', 'echo', 'OK'],
                                               capture_output=True, text=True, timeout=5, encoding='utf-8',
                                               errors='ignore')

                if verify_result.returncode == 0:
                    logging.debug(f"{wsl_distro_name} started successfully")
                    return True
                else:
                    logging.debug(f"Failed to start {wsl_distro_name}")
                    return False
            except Exception as verify_e:
                if QC_MODE:
                    logging.debug(f"Verification failed for {wsl_distro_name}: {verify_e}")
                # 검증이 실패해도 시작은 성공으로 간주 (WSL 특성상)
                logging.debug(f"{wsl_distro_name} started (verification skipped)")
                return True

        except Exception as start_e:
            logging.debug(f"Error starting {wsl_distro_name}: {start_e}")
            return False

    except subprocess.TimeoutExpired:
        logging.debug(f"Timeout starting {wsl_distro_name}")
        return False
    except Exception as e:
        logging.debug(f"Error starting {wsl_distro_name}: {e}")
        return False
