"""
Xavier에서 VSCode Live Share 서버를 시작하는 함수

Jetson Xavier를 headless 서버로 사용하여 VSCode Remote SSH + Live Share를 통한
협업 개발 환경을 구축하는 함수입니다.
"""

import logging
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS
from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkRemoteTargetEngine,
    PkModes2,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice

logger = logging.getLogger(__name__)


def _get_live_share_setup_guide() -> str:
    """VSCode Live Share 설정 가이드 텍스트 반환 (파일에서 읽어옴)"""
    guide_file = D_PK_EXTERNAL_TOOLS / "vscode_live_share_setup_guide.txt"
    guide_text = get_str_from_f(f=str(guide_file))
    
    if not guide_text:
        logger.warning(f"가이드 파일을 읽을 수 없습니다: {guide_file}")
        return "가이드 파일을 읽을 수 없습니다."
    
    return guide_text


def ensure_vscode_live_share_server_started_on_remote_target(
    remote_target_ip: Optional[str] = None,
    remote_target_user: Optional[str] = None,
    remote_target_pw: Optional[str] = None,
) -> bool:
    """
    Xavier에서 VSCode Live Share 서버를 시작합니다.
    
    Xavier에 VSCode Server가 설치되어 있는지 확인하고,
    Live Share Extension이 설치되어 있는지 확인합니다.
    필요 시 설치 가이드를 제공합니다.
    
    Args:
        remote_target_ip: remote_target_ip 주소. None이면 환경변수 또는 입력받기
        remote_target_user: Xavier 사용자명. None이면 환경변수 또는 입력받기
        remote_target_pw: Xavier 비밀번호. None이면 환경변수 또는 입력받기
        
    Returns:
        bool: 서버 준비 성공 여부
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import (
            ensure_env_var_completed,
        )
        
        func_n = get_caller_name()
        
        logger.info("=" * 60)
        logger.info("VSCode Live Share 서버 설정 (Xavier)")
        logger.info("=" * 60)
        
        # 가이드 표시
        logger.info(_get_live_share_setup_guide())
        
        # remote_target 연결 정보 가져오기
        if not remote_target_ip:
            remote_target_ip = ensure_env_var_completed(
                "XAVIER_IP",
                func_n=func_n,
                guide_text="remote_target_ip 주소를 입력하세요:",
            )
        if not remote_target_user:
            remote_target_user = ensure_env_var_completed(
                "XAVIER_USER",
                func_n=func_n,
                default_value="pk",
            )
        if not remote_target_pw:
            remote_target_pw = ensure_env_var_completed(
                "XAVIER_PW",
                func_n=func_n,
                guide_text="Xavier 비밀번호를 입력하세요 (SSH 키를 사용하는 경우 Enter):",
            )
        
        if not remote_target_ip:
            logger.error("remote_target_ip 주소가 입력되지 않았습니다.")
            return False
        
        # Xavier 컨트롤러 생성
        controller = PkRemoteTargetEngine(
            identifier=PkDevice.jetson_agx_xavier,
            
        )
        
        # 1. SSH 서버 상태 확인
        logger.info("1. SSH 서버 상태 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd="sudo systemctl is-active ssh",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code == 0 and stdout and "active" in stdout[0].lower():
            logger.info("  ✅ SSH 서버가 실행 중입니다.")
        else:
            logger.warning("  ⚠️ SSH 서버가 실행 중이지 않습니다.")
            logger.info("  SSH 서버 시작 명령:")
            logger.info("    sudo systemctl start ssh")
            logger.info("    sudo systemctl enable ssh")
        
        # 2. SSH 포트 확인
        logger.info("2. SSH 포트 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd="sudo netstat -tlnp | grep :22 || sudo ss -tlnp | grep :22",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code == 0 and stdout:
            logger.info("  ✅ SSH 포트 22가 열려있습니다.")
            for line in stdout[:3]:  # 처음 3줄만 출력
                logger.debug(f"    {line}")
        else:
            logger.warning("  ⚠️ SSH 포트 22가 열려있지 않을 수 있습니다.")
            logger.info("  방화벽 설정 명령:")
            logger.info("    sudo ufw allow ssh")
            logger.info("    sudo ufw allow 22/tcp")
        
        # 3. VSCode Server 설치 확인 (Xavier에)
        # 주의: VSCode 자체는 pk_asus(Windows)에 설치되어야 하고,
        # VSCode Server는 Remote SSH로 Xavier에 연결할 때 자동으로 설치됩니다.
        logger.info("3. Xavier에 VSCode Server 설치 확인 중...")
        logger.info("  (VSCode는 pk_asus(Windows)에 설치되어 있어야 합니다.)")
        logger.info("  (VSCode Server는 Remote SSH 연결 시 자동으로 Xavier에 설치됩니다.)")
        
        try:
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd="test -d ~/.vscode-server && echo 'exists' || echo 'not_found'",
                timeout_seconds=10,
                use_sudo=False,
            )
            
            # 디버그: stdout 내용 확인
            logger.debug(f"  VSCode Server 확인 - exit_code: {exit_code}")
            logger.debug(f"  VSCode Server 확인 - stdout: {stdout}")
            logger.debug(f"  VSCode Server 확인 - stderr: {stderr}")
            
            if exit_code == 0 and stdout and len(stdout) > 0:
                result = stdout[0].strip().lower() if stdout[0] else ""
                logger.debug(f"  VSCode Server 확인 결과: {result}")
                
                if result == "exists":
                    logger.info("  ✅ VSCode Server가 Xavier에 이미 설치되어 있습니다.")
                    
                    # VSCode Server 버전 확인
                    try:
                        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                            cmd="ls -d ~/.vscode-server/bin/* 2>/dev/null | head -1 | xargs basename 2>/dev/null || echo 'unknown'",
                            timeout_seconds=10,
                            use_sudo=False,
                        )
                        
                        logger.debug(f"  VSCode Server 버전 확인 - exit_code: {exit_code}")
                        logger.debug(f"  VSCode Server 버전 확인 - stdout: {stdout}")
                        
                        if exit_code == 0 and stdout and len(stdout) > 0:
                            version = stdout[0].strip() if stdout[0] else "unknown"
                            logger.info(f"VSCode Server 버전: {version}")
                        else:
                            logger.debug("  VSCode Server 버전 확인 실패 (stdout 비어있음)")
                    except Exception as e:
                        logger.debug(f"  VSCode Server 버전 확인 중 예외 발생: {e}")
                else:
                    logger.info("  ℹ️ Xavier에 VSCode Server가 아직 설치되지 않았습니다.")
                    logger.info("  → pk_asus(Windows)에서 VSCode Remote SSH로 Xavier에 연결하면 Xavier에 VSCode가 자동으로 설치됩니다.")
                    
                    # 자동 연결 시도 (pk_asus에서 실행)
                    try:
                        from pk_internal_tools.pk_functions.ensure_vscode_remote_ssh_connected_to_remote_target import (
                            ensure_vscode_remote_ssh_connected_to_remote_target,
                        )
                        
                        logger.info("  pk_asus에서 VSCode Remote SSH 연결 시도 중...")
                        if ensure_vscode_remote_ssh_connected_to_remote_target(
                            remote_target_host="remote_target",
                            remote_target_ip=remote_target_ip,
                            remote_target_user=remote_target_user,
                            project_path=None,  # 프로젝트 경로는 선택사항
                        ):
                            logger.info("  ✅ pk_asus에서 VSCode Remote SSH 연결 시작됨")
                            logger.info("  → 연결이 완료되면 VSCode Server가 Xavier에 자동으로 설치됩니다.")
                        else:
                            logger.warning("  ⚠️ 자동 연결에 실패했습니다. 수동으로 연결하세요.")
                            logger.info("  수동 연결 방법 (pk_asus에서):")
                            logger.info("    1. Windows에서 VSCode 실행")
                            logger.info("    2. F1 > 'Remote-SSH: Connect to Host...'")
                            logger.info(f"3. '{remote_target_user}@{remote_target_ip}' 또는 'remote_target' 선택")
                            logger.info("    4. 연결 후 VSCode Server가 Xavier에 자동 설치됨")
                    except ImportError as e:
                        logger.debug(f"  자동 연결 함수를 불러올 수 없습니다: {e}")
                        logger.info("  수동 연결 방법 (pk_asus에서):")
                        logger.info("    1. Windows에서 VSCode 실행")
                        logger.info("    2. F1 > 'Remote-SSH: Connect to Host...'")
                        logger.info(f"3. '{remote_target_user}@{remote_target_ip}' 또는 'remote_target' 선택")
                        logger.info("    4. 연결 후 VSCode Server가 Xavier에 자동 설치됨")
            else:
                logger.info(f"ℹ️ Xavier에 VSCode Server가 아직 설치되지 않았습니다. (exit_code: {exit_code}, stdout: {stdout})")
                logger.info("  → pk_asus(Windows)에서 VSCode Remote SSH로 Xavier에 연결하면 자동으로 설치됩니다.")
                
                # 자동 연결 시도 (pk_asus에서 실행)
                try:
                    from pk_internal_tools.pk_functions.ensure_vscode_remote_ssh_connected_to_remote_target import (
                        ensure_vscode_remote_ssh_connected_to_remote_target,
                    )
                    
                    logger.info("  pk_asus에서 VSCode Remote SSH 연결 시도 중...")
                    if ensure_vscode_remote_ssh_connected_to_remote_target(
                        remote_target_host="remote_target",
                        remote_target_ip=remote_target_ip,
                        remote_target_user=remote_target_user,
                        project_path=None,
                    ):
                        logger.info("  ✅ pk_asus에서 VSCode Remote SSH 연결 시작됨")
                        logger.info("  → 연결이 완료되면 VSCode Server가 Xavier에 자동으로 설치됩니다.")
                    else:
                        logger.warning("  ⚠️ 자동 연결에 실패했습니다. 수동으로 연결하세요.")
                        logger.info("  수동 연결 방법 (pk_asus에서):")
                        logger.info("    1. Windows에서 VSCode 실행")
                        logger.info("    2. F1 > 'Remote-SSH: Connect to Host...'")
                        logger.info(f"3. '{remote_target_user}@{remote_target_ip}' 또는 'remote_target' 선택")
                        logger.info("    4. 연결 후 VSCode Server가 Xavier에 자동 설치됨")
                except ImportError as e:
                    logger.debug(f"  자동 연결 함수를 불러올 수 없습니다: {e}")
                    logger.info("  수동 연결 방법 (pk_asus에서):")
                    logger.info("    1. Windows에서 VSCode 실행")
                    logger.info("    2. F1 > 'Remote-SSH: Connect to Host...'")
                    logger.info(f"3. '{remote_target_user}@{remote_target_ip}' 또는 'remote_target' 선택")
                    logger.info("    4. 연결 후 VSCode Server가 Xavier에 자동 설치됨")
        except Exception as e:
            logger.warning(f"  ⚠️ VSCode Server 확인 중 예외 발생: {e}", exc_info=True)
            logger.info("  → pk_asus(Windows)에서 VSCode Remote SSH로 Xavier에 연결하면 자동으로 설치됩니다.")
            
            # 자동 연결 시도 (pk_asus에서 실행)
            try:
                from pk_internal_tools.pk_functions.ensure_vscode_remote_ssh_connected_to_remote_target import (
                    ensure_vscode_remote_ssh_connected_to_remote_target,
                )
                
                logger.info("  pk_asus에서 VSCode Remote SSH 연결 시도 중...")
                if ensure_vscode_remote_ssh_connected_to_remote_target(
                    remote_target_host="remote_target",
                    remote_target_ip=remote_target_ip,
                    remote_target_user=remote_target_user,
                    project_path=None,
                ):
                    logger.info("  ✅ pk_asus에서 VSCode Remote SSH 연결 시작됨")
                    logger.info("  → 연결이 완료되면 VSCode Server가 Xavier에 자동으로 설치됩니다.")
                else:
                    logger.warning("  ⚠️ 자동 연결에 실패했습니다. 수동으로 연결하세요.")
            except ImportError:
                logger.debug("  자동 연결 함수를 불러올 수 없습니다.")
        
        # 4. Live Share Extension 설치 확인
        logger.info("4. Live Share Extension 설치 확인 중...")
        try:
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd="ls -d ~/.vscode-server/extensions/*vsliveshare* 2>/dev/null | head -1 || echo 'not_found'",
                timeout_seconds=10,
                use_sudo=False,
            )
            
            # 디버그: stdout 내용 확인
            logger.debug(f"  exit_code: {exit_code}")
            logger.debug(f"  stdout: {stdout}")
            logger.debug(f"  stderr: {stderr}")
            
            if exit_code == 0:
                # stdout이 비어있지 않고 첫 번째 줄에 경로가 있는지 확인
                if stdout and len(stdout) > 0:
                    extension_path = stdout[0].strip() if stdout[0] else ""
                    logger.debug(f"  extension_path: {extension_path}")
                    
                    # 'not_found' 문자열 체크 (대소문자 무시)
                    if extension_path and extension_path.lower() != "not_found" and "not_found" not in extension_path.lower():
                        logger.info("  ✅ Live Share Extension이 설치되어 있습니다.")
                        logger.info(f"경로: {extension_path}")
                    else:
                        logger.info("  ℹ️ Live Share Extension이 아직 설치되지 않았습니다.")
                        logger.info("  설치 방법:")
                        logger.info("    1. VSCode Remote SSH로 Xavier에 연결")
                        logger.info("    2. 확장 프로그램 탭 (Ctrl+Shift+X)")
                        logger.info("    3. 'Live Share' 검색")
                        logger.info("    4. 'Install in SSH: remote_target' 클릭")
                else:
                    logger.info("  ℹ️ Live Share Extension이 아직 설치되지 않았습니다. (stdout이 비어있음)")
                    logger.info("  설치 방법:")
                    logger.info("    1. VSCode Remote SSH로 Xavier에 연결")
                    logger.info("    2. 확장 프로그램 탭 (Ctrl+Shift+X)")
                    logger.info("    3. 'Live Share' 검색")
                    logger.info("    4. 'Install in SSH: remote_target' 클릭")
            else:
                logger.warning(f"  ⚠️ Live Share Extension 확인 명령 실행 실패 (exit_code: {exit_code})")
                if stderr:
                    for line in stderr:
                        logger.debug(f"    stderr: {line}")
                logger.info("  ℹ️ Live Share Extension이 아직 설치되지 않았습니다.")
                logger.info("  설치 방법:")
                logger.info("    1. VSCode Remote SSH로 Xavier에 연결")
                logger.info("    2. 확장 프로그램 탭 (Ctrl+Shift+X)")
                logger.info("    3. 'Live Share' 검색")
                logger.info("    4. 'Install in SSH: remote_target' 클릭")
        except Exception as e:
            logger.warning(f"  ⚠️ Live Share Extension 확인 중 예외 발생: {e}", exc_info=True)
            logger.info("  VSCode Remote SSH로 Xavier에 연결 후 확장 프로그램을 설치하세요.")
        
        # 5. 최종 안내
        logger.info("")
        logger.info("=" * 60)
        logger.info("다음 단계:")
        logger.info("=" * 60)
        logger.info("1. Windows에서 VSCode Remote SSH로 Xavier에 연결")
        logger.info("2. Live Share Extension이 설치되어 있는지 확인")
        logger.info("3. 프로젝트 디렉토리 열기 (File → Open Folder...)")
        logger.info("4. Live Share 세션 시작 (왼쪽 하단 Live Share 버튼)")
        logger.info("5. URL 링크를 게스트와 공유")
        logger.info("")
        logger.info("상세 가이드: pk_docs/XAVIER_VSCODE_LIVE_SHARE_SETUP_GUIDE.md")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"VSCode Live Share 서버 설정 중 예외가 발생했습니다: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return False
