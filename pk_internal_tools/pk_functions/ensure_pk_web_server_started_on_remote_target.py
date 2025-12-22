from __future__ import annotations

import logging
from typing import Optional

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_remote_target_controller import (
    PkRemoteTargetEngine,
    PkModes2,
)


def ensure_pk_web_server_started_on_remote_target(
    target_device: PkDevice = PkDevice.jetson_agx_xavier,
    target_ip: Optional[str] = None,
    target_user: Optional[str] = None,
    target_pw: Optional[str] = None,
    port: int = 8000,
) -> bool:
    """
    Starts the web server on a remote target device.

    Args:
        target_device: The identifier for the target device.
        target_ip: IP address of the target. If None, it will be fetched.
        target_user: Username for the target. If None, it will be fetched.
        target_pw: Password for the target. If None, it will be fetched.
        port: The port on which the server should run.

    Returns:
        True if the server was started successfully, False otherwise.
    """
    logger = logging.getLogger(__name__)

    try:
        # --- Get Target Connection Info ---
        if not target_ip:
            target_ip = ensure_env_var_completed(f"{target_device.name.upper()}_IP")
        if not target_user:
            target_user = ensure_env_var_completed(f"{target_device.name.upper()}_USER")
        if not target_pw:
            target_pw = ensure_env_var_completed(f"{target_device.name.upper()}_PW")

        if not all([target_ip, target_user, target_pw]):
            logger.error(f"{target_device.name} 연결 정보를 가져올 수 없습니다. 서버 시작을 중단합니다.")
            return False

        # --- Initialize Controller ---
        controller = PkRemoteTargetEngine(
            identifier=target_device,
            
            ip=target_ip,
            user_n=target_user,
            pw=target_pw
        )
        logger.info(f"Initialized controller for target: {target_device.name}")

        # --- Define Command ---
        server_script_name = "pk_ensure_pk_web_server_executed_on_remote_target.py"
        remote_script_path = f"/tmp/{server_script_name}"
        
        # Define environment variables for the remote command
        env_vars = f"PK_WEB_SERVER_API_PORT={port}"
        
        # Construct the command to run the server in the background
        cmd = (
            f"nohup env {env_vars} python3 {remote_script_path} "
            f"> /tmp/pk_web_server.log 2>&1 &"
        )

        logger.info(f"원격지에서 웹 서버 시작 명령을 실행합니다: {cmd}")

        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=cmd,
            timeout_seconds=10,
            use_sudo=False,
        )

        # For nohup background commands, exit_code is often 0 even if the script fails later.
        # We rely on the absence of immediate errors.
        if exit_code == 0:
            logger.info("✅ 웹 서버 시작 명령이 성공적으로 전송되었습니다.")
            logger.info("📊 접속 URL: http://%s:%d", target_ip, port)
            logger.info("   - 로그 확인: ssh로 접속 후 'tail -f /tmp/pk_web_server.log'")
            logger.info("   - 중지 방법: 'pkill -f %s'", server_script_name)
            return True
        else:
            logger.error("웹 서버 시작 명령 실행에 실패했습니다.")
            if stderr:
                for line in stderr:
                    logger.error("  %s", line)
            return False

    except Exception as e:
        logger.error(f"웹 서버 시작 중 오류 발생: {e}", exc_info=True)
        return False
