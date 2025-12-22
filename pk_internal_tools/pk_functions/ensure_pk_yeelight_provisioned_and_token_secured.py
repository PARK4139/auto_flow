from __future__ import annotations

import logging
import traceback
from typing import Optional, Tuple # Added Tuple

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_pk_yldp06yl_provisioning_completed import ensure_pk_yldp06yl_provisioning_completed
from pk_internal_tools.pk_functions.ensure_aioiotprov_installed_on_xavier import ensure_aioiotprov_installed_on_xavier # NEW IMPORT
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

def ensure_pk_yeelight_provisioned_and_token_secured(
    controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
) -> Tuple[Optional[str], Optional[PkRemoteTargetEngine]]: # Modified return type
    """
    Ensures the Yeelight is provisioned to the home Wi-Fi and its token is secured.
    This function leverages `aioiotprov` on a remote Xavier machine.

    Args:
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device (Xavier) from which to run aioiotprov.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        A tuple of (Yeelight token as a string, PkRemoteTargetEngine instance) if
        provisioning is successful, otherwise (None, None).
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 프로비저닝 및 토큰 확보 시작{PkColors.RESET}")
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
                logging.error("Failed to get remote controller for Xavier. Aborting provisioning.")
                return None, None # Modified return value

        # 2. Get Home Wi-Fi Credentials
        home_ssid = ensure_value_completed(
            key_name="home_wifi_ssid",
            func_n=func_n,
            guide_text="Yeelight를 연결할 집 Wi-Fi SSID를 입력하세요:",
        )
        home_password = ensure_value_completed(
            key_name="home_wifi_password",
            func_n=func_n,
            guide_text="집 Wi-Fi 비밀번호를 입력하세요:",
            secret=True,
        )

        if not all([home_ssid, home_password]):
            logging.error("Home Wi-Fi credentials not provided. Aborting provisioning.")
            return None, controller # Modified return value

        # 3. Ensure Yeelight AP is up
        logging.info("YeeLight AP 모드 활성화 여부를 확인합니다...")
        if not ensure_pk_yldp06yl_provisioning_completed(
            controller=controller, # Pass the controller
            # target_device, target_ip, target_user, target_pw are now handled by get_remote_controller_for_xavier
        ):
            logging.error("YeeLight AP 모드 확인에 실패했습니다. 프로비저닝을 중단합니다.")
            return None, controller # Modified return value

        # 4. Ensure aioiotprov is installed on Xavier
        logging.info("Xavier에 aioiotprov 설치 여부를 확인합니다...")
        if not ensure_aioiotprov_installed_on_xavier(controller=controller): # Use helper function
            logging.error("aioiotprov 설치에 실패했습니다. 프로비저닝을 중단합니다.")
            return None, controller # Modified return value

        # 5. Run aioiotprov on Xavier
        logging.info("Xavier에서 aioiotprov를 실행하여 YeeLight 프로비저닝을 시도합니다...")
        aioiotprov_cmd = f"python3 -m aioiotprov '{home_ssid}' '{home_password}'"
        stdout_prov, stderr_prov, exit_code_prov = controller.ensure_command_to_remote_target(
            cmd=aioiotprov_cmd, use_sudo=False, timeout_seconds=120 # Provisioning can take time
        )

        if exit_code_prov != 0:
            logging.error(f"aioiotprov 프로비저닝에 실패했습니다. STDERR: {' '.join(stderr_prov)}")
            return None, controller # Modified return value
        logging.info("aioiotprov 프로비저닝 실행 완료.")

        # 6. Retrieve Token from ~/.aioyeelight
        logging.info("Xavier에서 YeeLight 토큰 파일을 확인합니다 (~/.aioyeelight)...")
        read_token_cmd = "cat ~/.aioyeelight"
        stdout_token, stderr_token, exit_code_token = controller.ensure_command_to_remote_target(
            cmd=read_token_cmd, use_sudo=False, timeout_seconds=10
        )

        if exit_code_token == 0 and stdout_token:
            token_content = "".join(stdout_token).strip()
            if token_content:
                logging.info("✅ YeeLight 토큰 확보 성공.")
                return token_content, controller # Modified return value
            else:
                logging.error("YeeLight 토큰 파일이 비어있습니다.")
                return None, controller # Modified return value
        else:
            logging.error(f"YeeLight 토큰 파일을 읽는 데 실패했습니다. STDERR: {' '.join(stderr_token)}")
            return None, controller # Modified return value

    except Exception as e:
        logging.error(f"YeeLight 프로비저닝 및 토큰 확보 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return None, None # Modified return value
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 프로비저닝 및 토큰 확보 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)

