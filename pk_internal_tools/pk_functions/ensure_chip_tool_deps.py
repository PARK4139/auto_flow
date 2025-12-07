import subprocess
import logging

async def ensure_chip_tool_deps() -> bool:
    logging.debug("➡️ ensure_chip_tool_deps 함수 시작")
    logging.info("🔧 chip-tool 종속성 설치 시작...")
    try:
        logging.info("chip-tool 종속성 설치 중...")
        cmd = "sudo apt update && sudo apt install -y git gcc g++ pkg-config libssl-dev libdbus-1-dev libglib2.0-dev libavahi-client-dev ninja-build python3-venv python3-dev python3-pip unzip"
        logging.debug(f"Executing: wsl -d Ubuntu -e bash -c \"{cmd}\"")
        subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", cmd], check=True)
        logging.info("chip-tool 종속성 설치 완료.")
        logging.debug("⬅️ ensure_chip_tool_deps 함수 종료 (성공)")
        return True
    except Exception as e:
        logging.error(f"chip-tool 종속성 설치 중 오류: {e}")
        logging.debug("⬅️ ensure_chip_tool_deps 함수 종료 (오류 발생)")
        return False
