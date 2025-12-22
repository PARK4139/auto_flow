"""
paramiko를 사용해서 WSL에 Docker 설치하는 함수
"""
import logging
import os

import paramiko

from pk_internal_tools.pk_functions.ensure_wsl_ip_detected import ensure_wsl_ip_detected


def ensure_docker_installed_in_wsl_via_paramiko():
    """paramiko를 사용해서 WSL에 Docker를 설치하는 함수"""
    try:
        # n. WSL IP 주소 감지
        logging.debug("WSL IP 주소 감지 중...")
        wsl_ip = ensure_wsl_ip_detected()

        if not wsl_ip:
            logging.debug("WSL IP 주소를 찾을 수 없어 Docker 설치를 중단합니다.")
            return False

        # n. SSH 클라이언트 설정
        logging.debug("SSH 클라이언트 설정 중...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # SSH 키 경로
        ssh_key_path = os.path.expanduser('~/.ssh/id_ed25519')

        if not os.path.exists(ssh_key_path):
            logging.debug("SSH 키가 없습니다. SSH 키를 먼저 생성해주세요.")
            return False

        # SSH 연결
        try:
            ssh.connect(
                hostname=wsl_ip,
                port=22,
                username='ubuntu',  # WSL Ubuntu 사용자명
                key_file_name=ssh_key_path,
                timeout=30
            )
            logging.debug("SSH 연결 성공")
        except Exception as e:
            logging.debug(f"SSH 연결 실패: {str(e)}")
            return False

        # n. 시스템 업데이트
        logging.debug("1️⃣ 시스템 업데이트 중...")
        stdin, stdout, stderr = ssh.exec_command("sudo apt-get update -y", timeout=300)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            error_output = stderr.read().decode()
            logging.debug(f"시스템 업데이트 실패: {error_output}")
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
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=600)
            exit_status = stdout.channel.recv_exit_status()

            if exit_status != 0:
                error_output = stderr.read().decode()
                logging.debug(f"Docker 설치 실패: {error_output}")
                return False

        # n. Docker 서비스 시작
        logging.debug("3️⃣ Docker 서비스 시작 중...")
        stdin, stdout, stderr = ssh.exec_command("sudo systemctl start docker && sudo systemctl enable docker", timeout=60)
        exit_status = stdout.channel.recv_exit_status()

        # 6. 현재 사용자를 docker 그룹에 추가
        logging.debug("4️⃣ 현재 사용자를 docker 그룹에 추가 중...")
        stdin, stdout, stderr = ssh.exec_command("sudo usermod -aG docker $USER", timeout=30)
        exit_status = stdout.channel.recv_exit_status()

        # 7. Docker 설치 확인
        logging.debug("5️⃣ Docker 설치 확인 중...")
        stdin, stdout, stderr = ssh.exec_command("docker --version", timeout=30)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            output = stdout.read().decode().strip()
            logging.debug(f"Docker 설치 완료: {output}")
            ssh.close()
            return True
        else:
            error_output = stderr.read().decode()
            logging.debug(f"Docker 설치 확인 실패: {error_output}")
            ssh.close()
            return False

    except Exception as e:
        logging.debug(f"Docker 설치 중 오류 발생: {str(e)}")
        return False
