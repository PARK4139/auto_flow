"""
기존 paramiko 도구들을 활용해서 WSL에 Docker 설치하는 함수
"""
import os
import logging
from pk_internal_tools.pk_functions.ensure_wsl_ip_detected import ensure_wsl_ip_detected
from pk_internal_tools.pk_functions.ensure_command_to_remote_os_with_pubkey import ensure_command_to_wireless_target_with_pubkey


def ensure_docker_installed_in_wsl_via_existing_paramiko():
    """기존 paramiko 도구들을 활용해서 WSL에 Docker를 설치하는 함수"""
    try:
        # n. WSL IP 주소 감지
        logging.debug("WSL IP 주소 감지 중...")
        wsl_ip = ensure_wsl_ip_detected()
        
        if not wsl_ip:
            logging.debug("WSL IP 주소를 찾을 수 없어 Docker 설치를 중단합니다.")
            return False
        
        # n. SSH 설정
        remote_device_target_config = {
            'ip': wsl_ip,
            'port': 22,
            'user_n': 'ubuntu',  # WSL Ubuntu 사용자명
            'local_ssh_private_key': os.path.expanduser('~/.ssh/id_ed25519')
        }
        
        # n. 시스템 업데이트
        logging.debug("1️⃣ 시스템 업데이트 중...")
        std_out, std_err = ensure_command_to_wireless_target_with_pubkey(
            "sudo apt-get update -y",
            **remote_device_target_config
        )
        
        if std_err and len(std_err) > 0:
            logging.debug(f"시스템 업데이트 실패: {std_err}")
            return False
        
        logging.debug("시스템 업데이트 완료")
        
        # n. Docker 설치
        logging.debug("2️⃣ Docker 설치 중...")
        docker_install_commands = [
            "sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release",
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
            "echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
            "sudo apt-get update -y",
            "sudo apt-get install -y docker-ce docker-ce-cli containerd.io"
        ]
        
        for cmd in docker_install_commands:
            logging.debug(f"실행 중: {cmd}")
            std_out, std_err = ensure_command_to_wireless_target_with_pubkey(cmd, **remote_device_target_config)
            
            if std_err and len(std_err) > 0:
                logging.debug(f"Docker 설치 실패: {std_err}")
                return False
        
        # n. Docker 서비스 시작
        logging.debug("3️⃣ Docker 서비스 시작 중...")
        std_out, std_err = ensure_command_to_wireless_target_with_pubkey(
            "sudo systemctl start docker && sudo systemctl enable docker",
            **remote_device_target_config
        )
        
        # 6. 현재 사용자를 docker 그룹에 추가
        logging.debug("4️⃣ 현재 사용자를 docker 그룹에 추가 중...")
        std_out, std_err = ensure_command_to_wireless_target_with_pubkey(
            "sudo usermod -aG docker $USER",
            **remote_device_target_config
        )
        
        # 7. Docker 설치 확인
        logging.debug("5️⃣ Docker 설치 확인 중...")
        std_out, std_err = ensure_command_to_wireless_target_with_pubkey(
            "docker --version",
            **remote_device_target_config
        )
        
        if std_out and len(std_out) > 0:
            logging.debug(f"Docker 설치 완료: {std_out[0]}")
            return True
        else:
            logging.debug("Docker 설치 확인 실패")
            return False
            
    except Exception as e:
        logging.debug(f"Docker 설치 중 오류 발생: {str(e)}")
        return False 