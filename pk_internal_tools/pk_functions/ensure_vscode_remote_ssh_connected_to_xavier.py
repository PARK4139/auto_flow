"""
VSCode Remote SSH 연결 자동화 함수

pk_asus(Windows)에서 VSCode Remote SSH를 사용하여 Xavier에 자동으로 연결합니다.
연결 시 VSCode Server가 Xavier에 자동으로 설치됩니다.

주의: 이 함수는 Host Machine (Windows)에서 실행되어야 합니다.
      Wireless Target (Xavier)에서 실행하면 안 됩니다.
"""

import logging
import subprocess
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.ensure_vscode_installed import (
    get_vscode_command_path,
)
from pk_internal_tools.pk_functions.ensure_vscode_remote_ssh_installed_on_host import (
    ensure_vscode_remote_ssh_installed_on_host,
)
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

logger = logging.getLogger(__name__)


def ensure_vscode_remote_ssh_connected_to_xavier(
    xavier_host: str = "xavier",
    xavier_ip: Optional[str] = None,
    xavier_user: Optional[str] = None,
    project_path: Optional[str] = None,
) -> bool:
    """
    Host Machine (Windows)에서 VSCode Remote SSH를 사용하여 Xavier에 자동으로 연결합니다.
    
    이 함수는 VSCode CLI 명령어를 사용하여 Remote SSH 연결을 시작합니다.
    연결이 성공하면 VSCode Server가 Xavier에 자동으로 설치됩니다.
    
    Args:
        xavier_host: SSH config에 정의된 호스트 이름 (기본값: "xavier")
                    또는 IP 주소 형식 (예: "pk@192.168.1.100")
        xavier_ip: Xavier IP 주소 (xavier_host가 IP 주소 형식이 아닌 경우 사용)
        xavier_user: Xavier 사용자명 (xavier_host가 IP 주소 형식이 아닌 경우 사용)
        project_path: 연결 후 열 프로젝트 경로 (Xavier의 절대 경로)
    
    Returns:
        bool: 연결 명령 실행 성공 여부 (실제 연결 완료 여부는 아님)
    
    Note:
        - 이 함수는 연결 명령만 실행합니다. 실제 연결 완료까지는 시간이 걸릴 수 있습니다.
        - VSCode가 이미 실행 중인 경우 새 창에서 연결이 시작됩니다.
        - VSCode가 실행되지 않은 경우 VSCode가 시작되고 연결이 시작됩니다.
    """
    try:
        func_n = get_caller_name()
        
        logger.info(f"VSCode Remote SSH 연결 자동화 시작 (호스트: {xavier_host})")
        
        # 1. VSCode 명령어 경로 확인
        code_command = get_vscode_command_path()
        if not code_command:
            logger.error("  ❌ VSCode가 설치되어 있지 않거나 code 명령을 찾을 수 없습니다.")
            logger.info("  → VSCode를 먼저 설치하세요: https://code.visualstudio.com/")
            return False
        
        logger.debug(f"  VSCode 명령어 경로: {code_command}")
        
        # 2. Remote SSH Extension 설치 확인 및 설치
        logger.info("  Remote SSH Extension 확인 중...")
        remote_ssh_installed = ensure_vscode_remote_ssh_installed_on_host()
        if not remote_ssh_installed:
            logger.error("  ❌ Remote SSH Extension이 설치되지 않았습니다.")
            logger.info("  → Remote SSH Extension을 먼저 설치하세요:")
            logger.info(f"    {code_command} --install-extension ms-vscode-remote.remote-ssh")
            return False
        
        logger.debug("  Remote SSH Extension이 설치되어 있습니다.")
        
        # 3. 연결할 호스트 이름 결정
        # xavier_host가 IP 주소 형식이면 그대로 사용, 아니면 ssh config에 정의된 호스트 이름 사용
        connect_host = xavier_host
        if xavier_ip and xavier_user:
            # IP 주소와 사용자명이 제공된 경우, 호스트 이름 대신 사용자@IP 형식 사용
            # 단, xavier_host가 이미 IP 주소 형식이면 그대로 사용
            if "@" not in xavier_host and not xavier_host.replace(".", "").replace(":", "").isdigit():
                connect_host = f"{xavier_user}@{xavier_ip}"
                logger.debug(f"  호스트 이름 구성: {connect_host} (사용자: {xavier_user}, IP: {xavier_ip})")
            else:
                logger.debug(f"  제공된 호스트 이름 사용: {connect_host}")
        else:
            logger.debug(f"  SSH config 호스트 이름 사용: {connect_host}")
        
        # 4. VSCode Remote SSH 연결 명령 구성
        # code --remote ssh-remote+<host> [project_path]
        remote_uri = f"ssh-remote+{connect_host}"
        cmd_args = [code_command, "--remote", remote_uri]
        
        if project_path:
            # 프로젝트 경로가 제공된 경우 추가
            project_path_str = str(Path(project_path))
            cmd_args.append(project_path_str)
            logger.info(f"  연결 후 프로젝트 열기: {project_path_str}")
        
        logger.info(f"  VSCode Remote SSH 연결 시도 중...")
        logger.debug(f"  실행 명령: {' '.join(cmd_args)}")
        
        # 5. VSCode Remote SSH 연결 명령 실행
        # 연결은 비동기로 시작되므로 subprocess.Popen을 사용하여 백그라운드에서 실행
        try:
            process = subprocess.Popen(
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0,
            )
            
            # 프로세스가 시작되었는지 확인 (실제 연결 완료까지는 시간이 걸림)
            logger.info(f"  ✅ VSCode Remote SSH 연결 프로세스 시작됨")
            logger.info(f"  → VSCode가 새 창에서 열리고 Xavier에 연결을 시도합니다.")
            logger.info(f"  → 연결이 완료되면 VSCode Server가 Xavier에 자동으로 설치됩니다.")
            logger.info(f"  → 연결 상태는 VSCode 왼쪽 하단 상태바에서 확인할 수 있습니다.")
            
            if project_path:
                logger.info(f"  → 프로젝트 디렉토리: {project_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"  ❌ VSCode Remote SSH 연결 명령 실행 실패: {e}")
            logger.info("  수동 연결 방법:")
            logger.info(f"    1. VSCode 실행")
            logger.info(f"    2. F1 > 'Remote-SSH: Connect to Host...'")
            logger.info(f"    3. '{connect_host}' 선택")
            if project_path:
                logger.info(f"    4. 프로젝트 열기: File → Open Folder... → {project_path}")
            return False
            
    except Exception as e:
        logger.error(f"VSCode Remote SSH 연결 자동화 중 오류 발생: {e}", exc_info=True)
        return False
