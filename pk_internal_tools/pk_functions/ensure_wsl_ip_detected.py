"""
WSL IP 주소 감지 함수
"""
import subprocess
import re
import logging


def ensure_wsl_ip_detected():
    """WSL의 IP 주소를 감지하는 함수"""
    try:
        # WSL에서 IP 주소 확인
        result = subprocess.run(
            ['wsl', '-d', 'Ubuntu', '-e', 'bash', '-c', 'hostname -I'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        
        if result.returncode == 0:
            ip_addresses = result.stdout.strip().split()
            if ip_addresses:
                # 첫 번째 IP 주소 사용 (보통 eth0의 IP)
                wsl_ip = ip_addresses[0]
                logging.debug(f"WSL IP 감지됨: {wsl_ip}")
                return wsl_ip
            else:
                logging.debug("WSL IP 주소를 찾을 수 없습니다.")
                return None
        else:
            logging.debug(f"WSL IP 확인 실패: {result.stderr}")
            return None
            
    except Exception as e:
        logging.debug(f"WSL IP 감지 중 오류 발생: {str(e)}")
        return None
