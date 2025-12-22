from __future__ import annotations

import logging
import traceback
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_pk_yeelight_provisioned_and_token_secured import ensure_pk_yeelight_provisioned_and_token_secured
from pk_internal_tools.pk_functions.get_yeelight_device_details import get_yeelight_device_details
from pk_internal_tools.pk_functions.set_yeelight_developer_mode import set_yeelight_developer_mode
from pk_internal_tools.pk_functions.ensure_pk_yeelight_state_changed import ensure_pk_yeelight_state_changed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


@ensure_seconds_measured
def ensure_pk_yeelight_off(
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
) -> bool:
    """
    Orchestrates the full flow to turn a Yeelight device OFF:
    provisioning, token retrieval, IP discovery, optional developer mode setup,
    and finally, setting the state to "off".

    Args:
        target_device: The remote target device (Xavier) for operations.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        True if the Yeelight is successfully turned OFF, False otherwise.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight OFF 제어 흐름 시작{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    controller: Optional[PkRemoteTargetEngine] = None
    try:
        # 1. Get Controller
        controller = get_remote_controller_for_xavier(
            target_device=target_device,
            target_ip=target_ip,
            target_user=target_user,
            target_pw=target_pw,
        )
        if controller is None:
            logging.error("Xavier 원격 컨트롤러 확보 실패. YeeLight OFF 제어를 중단합니다.")
            return False

        # 2. Provisioning & Token Retrieval
        logging.info("YeeLight 프로비저닝 및 토큰 확보를 시도합니다...")
        yeelight_token, controller = ensure_pk_yeelight_provisioned_and_token_secured(
            controller=controller,
        )
        if not yeelight_token:
            logging.error("YeeLight 프로비저닝 또는 토큰 확보에 실패했습니다.")
            return False
        
        logging.info(f"YeeLight 토큰 확보 완료: {yeelight_token[:5]}...{yeelight_token[-5:]}")


        # 3. Device Details (IP discovery)
        logging.info("YeeLight 장치 IP 주소를 탐색합니다...")
        yeelight_details = get_yeelight_device_details(
            controller=controller,
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
            controller=controller,
        )
        if not dev_mode_success:
            logging.warning("YeeLight 개발자 모드 설정에 실패했거나 필요하지 않습니다. 계속 진행합니다.")
        

        # 5. State Change (OFF)
        logging.info(f"YeeLight ({yeelight_ip}) 상태를 'off'으로 변경 시도합니다...")
        control_success = ensure_pk_yeelight_state_changed(
            yeelight_ip=yeelight_ip,
            state="off",
            controller=controller,
        )
        if control_success:
            logging.info(f"✅ YeeLight '{yeelight_ip}' 상태를 'off'으로 성공적으로 변경했습니다.")
            return True
        else:
            logging.error(f"YeeLight '{yeelight_ip}' 상태를 'off'으로 변경하는 데 실패했습니다.")
            return False

    except Exception as e:
        logging.error(f"YeeLight OFF 제어 흐름 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight OFF 제어 흐름 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
