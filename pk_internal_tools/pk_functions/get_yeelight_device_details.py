from __future__ import annotations

import logging
import re
import time
import traceback
from typing import Optional, Dict, Any

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


# Constants for Yeelight discovery
IP_NEIGH_PATTERN = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+dev\s+\S+\s+lladdr\s+([0-9a-fA-F:]{17})")
YEELIGHT_MAC_PREFIX = "04:cf:8c"  # Common MAC prefix for Yeelight devices
MAX_RETRIES = 10
RETRY_DELAY_SECONDS = 5


def get_yeelight_device_details(
    controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
) -> Optional[Dict[str, str]]:
    """
    Discovers the IP and MAC address of a provisioned Yeelight device on the network
    by scanning from a remote Xavier machine.

    Args:
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device (Xavier) to scan from.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        A dictionary containing "ip" and "mac" of the Yeelight, or None if not found.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 장치 정보 탐색 시작{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    try:
        if controller is None:
            controller = get_remote_controller_for_xavier(
                target_device=target_device,
                target_ip=target_ip,
                target_user=target_user,
                target_pw=target_pw,
            )
            if controller is None:
                logging.error("Failed to get remote controller for Xavier. Aborting discovery.")
                return None

        # 2. Scan Network for Yeelight
        logging.info(f"Xavier에서 'ip neigh' 명령어를 사용하여 YeeLight ({YEELIGHT_MAC_PREFIX}...)를 탐색합니다.")
        retries = 0
        while retries < MAX_RETRIES:
            logging.debug(f"Discovery attempt {retries + 1}/{MAX_RETRIES}...")
            stdout_neigh, stderr_neigh, exit_code_neigh = controller.ensure_command_to_remote_target(
                cmd="ip neigh", use_sudo=False, timeout_seconds=10
            )

            if exit_code_neigh != 0:
                logging.warning(f"'ip neigh' 명령어 실행 실패. STDERR: {' '.join(stderr_neigh)}")
                # Continue retrying, network might be unstable
            
            if stdout_neigh:
                for line in stdout_neigh:
                    match = IP_NEIGH_PATTERN.search(line)
                    if match:
                        ip_addr = match.group(1)
                        mac_addr = match.group(2).lower()
                        if mac_addr.startswith(YEELIGHT_MAC_PREFIX):
                            logging.info(f"✅ YeeLight 장치 발견: IP={ip_addr}, MAC={mac_addr}")
                            return {"ip": ip_addr, "mac": mac_addr}
            
            logging.debug(f"YeeLight 장치 미발견. {RETRY_DELAY_SECONDS}초 후 재시도합니다.")
            time.sleep(RETRY_DELAY_SECONDS)
            retries += 1
        
        logging.error(f"지정된 재시도 횟수 ({MAX_RETRIES}회) 동안 YeeLight 장치를 찾을 수 없습니다.")
        return None

    except Exception as e:
        logging.error(f"YeeLight 장치 정보 탐색 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return None
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 장치 정보 탐색 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
