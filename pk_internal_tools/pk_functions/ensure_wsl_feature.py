import subprocess
import logging

async def ensure_wsl_feature() -> bool:
    logging.debug("➡️ ensure_wsl_feature 함수 시작")
    logging.info("🚀 WSL 기능 설치/확인 시작...")
    try:
        logging.debug("🔍 WSL 기능 상태 확인 중...")
        result = subprocess.run(["powershell", "-Command", "Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux | Select-Object -ExpandProperty State"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        wsl_feature_state = result.stdout.strip()
        logging.debug(f"WSL 기능 상태: {wsl_feature_state}")
        if wsl_feature_state != "Enabled":
            logging.info("WSL 기능 활성화 중...")
            logging.debug("Executing: dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart")
            subprocess.run(["powershell", "-Command", "dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart"], check=True)
            logging.debug("Executing: dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart")
            subprocess.run(["powershell", "-Command", "dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart"], check=True)
            logging.info("💡 WSL 기능 활성화 완료. 시스템 재부팅이 필요할 수 있습니다.")
            logging.debug("⬅️ ensure_wsl_feature 함수 종료 (WSL 기능 활성화 완료)")
        else:
            logging.info("WSL 기능 이미 활성화됨.")
            logging.debug("⬅️ ensure_wsl_feature 함수 종료 (WSL 기능 이미 활성화됨)")
        return True
    except Exception as e:
        logging.error(f"WSL 기능 활성화 확인/설치 중 오류: {e}")
        logging.debug("⬅️ ensure_wsl_feature 함수 종료 (오류 발생)")
        return False