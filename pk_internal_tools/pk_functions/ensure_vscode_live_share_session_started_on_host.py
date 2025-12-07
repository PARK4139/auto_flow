"""
Host Machine (Windows)에서 VSCode Live Share 세션을 시작하는 함수

VSCode가 실행 중이고 Remote SSH로 Xavier에 연결되어 있는지 확인한 후,
Live Share 세션 시작 가이드를 제공합니다.
"""

import logging
import subprocess
import platform
from pathlib import Path
from typing import Optional, Tuple

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

logger = logging.getLogger(__name__)


# VSCode 설치 관련 함수들은 ensure_vscode_installed.py로 이동됨
# 이 파일에서는 import하여 사용


def _check_vscode_running() -> bool:
    """VSCode 프로세스가 실행 중인지 확인 (Windows)"""
    if platform.system() != "Windows":
        return False
    
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Code.exe"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return "Code.exe" in result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _check_vscode_extension_installed(extension_id: str) -> bool:
    """VSCode 확장 프로그램이 설치되어 있는지 확인"""
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return extension_id in result.stdout
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _get_clipboard_content() -> Optional[str]:
    """클립보드 내용 가져오기 (Windows)"""
    if platform.system() != "Windows":
        return None
    
    try:
        import win32clipboard
        
        win32clipboard.OpenClipboard()
        try:
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return clipboard_data if isinstance(clipboard_data, str) else None
        except:
            win32clipboard.CloseClipboard()
            return None
    except ImportError:
        # pywin32가 설치되지 않은 경우 PowerShell 사용
        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-Clipboard"
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None
    except:
        return None


def _extract_live_share_url(text: str) -> Optional[str]:
    """텍스트에서 Live Share URL 추출"""
    import re
    
    # Live Share URL 패턴
    pattern = r'https://prod\.liveshare\.vsengsaas\.visualstudio\.com/join[^\s\)]+'
    match = re.search(pattern, text)
    
    if match:
        return match.group(0)
    
    return None


# VSCode 설치 관련 함수들은 ensure_vscode_installed.py로 이동됨
# 이 파일에서는 import하여 사용


