def ensure_fd_exe_enabled():
    """fd (fd-find) 실행 파일이 설치되어 있는지 확인하고, 없다면 설치를 도와주는 함수"""
    import subprocess
    import os
    import sys
    import logging

    def check_fd_enabled():
        """fd가 설치되어 있는지 확인"""
        try:
            result = subprocess.run(
                ["fd", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                logging.debug(f"fd가 이미 설치되어 있습니다: {version}")
                return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return False

    def install_with_chocolatey():
        """Chocolatey를 사용하여 fd 설치"""
        try:
            logging.debug("Chocolatey를 사용하여 fd를 설치합니다...")
            result = subprocess.run(
                ["choco", "install", "fd", "--yes"], 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            if result.returncode == 0:
                logging.debug("fd 설치가 완료되었습니다!")
                return True
            else:
                logging.debug(f"Chocolatey 설치 실패: {result.stderr}")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            logging.debug(f"Chocolatey 설치 중 오류: {e}")
            return False

    def install_with_scoop():
        """Scoop을 사용하여 fd 설치"""
        try:
            logging.debug("Scoop을 사용하여 fd를 설치합니다...")
            result = subprocess.run(
                ["scoop", "install", "fd"], 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            if result.returncode == 0:
                logging.debug("fd 설치가 완료되었습니다!")
                return True
            else:
                logging.debug(f"Scoop 설치 실패: {result.stderr}")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            logging.debug(f"Scoop 설치 중 오류: {e}")
            return False

    def install_with_winget():
        """winget을 사용하여 fd 설치"""
        try:
            logging.debug("winget을 사용하여 fd를 설치합니다...")
            result = subprocess.run(
                ["winget", "install", "sharkdp.fd"], 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            if result.returncode == 0:
                logging.debug("fd 설치가 완료되었습니다!")
                return True
            else:
                logging.debug(f"winget 설치 실패: {result.stderr}")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            logging.debug(f"winget 설치 중 오류: {e}")
            return False

    def download_manual():
        """수동 다운로드 안내"""
        logging.debug("fd 수동 설치 방법:")
        logging.debug("1. https://github.com/sharkdp/fd/releases 방문")
        logging.debug("2. 최신 버전의 fd-v*.exe 다운로드")
        logging.debug("3. 다운로드한 파일을 C:\\Windows\\System32 또는 PATH에 추가된 폴더에 복사")
        logging.debug("4. 또는 fd.exe를 원하는 폴더에 두고 PATH에 추가")

    # n. fd가 이미 설치되어 있는지 확인
    if check_fd_enabled():
        return True

    logging.debug("fd가 설치되어 있지 않습니다.")
    logging.debug("fd는 find보다 훨씬 빠른 파일 검색 도구입니다.")

    # n. 설치 방법 선택
    install_methods = [
        "Chocolatey로 설치 (권장)",
        "Scoop으로 설치",
        "winget으로 설치",
        "수동 다운로드 안내",
        "설치 취소"
    ]

    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    selected_method = ensure_value_completed_2025_10_12_0000("설치 방법을 선택하세요: ", install_methods)
    
    if selected_method is None:
        logging.debug("설치가 취소되었습니다.")
        return False

    # n. 선택된 방법으로 설치 시도
    if selected_method == "Chocolatey로 설치 (권장)":
        # Chocolatey가 설치되어 있는지 확인
        try:
            subprocess.run(["choco", "--version"], capture_output=True, check=True)
            return install_with_chocolatey()
        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.debug("Chocolatey가 설치되어 있지 않습니다.")
            logging.debug("Chocolatey 설치: https://chocolatey.org/install")
            return False

    elif selected_method == "Scoop으로 설치":
        # Scoop이 설치되어 있는지 확인
        try:
            subprocess.run(["scoop", "--version"], capture_output=True, check=True)
            return install_with_scoop()
        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.debug("Scoop이 설치되어 있지 않습니다.")
            logging.debug("Scoop 설치: https://scoop.sh/")
            return False

    elif selected_method == "winget으로 설치":
        # winget이 설치되어 있는지 확인
        try:
            subprocess.run(["winget", "--version"], capture_output=True, check=True)
            return install_with_winget()
        except (subprocess.CalledProcessError, FileNotFoundError):
            logging.debug("winget이 설치되어 있지 않습니다.")
            logging.debug("winget은 Windows 10 1709 이상에서 사용 가능합니다.")
            return False

    elif selected_method == "수동 다운로드 안내":
        download_manual()
        return False

    else:  # 설치 취소
        logging.debug("설치가 취소되었습니다.")
        return False

    # n. 설치 후 다시 확인
    if check_fd_enabled():
        logging.debug("fd 설치가 완료되었습니다!")
        return True
    else:
        logging.debug("fd 설치에 실패했습니다. 수동으로 설치해주세요.")
        return False


if __name__ == "__main__":
    ensure_fd_exe_enabled() 