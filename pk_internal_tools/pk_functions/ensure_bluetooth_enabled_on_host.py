import logging
import subprocess
from typing import Tuple
import asyncio

from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

async def ensure_bluetooth_enabled_on_host() -> Tuple[bool, str]:
    logging.info("호스트 시스템의 Bluetooth 상태를 확인합니다...")
    
    if is_os_windows():
        try:
            # PowerShell 명령을 사용하여 Bluetooth 서비스 상태 확인
            # BthAvctpSvc: Bluetooth Audio/Video Control Transport Protocol Service
            # bthserv: Bluetooth Support Service
            command = "powershell -Command \"Get-Service -Name BthAvctpSvc,bthserv -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Status\""
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            stdout_str = stdout.decode().strip()
            stderr_str = stderr.decode().strip()

            if process.returncode == 0:
                statuses = stdout_str.splitlines()
                all_running = all(status.strip().lower() == 'running' for status in statuses)
                
                if all_running:
                    logging.info("Windows 호스트 Bluetooth 서비스가 활성화되어 있습니다.")
                    return True, "Windows Bluetooth services are running."
                else:
                    logging.warning(f"Windows 호스트 Bluetooth 서비스 중 일부 또는 전부가 실행 중이 아닙니다. 상태: {stdout_str}")
                    logging.warning("Bluetooth를 활성화하려면 Windows 설정에서 Bluetooth를 켜고, 서비스(services.msc)에서 'Bluetooth 지원 서비스' 및 'Bluetooth 오디오 게이트웨이 서비스'가 실행 중인지 확인하세요.")
                    return False, f"Windows Bluetooth services not fully running: {stdout_str}"
            else:
                logging.error(f"Windows Bluetooth 서비스 상태 확인 실패 (종료 코드: {process.returncode}). Stderr: {stderr_str}")
                return False, f"Failed to check Windows Bluetooth services: {stderr_str}"
        except Exception as e:
            logging.error(f"Windows Bluetooth 상태 확인 중 예외 발생: {e}")
            return False, f"Exception during Windows Bluetooth check: {e}"
    else: # Assume Linux/WSL
        logging.info("Linux/WSL 환경입니다. 호스트 Bluetooth 상태는 직접 확인할 수 없습니다. 물리적 호스트에서 Bluetooth가 활성화되어 있는지 확인하세요.")
        # We cannot directly check the Windows host's Bluetooth from WSL, so we assume it's handled externally.
        # For the purpose of proceeding with Docker, we'll return True, but with a warning.
        return True, "Host Bluetooth status assumed to be enabled (running in Linux/WSL)."