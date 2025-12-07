import textwrap
import os
import logging
from pathlib import Path

# Lazy import for pk_files and pk_directories
try:
    from pk_internal_tools.pk_objects.pk_files import F_PK_LOG
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
except ImportError:
    # Fallback for when running outside the main project structure
    F_PK_LOG = Path(os.path.expanduser("~")) / "pk_logs" / "pk_log.log"
    d_pk_root_hidden = Path(os.path.expanduser("~")) / ".pk_system"

def ensure_wsl_script_executed_as_root(
    distro_name: str,
    script_content: str,
    script_name: str = "temp_script.sh"
) -> dict:
    """
    WSL 환경 내에서 루트 권한으로 셸 스크립트를 생성, 실행 및 정리하는 자동화된 함수.

    Args:
        distro_name (str): WSL 배포판 이름 (예: "Ubuntu-18.04").
        script_content (str): 실행할 셸 스크립트의 내용.
        script_name (str): WSL 내에서 사용할 임시 스크립트 파일 이름.

    Returns:
        dict: 실행 결과 (stdout, stderr, exit_code 등).
    """
    logging.info(f"WSL 스크립트 실행 자동화 시작: {script_name} (배포판: {distro_name})")

    # n. Windows 쪽에 임시 파일로 셸 스크립트 작성
    windows_temp_script_path = d_pk_root_hidden / script_name
    try:
        with open(windows_temp_script_path, 'w', encoding='utf-8') as f:
            f.write(textwrap.dedent(script_content).strip())
        logging.debug(f"Windows 임시 스크립트 생성 완료: {windows_temp_script_path}")
    except Exception as e:
        logging.error(f"Windows 임시 스크립트 생성 실패: {e}")
        return {"error": f"Windows 임시 스크립트 생성 실패: {e}", "exit_code": 1}

    # n. 셸 스크립트를 WSL로 복사
    wsl_temp_script_path = Path("/tmp") / script_name
    copy_command = f"wsl.exe -d {distro_name} -u root -- cp {windows_temp_script_path.as_posix()} {wsl_temp_script_path.as_posix()}"
    logging.debug(f"WSL로 스크립트 복사 명령: {copy_command}")
    copy_result = _run_wsl_command(copy_command)
    if copy_result.get("exit_code", 1) != 0:
        logging.error(f"WSL로 스크립트 복사 실패: {copy_result.get('error', '알 수 없는 오류')}")
        _cleanup_windows_temp_file(windows_temp_script_path)
        return copy_result

    # 3. 스크립트를 실행 가능하게 만들기
    chmod_command = f"wsl.exe -d {distro_name} -u root -- chmod +x {wsl_temp_script_path.as_posix()}"
    logging.debug(f"WSL 스크립트 실행 권한 부여 명령: {chmod_command}")
    chmod_result = _run_wsl_command(chmod_command)
    if chmod_result.get("exit_code", 1) != 0:
        logging.error(f"WSL 스크립트 실행 권한 부여 실패: {chmod_result.get('error', '알 수 없는 오류')}")
        _cleanup_wsl_temp_file(distro_name, wsl_temp_script_path)
        _cleanup_windows_temp_file(windows_temp_script_path)
        return chmod_result

    # 4. WSL에서 루트 권한으로 셸 스크립트 실행
    execute_command = f"wsl.exe -d {distro_name} -u root -- {wsl_temp_script_path.as_posix()}"
    logging.debug(f"WSL 스크립트 실행 명령: {execute_command}")
    execution_result = _run_wsl_command(execute_command)
    if execution_result.get("exit_code", 1) != 0:
        logging.error(f"WSL 스크립트 실행 실패: {execution_result.get('error', '알 수 없는 오류')}")
    else:
        logging.info(f"WSL 스크립트 실행 성공: {script_name}")

    # 5. 임시 파일 정리 (WSL)
    _cleanup_wsl_temp_file(distro_name, wsl_temp_script_path)

    # 6. 임시 파일 정리 (Windows)
    _cleanup_windows_temp_file(windows_temp_script_path)

    return execution_result

def _run_wsl_command(command: str) -> dict:
    """
    실제 wsl.exe 명령을 실행하는 헬퍼 함수 (default_api.run_shell_command 대체).
    """
    logging.debug(f"Executing WSL command: {command}")
    result = default_api.run_shell_command(command=command)
    return {
        "stdout": result.get("stdout", ""),
        "stderr": result.get("stderr", ""),
        "exit_code": result.get("exit_code", 1), # Default to 1 for error if not present
        "error": result.get("error", None)
    }

def _cleanup_windows_temp_file(file_path: Path):
    """Windows 임시 파일을 정리합니다."""
    try:
        if file_path.exists():
            os.remove(file_path)
            logging.debug(f"Windows 임시 파일 삭제 완료: {file_path}")
    except Exception as e:
        logging.warning(f"Windows 임시 파일 삭제 실패: {file_path} - {e}")

def _cleanup_wsl_temp_file(distro_name: str, wsl_file_path: Path):
    """WSL 임시 파일을 정리합니다."""
    rm_command = f"wsl.exe -d {distro_name} -u root -- rm {wsl_file_path.as_posix()}"
    logging.debug(f"WSL 임시 파일 삭제 명령: {rm_command}")
    _run_wsl_command(rm_command)