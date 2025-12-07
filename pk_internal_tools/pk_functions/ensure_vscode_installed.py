"""
VSCode 설치 확인 및 자동 설치 함수

Windows에서 VSCode가 설치되어 있는지 확인하고,
설치되어 있지 않은 경우 다양한 방법으로 설치를 시도합니다.
"""

import logging
import os
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

logger = logging.getLogger(__name__)


def get_vscode_command_path() -> Optional[str]:
    """
    VSCode의 code.cmd 실행 파일 경로를 반환합니다.
    PATH에 없으면 일반적인 설치 경로에서 찾습니다.
    
    Returns:
        Optional[str]: code.cmd의 전체 경로. 찾지 못하면 None
    """
    # 1. PATH에 등록된 code 명령 시도
    try:
        result = subprocess.run(
            ["code", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return "code"  # PATH에 있으면 "code" 반환
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # 2. PATH에 없으면 일반적인 설치 경로 확인
    # Windows에서 VSCode가 설치될 수 있는 모든 일반적인 경로 확인
    possible_paths = []
    
    # 환경 변수 기반 경로
    env_vars = {
        "LOCALAPPDATA": os.environ.get("LOCALAPPDATA", ""),
        "APPDATA": os.environ.get("APPDATA", ""),
        "ProgramFiles": os.environ.get("ProgramFiles", ""),
        "ProgramFiles(x86)": os.environ.get("ProgramFiles(x86)", ""),
        "USERPROFILE": os.environ.get("USERPROFILE", ""),
    }
    
    # 각 환경 변수에 대해 가능한 경로 생성
    for env_var, env_value in env_vars.items():
        if not env_value:
            continue
        
        base_path = Path(env_value)
        
        # Microsoft VS Code 경로들
        possible_paths.extend([
            base_path / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
            base_path / "Microsoft VS Code" / "bin" / "code.cmd",
            base_path / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
        ])
    
    # 추가 일반적인 경로들
    if platform.system() == "Windows":
        # C: 드라이브 기본 경로들
        c_drive = Path("C:/")
        possible_paths.extend([
            c_drive / "Program Files" / "Microsoft VS Code" / "bin" / "code.cmd",
            c_drive / "Program Files (x86)" / "Microsoft VS Code" / "bin" / "code.cmd",
            c_drive / "Users" / os.environ.get("USERNAME", "") / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
        ])
        
        # 다른 드라이브도 확인 (D:, E: 등)
        for drive_letter in ["D:", "E:", "F:"]:
            drive_path = Path(drive_letter)
            if drive_path.exists():
                possible_paths.extend([
                    drive_path / "Program Files" / "Microsoft VS Code" / "bin" / "code.cmd",
                    drive_path / "Program Files (x86)" / "Microsoft VS Code" / "bin" / "code.cmd",
                ])
    
    # 중복 제거 (같은 경로가 여러 번 추가될 수 있음)
    seen_paths = set()
    unique_paths = []
    for code_path in possible_paths:
        normalized_path = str(code_path.resolve()) if code_path.exists() else str(code_path)
        if normalized_path not in seen_paths:
            seen_paths.add(normalized_path)
            unique_paths.append(code_path)
    
    # 각 경로 확인
    for code_path in unique_paths:
        if code_path.exists():
            try:
                result = subprocess.run(
                    [str(code_path), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    return str(code_path)
            except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
                continue
    
    return None


def check_vscode_installed() -> bool:
    """VSCode가 설치되어 있는지 확인"""
    return get_vscode_command_path() is not None


def _check_winget_available() -> bool:
    """winget이 설치되어 있고 사용 가능한지 확인"""
    try:
        result = subprocess.run(
            ["winget", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _check_chocolatey_available() -> bool:
    """Chocolatey가 설치되어 있고 사용 가능한지 확인"""
    try:
        result = subprocess.run(
            ["choco", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _check_scoop_available() -> bool:
    """Scoop이 설치되어 있고 사용 가능한지 확인"""
    try:
        result = subprocess.run(
            ["scoop", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _install_vscode_with_winget() -> bool:
    """winget을 사용하여 VSCode 설치"""
    try:
        logger.info("  winget으로 VSCode 설치 시도 중...")
        result = subprocess.run(
            ["winget", "install", "Microsoft.VisualStudioCode", "--silent", "--accept-package-agreements", "--accept-source-agreements"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            logger.info("  ✅ VSCode 설치 완료")
            return True
        else:
            logger.warning("  ⚠️ winget 설치 실패")
            if result.stderr:
                logger.debug(f"    {result.stderr[:200]}")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"  ⚠️ winget 설치 실패: {e}")
        return False


def _install_vscode_with_chocolatey() -> bool:
    """Chocolatey를 사용하여 VSCode 설치"""
    try:
        logger.info("  Chocolatey로 VSCode 설치 시도 중...")
        result = subprocess.run(
            ["choco", "install", "vscode", "--yes"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            logger.info("  ✅ VSCode 설치 완료")
            return True
        else:
            logger.warning("  ⚠️ Chocolatey 설치 실패")
            if result.stderr:
                logger.debug(f"    {result.stderr[:200]}")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"  ⚠️ Chocolatey 설치 실패: {e}")
        return False


def _install_vscode_with_scoop() -> bool:
    """Scoop을 사용하여 VSCode 설치"""
    try:
        logger.info("  Scoop으로 VSCode 설치 시도 중...")
        result = subprocess.run(
            ["scoop", "bucket", "add", "extras"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # bucket 추가 실패해도 계속 진행
        
        result = subprocess.run(
            ["scoop", "install", "vscode"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            logger.info("  ✅ VSCode 설치 완료")
            return True
        else:
            logger.warning("  ⚠️ Scoop 설치 실패")
            if result.stderr:
                logger.debug(f"    {result.stderr[:200]}")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        logger.warning(f"  ⚠️ Scoop 설치 실패: {e}")
        return False


def _install_vscode_download() -> bool:
    """VSCode 다운로드 및 설치 (PowerShell 사용)"""
    try:
        current_platform = platform.system()
        if current_platform != "Windows":
            logger.error(f"  ❌ 이 함수는 Windows에서만 동작합니다. 현재 플랫폼: {current_platform}")
            logger.debug(f"  플랫폼 정보: {platform.platform()}")
            logger.debug(f"  Python 버전: {platform.python_version()}")
            return False
        
        logger.info("  VSCode 다운로드 및 설치 시도 중...")
        
        # VSCode 다운로드 URL
        vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
        installer_path = str(Path(tempfile.gettempdir()) / "VSCodeSetup.exe")
        
        # PowerShell 명령어로 다운로드 및 설치 (dedent 사용)
        import textwrap
        ps_script = textwrap.dedent(f"""
            $url = "{vscode_url}"
            $outfile = "{installer_path}"
            Invoke-WebRequest -Uri $url -OutFile $outfile
            Start-Process -FilePath $outfile -ArgumentList "/VERYSILENT /NORESTART" -Wait
            Remove-Item -Path $outfile -Force -ErrorAction SilentlyContinue
        """)
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=600,
        )
        
        if result.returncode == 0:
            logger.info("  PowerShell 설치 프로세스 완료")
            
            # PATH 새로고침을 위해 잠시 대기
            logger.info("  설치 확인 중...")
            time.sleep(3)  # PATH 새로고침 및 설치 완료 대기
            
            # VSCode 설치 확인 (최대 5회 재시도)
            max_retries = 5
            retry_delay = 2  # 초
            
            for attempt in range(max_retries):
                if check_vscode_installed():
                    # 버전 정보 가져오기
                    try:
                        version_result = subprocess.run(
                            ["code", "--version"],
                            capture_output=True,
                            text=True,
                            timeout=5,
                        )
                        if version_result.returncode == 0 and version_result.stdout:
                            version_line = version_result.stdout.strip().split('\n')[0]
                            logger.info(f"  ✅ VSCode 설치 확인 완료 (버전: {version_line})")
                        else:
                            logger.info("  ✅ VSCode 설치 확인 완료")
                    except Exception as e:
                        logger.debug(f"  버전 정보 가져오기 실패: {e}")
                        logger.info("  ✅ VSCode 설치 확인 완료")
                    
                    return True
                else:
                    if attempt < max_retries - 1:
                        logger.debug(f"  설치 확인 실패, 재시도 {attempt + 1}/{max_retries - 1}...")
                        time.sleep(retry_delay)
                    else:
                        logger.warning("  ⚠️ VSCode 설치 프로세스는 완료되었지만, 설치 확인에 실패했습니다.")
                        logger.info("  PATH를 새로고침하거나 새 터미널을 열어주세요.")
                        logger.info("  또는 'code --version' 명령어를 직접 실행하여 확인하세요.")
                        
                        # 설치 파일이 실제로 설치되었는지 확인 (Windows 레지스트리 또는 파일 시스템)
                        try:
                            # VSCode 기본 설치 경로 확인
                            possible_paths = [
                                Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
                                Path(os.environ.get("ProgramFiles", "")) / "Microsoft VS Code" / "bin" / "code.cmd",
                                Path(os.environ.get("ProgramFiles(x86)", "")) / "Microsoft VS Code" / "bin" / "code.cmd",
                            ]
                            
                            installed = False
                            for code_path in possible_paths:
                                if code_path.exists():
                                    logger.info(f"  VSCode 설치 파일 발견: {code_path}")
                                    installed = True
                                    break
                            
                            if installed:
                                logger.info("  VSCode는 설치되었지만 PATH에 등록되지 않았을 수 있습니다.")
                                logger.info("  새 터미널을 열거나 시스템을 재시작하면 정상 작동할 수 있습니다.")
                                return True  # 설치된 것으로 간주
                            else:
                                logger.warning("  VSCode 설치 파일을 찾을 수 없습니다.")
                                return False
                        except Exception as e:
                            logger.debug(f"  설치 파일 확인 중 오류: {e}")
                            return False
            
            return False
        else:
            logger.warning("  ⚠️ 다운로드/설치 실패")
            if result.stderr:
                logger.debug(f"    stderr: {result.stderr[:200]}")
            if result.stdout:
                logger.debug(f"    stdout: {result.stdout[:200]}")
            return False
    except Exception as e:
        logger.warning(f"  ⚠️ 다운로드/설치 실패: {e}", exc_info=True)
        return False


def ensure_vscode_installed() -> bool:
    """VSCode가 설치되어 있는지 확인하고, 없으면 설치 시도"""
    # 1. VSCode 설치 여부 확인 (리스트업 전에 확인)
    logger.info("VSCode 설치 확인 중...")
    if check_vscode_installed():
        logger.info("  ✅ VSCode가 이미 설치되어 있습니다.")
        return True
    
    # 2. 설치되어 있지 않은 경우 설치 방법 선택
    logger.warning("  ❌ VSCode가 설치되어 있지 않습니다.")
    logger.info("  VSCode 설치 방법을 선택하세요:")
    
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import (
        ensure_value_completed_2025_11_11,
    )
    
    func_n = get_caller_name()
    
    # 각 설치 방법의 종속성 확인 (리스트업 전에 확인)
    winget_available = _check_winget_available()
    chocolatey_available = _check_chocolatey_available()
    scoop_available = _check_scoop_available()
    
    # 종속성 상태에 따라 리스트 항목 구성
    install_options = []
    
    # winget 옵션
    if winget_available:
        install_options.append("winget으로 설치 (Windows 10/11, 권장)")
    else:
        install_options.append("winget으로 설치 (winget 설치 필요)")
    
    # Chocolatey 옵션
    if chocolatey_available:
        install_options.append("Chocolatey로 설치")
    else:
        install_options.append("Chocolatey로 설치 (Chocolatey 설치 필요)")
    
    # Scoop 옵션
    if scoop_available:
        install_options.append("Scoop으로 설치")
    else:
        install_options.append("Scoop으로 설치 (Scoop 설치 필요)")
    
    # PowerShell 다운로드 (PowerShell은 Windows에 기본 포함)
    install_options.append("다운로드 및 설치 (PowerShell)")
    
    # 수동 설치 안내 (항상 가능)
    install_options.append("수동 설치 안내")
    
    # 취소
    install_options.append("취소")
    
    selected_method = ensure_value_completed_2025_11_11(
        key_name="vscode_install_method",
        func_n=func_n,
        options=install_options,
        guide_text="VSCode 설치 방법을 선택하세요:",
        history_reset=True,
    )
    
    if not selected_method or selected_method == "취소":
        logger.info("  설치가 취소되었습니다.")
        logger.info("  VSCode 다운로드: https://code.visualstudio.com/download")
        return False
    
    # 선택된 방법으로 설치 시도
    success = False
    if "winget" in selected_method.lower():
        success = _install_vscode_with_winget()
    elif "chocolatey" in selected_method.lower():
        success = _install_vscode_with_chocolatey()
    elif "scoop" in selected_method.lower():
        success = _install_vscode_with_scoop()
    elif "다운로드" in selected_method or "powershell" in selected_method.lower():
        success = _install_vscode_download()
    elif "수동" in selected_method:
        logger.info("  VSCode 수동 설치 방법:")
        logger.info("    1. https://code.visualstudio.com/download 방문")
        logger.info("    2. Windows x64 버전 다운로드")
        logger.info("    3. 설치 프로그램 실행")
        logger.info("  설치 완료 후 이 함수를 다시 실행하세요.")
        return False
    
    # 설치 후 다시 확인
    if success:
        time.sleep(2)  # PATH 새로고침 대기
        
        if check_vscode_installed():
            logger.info("  ✅ VSCode 설치 및 확인 완료")
            return True
        else:
            logger.warning("  ⚠️ VSCode가 설치되었지만 아직 인식되지 않습니다.")
            logger.info("  PATH를 새로고침하거나 새 터미널을 열어주세요.")
            logger.info("  또는 'code --version' 명령어를 직접 실행하여 확인하세요.")
            return False
    
    return False
