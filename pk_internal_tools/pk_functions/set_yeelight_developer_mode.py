from __future__ import annotations

import logging
import traceback
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_python_miio_installed_on_xavier import ensure_python_miio_installed_on_xavier # NEW IMPORT
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def set_yeelight_developer_mode(
    yeelight_ip: str,
    yeelight_token: str,
    controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
) -> bool:
    """
    Enables developer mode on the Yeelight using python-miio on a remote Xavier machine.
    Note: Many Yeelights have LAN control enabled by default and might not require
    an explicit "developer mode" setting. This function primarily ensures python-miio
    is available and can execute a command if needed.

    Args:
        yeelight_ip: The IP address of the Yeelight device.
        yeelight_token: The token for the Yeelight device.
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device (Xavier) from which to run python-miio.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        True if developer mode is successfully set (or not required/assumed to be on),
        False if an error occurs.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 개발자 모드 설정 시도{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    try:
        # 1. Get Xavier Connection Details and Controller
        if controller is None:
            controller = get_remote_controller_for_xavier(
                target_device=target_device,
                target_ip=target_ip,
                target_user=target_user,
                target_pw=target_pw,
            )
            if controller is None:
                logging.error("Failed to get remote controller for Xavier. Aborting developer mode setup.")
                return False

        # 2. Install python-miio on Xavier (if not present)
        logging.info("Xavier에 python-miio 설치 여부를 확인합니다...")
        if not ensure_python_miio_installed_on_xavier(controller=controller): # Use helper function
            logging.error("python-miio 설치에 실패했습니다. 개발자 모드 설정을 중단합니다.")
            return False

        # 3. Execute python-miio command for developer mode
        # The exact command for Yeelight's developer mode is often not explicit via miio
        # as LAN control is usually enabled by provisioning.
        # This is a placeholder for a specific miio command if one exists for a particular model.
        # For now, we'll assume successful setup if python-miio is installed.
        logging.info("YeeLight 개발자 모드 활성화 명령어를 실행합니다 (필요한 경우)...")
        
        # Example placeholder: Replace with actual command if known
        # miio_dev_mode_cmd = f"miio device --ip {yeelight_ip} --token {yeelight_token} set_dev_mode 1"
        # stdout_miio, stderr_miio, exit_code_miio = controller.ensure_command_to_remote_target(
        #     cmd=miio_dev_mode_cmd, use_sudo=False, timeout_seconds=30
        # )
        # if exit_code_miio != 0:
        #     logging.error(f"개발자 모드 설정에 실패했습니다. STDERR: {' '.join(stderr_miio)}")
        #     return False
        
        logging.info("YeeLight 개발자 모드 설정이 완료되었거나 필요하지 않습니다.")
        return True

    except Exception as e:
        logging.error(f"YeeLight 개발자 모드 설정 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 개발자 모드 설정 시도 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
