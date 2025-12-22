from __future__ import annotations

import logging
import traceback
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def ensure_python_yeelight_installed_on_xavier(controller: PkRemoteTargetEngine) -> bool:
    """
    Ensures that the 'python-yeelight' library is installed and up-to-date
    on the remote Xavier machine.

    Args:
        controller: An initialized PkRemoteTargetEngine instance for Xavier.

    Returns:
        True if python-yeelight is successfully installed/updated or already present, False otherwise.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}Xavier에 python-yeelight 설치/업데이트 확인{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    try:
        # 1. Check if python-yeelight is installed
        logging.info("python-yeelight 설치 여부를 확인합니다...")
        check_cmd = "pip show python-yeelight"
        stdout_check, stderr_check, exit_code_check = controller.ensure_command_to_remote_target(
            cmd=check_cmd, use_sudo=False, timeout_seconds=10
        )

        if exit_code_check != 0:
            # Not installed, try installing
            logging.warning("python-yeelight가 Xavier에 설치되어 있지 않습니다. 설치를 시도합니다...")
            install_cmd = "pip install python-yeelight"
            stdout_install, stderr_install, exit_code_install = controller.ensure_command_to_remote_target(
                cmd=install_cmd, use_sudo=False, timeout_seconds=60
            )
            if exit_code_install != 0:
                logging.error(f"python-yeelight 설치에 실패했습니다. STDERR: {' '.join(stderr_install)}")
                return False
            logging.info("✅ python-yeelight 설치 완료.")
        else:
            # Already installed, ensure it's up to date
            logging.info("python-yeelight가 이미 설치되어 있습니다. 최신 버전으로 업데이트를 시도합니다...")
            update_cmd = "pip install -U python-yeelight"
            stdout_update, stderr_update, exit_code_update = controller.ensure_command_to_remote_target(
                cmd=update_cmd, use_sudo=False, timeout_seconds=30
            )
            if exit_code_update != 0 and "not up-to-date" not in "".join(stderr_update).lower(): # Ignore "not up-to-date" for pip
                logging.warning(f"python-yeelight 업데이트에 실패했습니다. STDERR: {' '.join(stderr_update)}")
                # Continue anyway, as it's already installed
            logging.info("✅ python-yeelight 업데이트 확인 완료.")
        
        return True

    except Exception as e:
        logging.error(f"Xavier에 python-yeelight 설치/업데이트 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Xavier에 python-yeelight 설치/업데이트 확인 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
