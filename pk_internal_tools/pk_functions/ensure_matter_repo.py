import subprocess
import logging
import asyncio # Added for sleep

async def ensure_matter_repo() -> bool:
    logging.info("🚀 Matter Repository 클론/확인 시작...")
    try:
        # n. Git 설치 확인 및 설치 시도
        for _ in range(2): # 최대 2번 시도
            result = subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "command -v git"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0 and result.stdout.strip():
                logging.info("Git이 WSL에 설치되어 있습니다.")
                break
            else:
                logging.warning("⚠️ Git이 WSL에 설치되어 있지 않습니다. 설치를 시도합니다.")
                subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "sudo apt update && sudo apt install -y git"], check=True)
                logging.info("Git 설치 완료. 잠시 대기...")
                await asyncio.sleep(5) # 설치 후 Git이 PATH에 반영될 시간 대기
        
        # 최종 Git 확인
        result = subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "command -v git"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0 or not result.stdout.strip():
            logging.error("❌ Git 설치에 실패했거나 WSL 환경에서 Git을 찾을 수 없습니다.")
            return False

        # n. Matter Repository 클론
        result = subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "test -d ~/connectedhomeip"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0: # 디렉토리가 없으면 클론
            logging.info("Matter Repository 클론 중...")
            
            # --- WSL 네트워크 문제 자동 해결 시도 ---
            logging.info("🔧 WSL 네트워크 문제 자동 해결 시도 중...")
            try:
                logging.debug("Executing: wsl --shutdown")
                subprocess.run(["wsl", "--shutdown"], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                logging.info("WSL 종료 완료. 재시작 대기...")
                await asyncio.sleep(5) # 종료 후 재시작 대기
                # WSL 재시작은 다음 wsl 명령으로 자동 발생
            except Exception as e:
                logging.warning(f"⚠️ WSL 종료 중 오류 발생 (계속 진행): {e}")

            try:
                logging.debug("🔧 WSL DNS 설정 (8.8.8.8) 시도 중...")
                # /etc/resolv.conf 파일 생성/수정 및 immutable 설정
                dns_commands = [
                    "echo 'nameserver 8.8.8.8' | sudo tee /etc/resolv.conf > /dev/null",
                    "sudo chattr +i /etc/resolv.conf" # 파일 변경 방지
                ]
                cmd = " && ".join(dns_commands)
                subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", cmd], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                logging.info("WSL DNS 설정 완료 (8.8.8.8).")
            except Exception as e:
                logging.warning(f"⚠️ WSL DNS 설정 중 오류 발생 (계속 진행): {e}")
            # --- WSL 네트워크 문제 자동 해결 시도 끝 ---

            # WSL 네트워크 및 DNS 확인 (디버깅용)
            logging.debug("🔍 WSL 네트워크 및 DNS 확인 중...")
            from pk_internal_tools.pk_functions.ensure_pinged import ensure_pinged_2025_11_22 # Import ping function
            try:
                if ensure_pinged_2025_11_22("google.com"):
                    logging.debug("✅ WSL에서 google.com 핑 성공.")
                else:
                    logging.warning("⚠️ WSL에서 google.com 핑 실패.")
            except Exception as net_e:
                logging.warning(f"⚠️ WSL에서 google.com 핑 중 오류: {net_e}")
            try:
                # nslookup은 별도 함수가 없으므로 subprocess.run 유지
                result = subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "nslookup github.com"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
                if result.returncode == 0 and "Name:" in result.stdout: # Basic check for successful nslookup
                    logging.debug("✅ WSL에서 github.com DNS 확인 성공.")
                else:
                    logging.warning(f"⚠️ WSL에서 github.com DNS 확인 실패. Stdout: {result.stdout.strip()}. Stderr: {result.stderr.strip()}")
            except Exception as dns_e:
                logging.warning(f"⚠️ WSL에서 github.com DNS 확인 중 오류: {dns_e}")

            # 클론 실패 시 재시도 로직 추가
            for attempt in range(3): # 최대 3번 시도
                try:
                    logging.debug(f"Git 클론 시도 {attempt + 1}/3...")
                    proc = subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "git clone https://github.com/project-chip/connectedhomeip.git"], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=300) # 5분 타임아웃
                    
                    if proc.returncode == 0:
                        logging.info("Matter Repository 클론 완료.")
                        return True
                    else:
                        logging.warning(f"⚠️ Git 클론 실패 (종료 코드: {proc.returncode}). Stdout: {proc.stdout.strip()}. Stderr: {proc.stderr.strip()}. 재시도...")
                        await asyncio.sleep(10)
                except subprocess.TimeoutExpired:
                    logging.warning(f"⚠️ Matter Repository 클론 시간 초과 (시도 {attempt + 1}/3). 재시도...")
                    await asyncio.sleep(10)
                except Exception as clone_e:
                    logging.warning(f"⚠️ Matter Repository 클론 실패 (시도 {attempt + 1}/3): {clone_e}. 재시도...")
                    await asyncio.sleep(10)
            logging.error("❌ Matter Repository 클론에 최종 실패했습니다.")
            return False
        else:
            logging.info("Matter Repository 이미 클론됨.")
            return True
    except Exception as e:
        logging.error(f"Matter Repository 클론/확인 중 오류: {e}")
        return False