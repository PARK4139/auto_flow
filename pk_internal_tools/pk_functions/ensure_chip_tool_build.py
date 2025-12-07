import subprocess
import logging

async def ensure_chip_tool_build() -> bool:
    logging.info("🚀 chip-tool 빌드 시작...")
    try:
        # chip-tool 존재 확인 (빌드된 파일)
        result = subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", "command -v chip-tool"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.returncode == 0 and result.stdout.strip():
            logging.info("chip-tool 이미 빌드됨.")
            return True # chip-tool이 이미 빌드되어 있으면 성공

        logging.info("chip-tool 빌드 중... (시간이 다소 소요될 수 있습니다.)")
        build_commands = [
            "cd connectedhomeip",
            "source scripts/activate.sh", # 환경 설정 스크립트 실행
            "gn gen out/host",
            "ninja -C out/host chip-tool"
        ]
        cmd = " && ".join(build_commands)
        subprocess.run(["wsl", "-d", "Ubuntu", "-e", "bash", "-c", cmd], check=True, timeout=600) # 10분 타임아웃
        logging.info("chip-tool 빌드 완료.")
        return True
    except subprocess.TimeoutExpired:
        logging.error("❌ chip-tool 빌드 시간 초과 (10분).")
        return False
    except Exception as e:
        logging.error(f"chip-tool 빌드 중 오류: {e}")
        return False