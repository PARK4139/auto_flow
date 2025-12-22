from __future__ import annotations

import logging
import textwrap
import traceback
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_python_yeelight_installed_on_xavier import ensure_python_yeelight_installed_on_xavier # NEW IMPORT
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_remote_controller_for_xavier import get_remote_controller_for_xavier # NEW IMPORT
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def ensure_pk_yeelight_state_changed(
    yeelight_ip: str,
    state: str,  # "on", "off", "toggle"
    controller: Optional[PkRemoteTargetEngine] = None, # Added controller argument
    target_device: Optional[PkDevice] = None,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
) -> bool:
    """
    Controls the state (on/off/toggle) of a Yeelight bulb using python-yeelight
    executed on a remote Xavier machine.

    Args:
        yeelight_ip: The IP address of the Yeelight bulb.
        state: The desired state ("on", "off", "toggle").
        controller: An optional, already initialized PkRemoteTargetEngine instance.
                    If None, a new one will be created.
        target_device: The remote target device (Xavier) from which to run python-yeelight.
        target_ip: IP address of the remote target.
        target_user: Username for the remote target.
        target_pw: Password for the remote target.

    Returns:
        True if the state change command was successful, False otherwise.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 상태 변경 ({state}) 시도{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    if state not in ["on", "off", "toggle"]:
        logging.error(f"유효하지 않은 YeeLight 상태 명령어: '{state}'. 'on', 'off', 'toggle' 중 하나여야 합니다.")
        return False

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
                logging.error("Failed to get remote controller for Xavier. Aborting Yeelight control.")
                return False

        # 2. Install python-yeelight on Xavier (if not present)
        logging.info("Xavier에 python-yeelight 설치 여부를 확인합니다...")
        if not ensure_python_yeelight_installed_on_xavier(controller=controller): # Use helper function
            logging.error("python-yeelight 설치에 실패했습니다. Yeelight 제어를 중단합니다.")
            return False

        # 3. Create and execute temporary Python script on Xavier
        logging.info(f"YeeLight IP: {yeelight_ip}, 상태: {state}로 제어 스크립트를 생성 및 실행합니다.")
        temp_script_path = "/tmp/yeelight_control_script.py"
        script_content = textwrap.dedent(f"""
            import yeelight
            import sys
            import logging # Import logging to make it available in the script

            # Configure basic logging for the remote script
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

            if __name__ == "__main__":
                if len(sys.argv) < 3:
                    logging.error("Usage: python yeelight_control_script.py <yeelight_ip> <state>")
                    sys.exit(1)

                ip = sys.argv[1]
                state = sys.argv[2]

                try:
                    # Discover bulbs if IP is not known, but here IP is provided
                    # yeelight.discover_bulbs() might not be suitable for specific IP
                    bulb = yeelight.Bulb(ip)
                    # Enable power mode (might be needed for some operations, but toggle/on/off is usually enough) 
                    # bulb.set_power_mode(yeelight.PowerMode.NORMAL) 
                    
                    if state == "on":
                        bulb.turn_on()
                    elif state == "off":
                        bulb.turn_off()
                    elif state == "toggle":
                        bulb.toggle()
                    else:
                        logging.error(f"Invalid state '{{state}}' provided.")
                        sys.exit(1)

                    logging.info(f"Successfully set Yeelight at {{ip}} to {{state}}")
                    sys.exit(0)
                except yeelight.BulbException as e:
                    logging.error(f"YeeLight Bulb Exception at {{ip}}: {{e}}")
                    sys.exit(1)
                except Exception as e:
                    logging.error(f"Error controlling Yeelight at {{ip}}: {{e}}", exc_info=True)
                    sys.exit(1)
        """)

        # Upload the script
        upload_stdout, upload_stderr, upload_exit_code = controller.upload_file_to_remote(
            local_path_content=script_content, remote_path=temp_script_path
        )
        if upload_exit_code != 0:
            logging.error(f"YeeLight 제어 스크립트 업로드 실패. STDERR: {' '.join(upload_stderr)}")
            return False

        # Execute the script
        exec_cmd = f"python3 {temp_script_path} {yeelight_ip} {state}"
        exec_stdout, exec_stderr, exec_exit_code = controller.ensure_command_to_remote_target(
            cmd=exec_cmd, use_sudo=False, timeout_seconds=30
        )

        # Clean up the script
        controller.ensure_command_to_remote_target(cmd=f"rm {temp_script_path}", use_sudo=False)

        if exec_exit_code == 0:
            logging.info(f"✅ YeeLight 상태 변경 성공. STDOUT: {' '.join(exec_stdout)}")
            return True
        else:
            logging.error(f"YeeLight 상태 변경 실패. STDERR: {' '.join(exec_stderr)}")
            return False

    except Exception as e:
        logging.error(f"YeeLight 상태 변경 중 오류 발생: {e}", exc_info=True)
        ensure_debugged_verbose(traceback, e)
        return False
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}YeeLight 상태 변경 시도 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
