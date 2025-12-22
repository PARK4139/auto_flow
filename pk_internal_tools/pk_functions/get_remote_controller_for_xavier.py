from __future__ import annotations

import logging
import traceback
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def get_remote_controller_for_xavier(
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
) -> Optional[PkRemoteTargetEngine]:
    """
    Ensures connection details for the remote Xavier are available and
    returns an initialized PkRemoteTargetEngine instance.

    Args:
        target_device: The remote target device (Xavier). Defaults to jetson_agx_xavier.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        An initialized PkRemoteTargetEngine instance, or None on failure.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}Xavier 원격 컨트롤러 초기화 시도{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    try:
        if target_device is None:
            target_device = PkDevice.jetson_agx_xavier 
            logging.debug(f"Defaulting remote target to: {target_device.value}")

        target_device_upper_name = target_device.name.upper()
        if not target_ip:
            target_ip = ensure_env_var_completed(key_name=f"{target_device_upper_name}_IP")
        if not target_user:
            target_user = ensure_env_var_completed(key_name=f"{target_device_upper_name}_USER")
        if not target_pw:
            target_pw = ensure_env_var_completed(key_name=f"{target_device_upper_name}_PW")

        if not all([target_ip, target_user, target_pw]):
            logging.error(f"Connection info for {target_device.value} is incomplete. Aborting controller initialization.")
            return None

        controller = PkRemoteTargetEngine(
            identifier=target_device,
            ip=target_ip,
            user_n=target_user,
            pw=target_pw
        )
        logging.info(f"✅ Xavier 원격 컨트롤러 초기화 성공: {target_device.value}")
        return controller

    except Exception as e:
        logging.error(f"Xavier 원격 컨트롤러 초기화 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return None
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Xavier 원격 컨트롤러 초기화 시도 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
