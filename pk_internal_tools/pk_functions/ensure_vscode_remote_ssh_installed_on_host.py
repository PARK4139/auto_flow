"""
Host Machine (Windows)에서 VSCode Remote SSH Extension 설치 확인 및 설치 함수

pk_asus(Windows)에서 VSCode Remote SSH Extension이 설치되어 있는지 확인하고,
설치되어 있지 않은 경우 자동으로 설치를 시도합니다.

주의: 이 함수는 Host Machine (Windows)에서 실행되어야 합니다.
      Wireless Target (Xavier)에서 실행하면 안 됩니다.
"""

import logging
import subprocess
import time
from typing import Optional

from pk_internal_tools.pk_functions.ensure_vscode_installed import (
    get_vscode_command_path,
)
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

logger = logging.getLogger(__name__)

# Remote SSH Extension ID
REMOTE_SSH_EXTENSION_ID = "ms-vscode-remote.remote-ssh"
REMOTE_SSH_EXTENSION_NAME = "Remote SSH"


def check_vscode_extension_installed_on_host(extension_id: str) -> bool:
    """
    Host Machine (Windows)에서 VSCode Extension이 설치되어 있는지 확인합니다.
    
    Args:
        extension_id: 확인할 Extension ID (예: "ms-vscode-remote.remote-ssh")
        
    Returns:
        bool: Extension이 설치되어 있으면 True, 아니면 False
        
    Note:
        이 함수는 Host Machine (Windows)에서만 실행되어야 합니다.
    """
    code_command = get_vscode_command_path()
    if not code_command:
        logger.warning("VSCode가 설치되어 있지 않거나 code 명령을 찾을 수 없습니다.")
        return False
    
    try:
        result = subprocess.run(
            [code_command, "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            installed = extension_id in result.stdout
            if installed:
                logger.debug(f"Extension '{extension_id}'이(가) Host에 설치되어 있습니다.")
            else:
                logger.debug(f"Extension '{extension_id}'이(가) Host에 설치되어 있지 않습니다.")
            return installed
        else:
            logger.warning(f"Extension 목록 확인 실패: {result.stderr}")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"Extension 확인 중 오류 발생: {e}")
        return False
    except Exception as e:
        logger.error(f"Extension 확인 중 예상치 못한 오류: {e}")
        return False


def ensure_vscode_remote_ssh_installed_on_host() -> bool:
    """
    Host Machine (Windows)에서 VSCode Remote SSH Extension이 설치되어 있는지 확인하고,
    설치되어 있지 않은 경우 자동으로 설치를 시도합니다.
    
    Returns:
        bool: Extension이 설치되어 있거나 설치에 성공하면 True, 실패하면 False
        
    Note:
        이 함수는 Host Machine (Windows)에서만 실행되어야 합니다.
        Wireless Target (Xavier)에서 실행하면 안 됩니다.
        
    Example:
        >>> if ensure_vscode_remote_ssh_installed_on_host():
        ...     print("Remote SSH Extension이 설치되어 있습니다.")
        ... else:
        ...     print("Remote SSH Extension 설치에 실패했습니다.")
    """
    func_n = get_caller_name()
    
    logger.info("=" * 60)
    logger.info("VSCode Remote SSH Extension 설치 확인 (Host Machine)")
    logger.info("=" * 60)
    logger.info("")
    logger.info("대상: Host Machine (Windows) - pk_asus")
    logger.info("Extension: Remote SSH (ms-vscode-remote.remote-ssh)")
    logger.info("")
    
    # 1. VSCode 설치 확인
    logger.info("1. VSCode 설치 확인 중...")
    code_command = get_vscode_command_path()
    if not code_command:
        logger.error("  ❌ VSCode가 설치되어 있지 않거나 code 명령을 찾을 수 없습니다.")
        logger.info("  VSCode를 먼저 설치하세요:")
        logger.info("    from pk_internal_tools.pk_functions.ensure_vscode_installed import ensure_vscode_installed")
        logger.info("    ensure_vscode_installed()")
        return False
    
    logger.info("  ✅ VSCode가 설치되어 있습니다.")
    logger.info(f"명령 경로: {code_command}")
    
    # VSCode 버전 확인
    try:
        result = subprocess.run(
            [code_command, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout:
            version = result.stdout.split('\n')[0] if result.stdout else "unknown"
            logger.info(f"VSCode 버전: {version}")
    except Exception as e:
        pass
    
    # 2. Remote SSH Extension 설치 확인
    logger.info("")
    logger.info("2. Remote SSH Extension 설치 확인 중...")
    if check_vscode_extension_installed_on_host(REMOTE_SSH_EXTENSION_ID):
        logger.info(f"✅ {REMOTE_SSH_EXTENSION_NAME} Extension이 Host에 설치되어 있습니다.")
        logger.info("")
        logger.info("=" * 60)
        logger.info("설치 확인 완료")
        logger.info("=" * 60)
        return True
    
    logger.warning(f"  ⚠️ {REMOTE_SSH_EXTENSION_NAME} Extension이 Host에 설치되어 있지 않습니다.")
    logger.info("  자동 설치 시도 중...")
    
    # 3. 자동 설치 시도
    logger.info("")
    logger.info("3. Remote SSH Extension 자동 설치 시도 중...")
    max_retries = 2
    for attempt in range(max_retries):
        try:
            logger.info(f"설치 시도 {attempt + 1}/{max_retries}...")
            result = subprocess.run(
                [code_command, "--install-extension", REMOTE_SSH_EXTENSION_ID, "--force"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            if result.returncode == 0:
                # 설치 확인을 위해 잠시 대기
                time.sleep(1)
                
                if check_vscode_extension_installed_on_host(REMOTE_SSH_EXTENSION_ID):
                    logger.info(f"✅ {REMOTE_SSH_EXTENSION_NAME} Extension 설치 완료 (Host)")
                    logger.info("")
                    logger.info("=" * 60)
                    logger.info("설치 완료")
                    logger.info("=" * 60)
                    logger.info("")
                    logger.info("다음 단계:")
                    logger.info("  1. VSCode를 재시작하거나")
                    logger.info("  2. F1 > 'Remote-SSH: Connect to Host...'로 Xavier에 연결")
                    return True
                else:
                    logger.warning("  ⚠️ 설치되었지만 아직 인식되지 않습니다.")
                    logger.info("  VSCode를 재시작한 후 다시 확인하세요.")
            
            # stdout에서 설치 성공 메시지 확인
            if result.stdout:
                stdout_lower = result.stdout.lower()
                if "successfully installed" in stdout_lower or "설치되었습니다" in result.stdout:
                    logger.info(f"✅ {REMOTE_SSH_EXTENSION_NAME} Extension 설치 완료 (Host)")
                    logger.info("  VSCode를 재시작한 후 Extension이 활성화됩니다.")
                    return True
            
            if result.stderr:
                logger.debug(f"  stderr: {result.stderr}")
            
            if attempt < max_retries - 1:
                logger.info("  재시도 중...")
                time.sleep(2)
                
        except subprocess.TimeoutExpired:
            logger.warning(f"  ⚠️ 설치 시간 초과 (시도 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            logger.warning(f"  ⚠️ 자동 설치 실패 (시도 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
    
    # 4. 자동 설치 실패 시 수동 설치 안내
    logger.warning("")
    logger.warning("=" * 60)
    logger.warning("자동 설치 실패")
    logger.warning("=" * 60)
    logger.warning("")
    logger.warning("Remote SSH Extension을 수동으로 설치하세요:")
    logger.warning("")
    logger.warning("방법 1: CLI에서 설치")
    logger.warning(f"  {code_command} --install-extension {REMOTE_SSH_EXTENSION_ID}")
    logger.warning("")
    logger.warning("방법 2: VSCode GUI에서 설치")
    logger.warning("  1. VSCode 실행")
    logger.warning("  2. 확장 프로그램 탭 열기 (Ctrl+Shift+X)")
    logger.warning(f"  3. '{REMOTE_SSH_EXTENSION_NAME}' 검색")
    logger.warning("  4. Microsoft의 'Remote - SSH' 설치")
    logger.warning("")
    logger.warning("설치 후 VSCode를 재시작하세요.")
    logger.warning("")
    
    return False


if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import (
        ensure_pk_wrapper_starting_routine_done,
    )
    
    ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)
    
    try:
        result = ensure_vscode_remote_ssh_installed_on_host()
        if result:
            logger.info("✅ Remote SSH Extension이 Host에 설치되어 있습니다.")
        else:
            logger.warning("❌ Remote SSH Extension 설치에 실패했습니다.")
    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=True)