def _ensure_vscode_extension_installed(extension_id: str, extension_name: str = "") -> bool:
    """VSCode Extension이 설치되어 있는지 확인하고, 없으면 설치 시도"""
    if _check_vscode_extension_installed(extension_id):
        return True
    
    logger.warning("  ⚠️ %s Extension이 설치되어 있지 않습니다.", extension_name or extension_id)
    logger.info("  자동 설치 시도 중...")
    
    # 자동 설치 시도 (최대 2회)
    max_retries = 2
    for attempt in range(max_retries):
        try:
            logger.info("  설치 시도 %d/%d...", attempt + 1, max_retries)
            result = subprocess.run(
                ["code", "--install-extension", extension_id, "--force"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            if result.returncode == 0:
                # 설치 확인
                import time
                time.sleep(1)  # 설치 완료 대기
                
                if _check_vscode_extension_installed(extension_id):
                    logger.info("  ✅ %s Extension 설치 완료", extension_name or extension_id)
                    return True
                else:
                    logger.warning("  ⚠️ 설치되었지만 아직 인식되지 않습니다.")
            
            if result.stdout:
                # 설치 성공 메시지 확인
                if "successfully installed" in result.stdout.lower() or "설치되었습니다" in result.stdout:
                    logger.info("  ✅ %s Extension 설치 완료", extension_name or extension_id)
                    return True
            
            if attempt < max_retries - 1:
                logger.info("  재시도 중...")
                import time
                time.sleep(2)
                
        except Exception as e:
            logger.warning("  ⚠️ 자동 설치 실패 (시도 %d/%d): %s", attempt + 1, max_retries, e)
            if attempt < max_retries - 1:
                import time
                time.sleep(2)
    
    # 자동 설치 실패 시 수동 설치 안내
    logger.warning("  ⚠️ 자동 설치 실패. 수동으로 설치하세요.")
    logger.info("  설치 명령:")
    logger.info("    code --install-extension %s", extension_id)
    logger.info("  또는 VSCode에서:")
    logger.info("    1. 확장 프로그램 탭 (Ctrl+Shift+X)")
    logger.info("    2. '%s' 검색", extension_name or extension_id)
    logger.info("    3. 설치")
    
    return False


def ensure_vscode_live_share_session_started_on_host(
    xavier_host: Optional[str] = None,
    project_path: Optional[str] = None,
    auto_copy_url: bool = True,
) -> Optional[str]:
    """
    Host Machine에서 VSCode Live Share 세션을 시작합니다.
    
    VSCode가 실행 중이고 Remote SSH로 Xavier에 연결되어 있는지 확인한 후,
    Live Share 세션 시작 가이드를 제공합니다.
    
    Args:
        xavier_host: Xavier SSH 호스트명 (예: "xavier"). None이면 환경변수 또는 입력받기
        project_path: 프로젝트 디렉토리 경로 (Xavier 기준). None이면 입력받기
        auto_copy_url: URL을 자동으로 클립보드에서 읽어올지 여부
        
    Returns:
        Optional[str]: Live Share URL (시작 성공 시). None이면 실패 또는 사용자 입력 필요
    """
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
            ensure_env_var_completed_2025_11_24,
        )
        
        func_n = get_caller_name()
        
        logger.info("=" * 60)
        logger.info("VSCode Live Share 세션 시작 (Host Machine)")
        logger.info("=" * 60)
        
        # 1. VSCode 설치 확인 및 설치
        # ensure_vscode_installed() 함수 내부에서 먼저 설치 유무 확인 후, 없으면 설치 방법 선택
        from pk_internal_tools.pk_functions.ensure_vscode_installed import (
            check_vscode_installed,
            ensure_vscode_installed,
        )
        
        # 먼저 VSCode 설치 유무 확인
        logger.info("1. VSCode 설치 확인 중...")
        if not check_vscode_installed():
            logger.warning("  VSCode가 설치되어 있지 않습니다. 설치를 진행합니다...")
            if not ensure_vscode_installed():
                logger.error("  ❌ VSCode 설치에 실패했습니다.")
                logger.info("  수동으로 설치하세요: https://code.visualstudio.com/download")
                return None
            logger.error("  ❌ VSCode 설치에 실패했습니다.")
            logger.info("  수동으로 설치하세요: https://code.visualstudio.com/download")
            return None
        
        logger.info("  ✅ VSCode가 설치되어 있습니다.")
        
        # VSCode 버전 확인
        from pk_internal_tools.pk_functions.ensure_vscode_installed import (
            get_vscode_command_path,
        )
        
        code_command = get_vscode_command_path()
        if code_command:
            try:
                result = subprocess.run(
                    [code_command, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0 and result.stdout:
                    version = result.stdout.split('\n')[0] if result.stdout else "unknown"
                    logger.info("  VSCode 버전: %s", version)
            except Exception:
                pass
        
        # 2. VSCode 실행 중 확인
        logger.info("2. VSCode 실행 상태 확인 중...")
        if not _check_vscode_running():
            logger.warning("  ⚠️ VSCode가 실행 중이지 않습니다.")
            logger.info("  VSCode를 먼저 실행하세요:")
            logger.info("    code")
            logger.info("  또는")
            logger.info("    code --remote ssh-remote+xavier <프로젝트_경로>")
        else:
            logger.info("  ✅ VSCode가 실행 중입니다.")
        
        # 3. Remote SSH Extension 설치 확인 및 설치
        logger.info("3. Remote SSH Extension 설치 확인 중...")
        from pk_internal_tools.pk_functions.ensure_vscode_remote_ssh_installed_on_host import (
            ensure_vscode_remote_ssh_installed_on_host,
        )
        
        remote_ssh_installed = ensure_vscode_remote_ssh_installed_on_host()
        
        if not remote_ssh_installed:
            logger.warning("  ⚠️ Remote SSH Extension 설치가 완료되지 않았습니다.")
            logger.info("  Remote SSH 없이는 Xavier에 연결할 수 없습니다.")
            logger.info("  위의 설치 안내를 따라 수동으로 설치 후 다시 시도하세요.")
        
        # 4. Live Share Extension 설치 확인 및 설치
        logger.info("4. Live Share Extension 설치 확인 중...")
        live_share_extension_id = "ms-vsliveshare.vsliveshare"
        live_share_installed = _ensure_vscode_extension_installed(
            extension_id=live_share_extension_id,
            extension_name="Live Share",
        )
        
        if not live_share_installed:
            logger.warning("  ⚠️ Live Share Extension 설치가 완료되지 않았습니다.")
            logger.info("  Live Share 없이는 협업 세션을 시작할 수 없습니다.")
            logger.info("  수동으로 설치 후 다시 시도하세요:")
            logger.info("    code --install-extension ms-vsliveshare.vsliveshare")
        
        # 5. Live Share 세션 시작 가이드
        logger.info("")
        logger.info("=" * 60)
        logger.info("Live Share 세션 시작 방법:")
        logger.info("=" * 60)
        logger.info("")
        logger.info("1. VSCode에서 Xavier에 Remote SSH로 연결:")
        if xavier_host:
            logger.info("   - 호스트: %s", xavier_host)
            logger.info("   - 명령: code --remote ssh-remote+%s <프로젝트_경로>", xavier_host)
        else:
            logger.info("   - F1 > 'Remote-SSH: Connect to Host...'")
            logger.info("   - 또는: code --remote ssh-remote+xavier <프로젝트_경로>")
        
        if project_path:
            logger.info("   - 프로젝트 경로: %s", project_path)
        
        logger.info("")
        logger.info("2. 프로젝트 디렉토리 열기:")
        logger.info("   - File → Open Folder...")
        logger.info("   - Xavier의 프로젝트 디렉토리 선택")
        
        logger.info("")
        logger.info("3. Live Share 세션 시작:")
        logger.info("   방법 1: 왼쪽 하단 'Live Share' 버튼 클릭")
        logger.info("   방법 2: F1 > 'Live Share: Start Collaboration Session'")
        
        logger.info("")
        logger.info("4. URL 링크 확인:")
        logger.info("   - 세션이 시작되면 URL 링크가 클립보드에 자동 복사됨")
        logger.info("   - VSCode 하단에 'Session started' 메시지 표시")
        
        # 6. URL 읽기 시도
        if auto_copy_url:
            logger.info("")
            logger.info("5. 클립보드에서 URL 확인 중...")
            logger.info("   (Live Share 세션을 시작한 후 이 함수를 다시 실행하세요)")
            
            clipboard_content = _get_clipboard_content()
            if clipboard_content:
                live_share_url = _extract_live_share_url(clipboard_content)
                if live_share_url:
                    logger.info("  ✅ Live Share URL 발견:")
                    logger.info("  %s", live_share_url)
                    return live_share_url
                else:
                    logger.info("  ℹ️ 클립보드에 Live Share URL이 없습니다.")
            else:
                logger.info("  ℹ️ 클립보드를 읽을 수 없습니다.")
        
        # 7. 사용자 입력으로 URL 받기
        logger.info("")
        logger.info("6. Live Share URL 입력 (선택사항):")
        url_input = ensure_env_var_completed_2025_11_24(
            key_name="LIVE_SHARE_URL",
            func_n=func_n,
            guide_text="Live Share URL을 입력하세요 (Enter로 건너뛰기):",
            default_value="",
        )
        
        if url_input and url_input.strip():
            url = url_input.strip()
            if url.startswith("https://prod.liveshare.vsengsaas.visualstudio.com/"):
                logger.info("  ✅ Live Share URL 확인:")
                logger.info("  %s", url)
                return url
            else:
                logger.warning("  ⚠️ 유효한 Live Share URL 형식이 아닙니다.")
        
        # 8. 최종 안내
        logger.info("")
        logger.info("=" * 60)
        logger.info("다음 단계:")
        logger.info("=" * 60)
        logger.info("1. VSCode에서 Remote SSH로 Xavier에 연결")
        logger.info("2. 프로젝트 디렉토리 열기")
        logger.info("3. Live Share 세션 시작 (F1 > 'Live Share: Start Collaboration Session')")
        logger.info("4. URL 링크를 게스트와 공유")
        logger.info("")
        logger.info("상세 가이드: pk_docs/XAVIER_VSCODE_LIVE_SHARE_SETUP_GUIDE.md")
        logger.info("=" * 60)
        
        return None
        
    except Exception as e:
        logger.error("VSCode Live Share 세션 시작 중 예외가 발생했습니다: %s", e)
        import traceback
        logger.debug(traceback.format_exc())
        return None

