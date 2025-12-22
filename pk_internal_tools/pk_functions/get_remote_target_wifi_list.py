from __future__ import annotations

import logging
from typing import Optional, List

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine

def get_remote_target_wifi_list(
        controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
        target_device: Optional[PkDevice] = None,
        target_ip: Optional[str] = None,
        target_user: Optional[str] = None,
        target_pw: Optional[str] = None,
) -> Optional[List[str]]:
    """
    Gets the Wi-Fi list from a remote target device.

    Args:
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device (e.g., PkDevice.jetson_agx_xavier). Prompts user if None.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        A list of strings representing the stdout of the wifi list command, or None on failure.
    """
    func_n = get_caller_name()

    try:
        if controller is None:
            # If no controller is provided, try to create one
            controller = get_remote_controller_for_xavier(
                target_device=target_device,
                target_ip=target_ip,
                target_user=target_user,
                target_pw=target_pw,
            )
            if controller is None:
                logging.error("Failed to get remote controller for Xavier. Aborting Wi-Fi list retrieval.")
                return None

        wifi_command = "nmcli device wifi list"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=wifi_command, use_sudo=False, timeout_seconds=15
        )

        if exit_code == 0 and stdout:
            return stdout
        else:
            logging.error(f"Failed to get Wi-Fi list from {controller.identifier.value}.")
            if stderr:
                for line in stderr:
                    logging.error(f"  STDERR: {line}")
            return None

    except Exception as e:
        logging.error(f"Error getting remote Wi-Fi list: {e}", exc_info=True)
        return None
