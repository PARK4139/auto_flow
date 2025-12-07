"""
WSL Ubuntu에 Docker 설치 함수
"""
import subprocess
import sys
import os

import logging

from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE


def ensure_docker_installed_in_wsl():
    """WSL Ubuntu에 Docker 설치"""
    logging.debug("WSL Ubuntu에 Docker 설치 중...")
    logging.debug(PK_UNDERLINE)
    
    try:
        # n. 시스템 업데이트
        logging.debug("1️⃣ 시스템 업데이트...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'sudo apt-get update'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("시스템 업데이트 완료")
        else:
            logging.debug(f"시스템 업데이트 실패: {result.stderr}")
            return False
        
        # n. 필요한 패키지 설치
        logging.debug("2️⃣ 필요한 패키지 설치...")
        packages = [
            'apt-transport-https',
            'ca-certificates',
            'curl',
            'gnupg',
            'lsb-release'
        ]
        
        for package in packages:
            result = subprocess.run(
                ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', f'sudo apt-get install -y {package}'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=300
            )
            if result.returncode == 0:
                logging.debug(f"{package} 설치 완료")
            else:
                logging.debug(f"{package} 설치 실패: {result.stderr}")
                return False
        
        # n. Docker GPG 키 추가
        logging.debug("3️⃣ Docker GPG 키 추가...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 
             'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("Docker GPG 키 추가 완료")
        else:
            logging.debug(f"Docker GPG 키 추가 실패: {result.stderr}")
            return False
        
        # n. Docker 저장소 추가
        logging.debug("4️⃣ Docker 저장소 추가...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 
             'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("Docker 저장소 추가 완료")
        else:
            logging.debug(f"Docker 저장소 추가 실패: {result.stderr}")
            return False
        
        # n. 패키지 목록 업데이트
        logging.debug("5️⃣ 패키지 목록 업데이트...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'sudo apt-get update'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("패키지 목록 업데이트 완료")
        else:
            logging.debug(f"패키지 목록 업데이트 실패: {result.stderr}")
            return False
        
        # 6. Docker 설치
        logging.debug("6️⃣ Docker 설치...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 
             'sudo apt-get install -y docker-ce docker-ce-cli containerd.io'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=600
        )
        if result.returncode == 0:
            logging.debug("Docker 설치 완료")
        else:
            logging.debug(f"Docker 설치 실패: {result.stderr}")
            return False
        
        # 7. Docker Compose 설치
        logging.debug("7️⃣ Docker Compose 설치...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 
             'sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("Docker Compose 설치 완료")
        else:
            logging.debug(f"Docker Compose 설치 실패: {result.stderr}")
            return False
        
        # 8. 현재 사용자를 docker 그룹에 추가
        logging.debug("8️⃣ 현재 사용자를 docker 그룹에 추가...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'sudo usermod -aG docker $USER'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("사용자를 docker 그룹에 추가 완료")
        else:
            logging.debug(f"사용자를 docker 그룹에 추가 실패: {result.stderr}")
            return False
        
        # 9. Docker 서비스 시작
        logging.debug("9️⃣ Docker 서비스 시작...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'sudo service docker start'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=300
        )
        if result.returncode == 0:
            logging.debug("Docker 서비스 시작 완료")
        else:
            logging.debug(f"Docker 서비스 시작 실패: {result.stderr}")
            return False
        
        # 10. 설치 확인
        logging.debug(" 설치 확인...")
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'docker --version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=10
        )
        if result.returncode == 0:
            logging.debug(f"Docker 설치 확인: {result.stdout.strip()}")
        else:
            logging.debug(f"Docker 설치 확인 실패: {result.stderr}")
            return False
        
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'docker-compose --version'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=10
        )
        if result.returncode == 0:
            logging.debug(f"Docker Compose 설치 확인: {result.stdout.strip()}")
        else:
            logging.debug(f"Docker Compose 설치 확인 실패: {result.stderr}")
            return False
        
        logging.debug("" + PK_UNDERLINE)
        logging.debug("Docker 설치가 완료되었습니다!")
        logging.debug("️  WSL을 재시작한 후 docker 명령어를 사용할 수 있습니다.")
        return True
        
    except Exception as e:
        logging.debug(f"오류 발생: {e}")
        return False


