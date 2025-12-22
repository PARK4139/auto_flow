from __future__ import annotations

import logging
from typing import Optional

from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_remote_target_wifi_list import get_remote_target_wifi_list
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine # NEW IMPORT (for type hint)


def ensure_pk_yldp06yl_provisioning_completed(
        controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
        target_device: Optional[PkDevice] = None,
        target_ip: Optional[str] = None,
        target_user: Optional[str] = None,
        target_pw: Optional[str] = None,
) -> bool:
    """
    Scans for a YeeLink device's provisioning Wi-Fi on a remote target and
    guides the user to put the device into provisioning mode if not found.

    Args:
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device to scan from. Defaults to jetson_agx_xavier.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        True if the provisioning SSID is found, False otherwise.
    """
    func_n = get_caller_name()
    provisioning_ssid = "yeelink-light-color2_miap998d"

    while True:
        logging.info(f"Scanning for '{provisioning_ssid}' on remote target...")
        
        # If controller is not provided, create one
        if controller is None:
            controller = get_remote_controller_for_xavier(
                target_device=target_device,
                target_ip=target_ip,
                target_user=target_user,
                target_pw=target_pw,
            )
            if controller is None:
                logging.error("Failed to get remote controller for Xavier. Aborting provisioning check.")
                return False

        wifi_list = get_remote_target_wifi_list(
            controller=controller, # Pass the controller
            # target_device, target_ip, target_user, target_pw are now handled by get_remote_controller_for_xavier if controller is None
        )

        if wifi_list is None:
            logging.error("Could not retrieve Wi-Fi list. Aborting provisioning.")
            return False

        found_device = False
        for line in wifi_list:
            if provisioning_ssid in line:
                logging.info(f"✅ Found provisioning SSID: {line.strip()}")
                found_device = True
                break
        
        if found_device:
            logging.info("Device is ready for provisioning.")
            return True
        else:
            logging.warning(f"'{provisioning_ssid}' not found in Wi-Fi scan.")
            user_choice = ensure_value_completed(
                key_name="yldp06yl_provisioning_retry",
                func_n=func_n,
                guide_text="YeeLink 조명을 5번 껐다 켰다 하여 프로비저닝 모드로 설정하세요.\n"
                           "완료 후 '다시 스캔'을 선택하거나, '취소'를 선택하세요.",
                options=['다시 스캔', '취소'],
            )

            if user_choice == '취소':
                logging.info("Provisioning cancelled by user.")
                return False
            # Otherwise, the loop will continue and rescan.

