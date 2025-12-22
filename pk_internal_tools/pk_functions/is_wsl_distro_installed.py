import subprocess
import logging

def is_wsl_distro_installed(distro_name: str) -> bool:
    """
    Checks if a WSL distribution with the given name is installed.
    """
    try:
        # Using --quiet lists only the names, which is faster and cleaner to parse.
        # If the distro is installed, its name will be in the output.
        result = subprocess.run(
            ["wsl", "--list", "--quiet"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='ignore'
        )
        installed_distros = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        
        if distro_name in installed_distros:
            logging.debug(f"WSL 배포판 '{distro_name}'이(가) 설치되어 있습니다.")
            return True
        else:
            logging.debug(f"WSL 배포판 '{distro_name}'이(가) 설치되어 있지 않습니다.")
            return False
    except FileNotFoundError:
        logging.error("WSL 명령어를 찾을 수 없습니다. WSL이 설치되어 있는지 확인하십시오.")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"WSL 명령어 실행 중 오류가 발생했습니다: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"WSL 배포판 설치 여부 확인 중 예상치 못한 오류 발생: {e}")
        return False