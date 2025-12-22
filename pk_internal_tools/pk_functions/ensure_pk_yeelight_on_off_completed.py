from __future__ import annotations

import logging
import traceback
from typing import Optional, Tuple # Added Tuple

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_pk_yeelight_provisioned_and_token_secured import ensure_pk_yeelight_provisioned_and_token_secured
from pk_internal_tools.pk_functions.get_yeelight_device_details import get_yeelight_device_details
from pk_internal_tools.pk_functions.set_yeelight_developer_mode import set_yeelight_developer_mode
from pk_internal_tools.pk_functions.ensure_pk_yeelight_state_changed import ensure_pk_yeelight_state_changed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine # NEW IMPORT (for type hint)
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


@ensure_seconds_measured
def ensure_pk_yeelight_on_off_completed(
    controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
    action: Optional[str] = None, # "on", "off", "toggle"
) -> bool:
    """
    Orchestrates the full flow for Yeelight control: provisioning, token retrieval,
    IP discovery, optional developer mode setup, and state change (on/off/toggle).
    Acts as an interactive interface for selecting actions.

    Args:
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device (Xavier) for operations.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.
        action: The desired state change action for the Yeelight ("on", "off", "toggle").
                If None, the user will be prompted.

    Returns:
        True if the Yeelight control operation is successful, False otherwise.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 통합 제어 흐름 시작{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    try:
        # 1. Get Controller
        if controller is None:
            controller = get_remote_controller_for_xavier(
                target_device=target_device,
                target_ip=target_ip,
                target_user=target_user,
                target_pw=target_pw,
            )
            if controller is None:
                logging.error("Xavier 원격 컨트롤러 확보 실패. YeeLight 통합 제어를 중단합니다.")
                return False

        # 2. Provisioning & Token Retrieval
        logging.info("YeeLight 프로비저닝 및 토큰 확보를 시도합니다...")
        yeelight_token, controller = ensure_pk_yeelight_provisioned_and_token_secured(
            controller=controller, # Pass the controller
            target_device=target_device, # Kept for standalone, get_remote_controller_for_xavier handles it
            target_ip=target_ip,
            target_user=target_user,
            target_pw=target_pw,
        )
        if not yeelight_token:
            logging.error("YeeLight 프로비저닝 또는 토큰 확보에 실패했습니다.")
            return False
        
        logging.info(f"YeeLight 토큰 확보 완료: {yeelight_token[:5]}...{yeelight_token[-5:]}")


        # 3. Device Details (IP discovery)
        logging.info("YeeLight 장치 IP 주소를 탐색합니다...")
        yeelight_details = get_yeelight_device_details(
            controller=controller, # Pass the controller
            target_device=target_device, # Kept for standalone, get_remote_controller_for_xavier handles it
            target_ip=target_ip,
            target_user=target_user,
            target_pw=target_pw,
        )
        if not yeelight_details or not yeelight_details.get("ip"):
            logging.error("YeeLight 장치 IP 주소 탐색에 실패했습니다.")
            return False
        
        yeelight_ip = yeelight_details["ip"]
        yeelight_mac = yeelight_details.get("mac", "N/A")
        logging.info(f"YeeLight 장치 발견: IP={yeelight_ip}, MAC={yeelight_mac}")


        # 4. Developer Mode (Optional)
        logging.info("YeeLight 개발자 모드 설정을 시도합니다 (선택 사항)...")
        dev_mode_success = set_yeelight_developer_mode(
            yeelight_ip=yeelight_ip,
            yeelight_token=yeelight_token,
            controller=controller, # Pass the controller
            target_device=target_device, # Kept for standalone, get_remote_controller_for_xavier handles it
            target_ip=target_ip,
            target_user=target_user,
            target_pw=target_pw,
        )
        if not dev_mode_success:
            logging.warning("YeeLight 개발자 모드 설정에 실패했거나 필요하지 않습니다. 계속 진행합니다.")
        

        # 5. User Action Selection
        if action is None:
            logging.info("YeeLight에 수행할 액션을 사용자에게 요청합니다.")
            if QC_MODE:
                action = "on" # Default action for QC_MODE
            else:
                action = ensure_value_completed(
                    key_name="yeelight_action",
                    func_n=func_n,
                    guide_text="YeeLight에 수행할 액션을 선택하세요:",
                    options=["on", "off", "toggle"],
                    default_value="on"
                )
            if not action:
                logging.warning("액션이 선택되지 않아 작업을 종료합니다.")
                return False
        
        if action not in ["on", "off", "toggle"]:
            logging.error(f"유효하지 않은 액션 '{action}'이 선택되었습니다. 작업을 종료합니다.")
            return False

        # 6. State Change
        logging.info(f"YeeLight ({yeelight_ip}) 상태를 '{action}'으로 변경 시도합니다...")
        control_success = ensure_pk_yeelight_state_changed(
            yeelight_ip=yeelight_ip,
            state=action,
            controller=controller, # Pass the controller
            target_device=target_device, # Kept for standalone, get_remote_controller_for_xavier handles it
            target_ip=target_ip,
            target_user=target_user,
            target_pw=target_pw,
        )
        if control_success:
            logging.info(f"✅ YeeLight '{yeelight_ip}' 상태를 '{action}'으로 성공적으로 변경했습니다.")
            return True
        else:
            logging.error(f"YeeLight '{yeelight_ip}' 상태를 '{action}'으로 변경하는 데 실패했습니다.")
            return False

    except Exception as e:
        logging.error(f"YeeLight 통합 제어 흐름 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 통합 제어 흐름 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
