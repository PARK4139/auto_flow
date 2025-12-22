import logging
import subprocess
from typing import Tuple, Optional

# Lazy imports for project-specific utilities
try:
    from pk_internal_tools.pk_objects.pk_colors import PkColors
except ImportError:
    # Fallback for testing or environments where pk_colors might not be available
    PkColors = {"RED": "", "GREEN": "", "RESET": ""}


def ensure_remote_command_executed(
    remote_target: str,
    command: str,
    capture_output: bool = True,
    text: bool = True,
    check: bool = False,
    timeout: Optional[int] = None
) -> Tuple[int, str, str]:
    """
    원격 대상 서버에서 SSH를 통해 명령을 실행합니다.

    Args:
        remote_target (str): 원격 대상의 주소 (예: "user@host").
        command (str): 원격에서 실행할 명령입니다.
        capture_output (bool): True이면 stdout 및 stderr를 캡처합니다.
        text (bool): True이면 stdout 및 stderr를 텍스트로 디코딩합니다.
        check (bool): True이면 0이 아닌 종료 코드에 대해 CalledProcessError를 발생시킵니다.
        timeout (Optional[int]): 명령 실행의 최대 시간(초)입니다.

    Returns:
        Tuple[int, str, str]: 종료 코드, 표준 출력, 표준 오류를 포함하는 튜플입니다.
    """
    logging.info(f"원격 대상 '{remote_target}'에서 다음 명령을 실행 중: {command}")

    full_command = ["ssh", remote_target, command]

    try:
        result = subprocess.run(
            full_command,
            capture_output=capture_output,
            text=text,
            check=check,
            timeout=timeout,
            shell=False # 보안상의 이유로 shell=False를 권장
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        exit_code = result.returncode

        if exit_code == 0:
            logging.info(f"{PkColors.GREEN']}원격 명령 성공:{PkColors.RESET} {command}")
            if stdout:
                logging.debug(f"STDOUT:\n{stdout}")
        else:
            logging.error(f"{PkColors.RED}원격 명령 실패 (종료 코드: {exit_code}):{PkColors.RESET} {command}")
            if stdout:
                logging.error(f"STDOUT:\n{stdout}")
            if stderr:
                logging.error(f"STDERR:\n{stderr}")
        
        return exit_code, stdout, stderr

    except subprocess.CalledProcessError as e:
        logging.error(f"{PkColors.RED}원격 명령 실행 중 오류 발생 (CalledProcessError):{PkColors.RESET} {e}")
        logging.error(f"STDOUT:\n{e.stdout}")
        logging.error(f"STDERR:\n{e.stderr}")
        return e.returncode, e.stdout, e.stderr
    except subprocess.TimeoutExpired as e:
        logging.error(f"{PkColors.RED}원격 명령 시간 초과 (TimeoutExpired):{PkColors.RESET} {e}")
        return 1, e.stdout.strip(), e.stderr.strip()
    except FileNotFoundError:
        logging.error(f"{PkColors.RED}SSH 클라이언트를 찾을 수 없습니다. SSH가 PATH에 설정되어 있는지 확인하세요.{PkColors.RESET}")
        return 1, "", "SSH client not found."
    except Exception as e:
        logging.error(f"{PkColors.RED}원격 명령 실행 중 예기치 않은 오류 발생:{PkColors.RESET} {e}")
        return 1, "", str(e)
