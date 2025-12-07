import subprocess
import logging
import asyncio
from pk_internal_tools.pk_functions.is_wsl_distro_installed import is_wsl_distro_installed

async def ensure_wsl_distro(distro_name: str = "Ubuntu") -> bool:
    logging.debug(f"➡️ ensure_wsl_distro 함수 시작 (배포판: {distro_name})")
    logging.info(f"🚀 WSL 배포판 '{distro_name}' 설치/확인 시작...")
    try:
        logging.debug(f"🔍 '{distro_name}' 배포판 설치 여부 확인 중...")
        if not is_wsl_distro_installed(distro_name):
            logging.info(f"{distro_name} 배포판 설치 중...")
            logging.debug(f"Executing: wsl --install -d {distro_name}")
            subprocess.run(["wsl", "--install", "-d", distro_name], check=True)
            logging.info("💡 Ubuntu 배포판 설치 완료. 초기 설정(사용자 이름/비밀번호)을 위해 WSL 창이 열릴 수 있습니다.")
            logging.info("⚠️ WSL 창에서 사용자 이름과 비밀번호를 설정해야 합니다. 이 과정은 자동화할 수 없습니다.")
            logging.debug("Waiting 10 seconds for user interaction...")
            await asyncio.sleep(10) # 충분한 시간 대기
            logging.debug("⬅️ ensure_wsl_distro 함수 종료 (배포판 설치 완료)")
        else:
            logging.info(f"{distro_name} 배포판 이미 설치됨.")
            logging.debug("⬅️ ensure_wsl_distro 함수 종료 (배포판 이미 설치됨)")
        return True
    except Exception as e:
        logging.error(f"{distro_name} 배포판 설치 확인/설치 중 오류: {e}")
        logging.debug("⬅️ ensure_wsl_distro 함수 종료 (오류 발생)")
        return False

async def ensure_wsl_default_version_2() -> bool:
    logging.debug("➡️ ensure_wsl_default_version_2 함수 시작")
    logging.info("🚀 기본 WSL 버전 2로 설정 확인 시작...")
    try:
        logging.debug("Executing: wsl --set-default-version 2")
        subprocess.run(["wsl", "--set-default-version", "2"], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        logging.info("기본 WSL 버전 2로 설정 완료.")
        logging.debug("⬅️ ensure_wsl_default_version_2 함수 종료 (성공)")
        return True
    except Exception as e:
        logging.warning(f"⚠️ 기본 WSL 버전 설정 중 오류 (계속 진행): {e}")
        logging.debug("⬅️ ensure_wsl_default_version_2 함수 종료 (오류 발생)")
        return False