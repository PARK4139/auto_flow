import logging
import traceback
from textwrap import dedent
from typing import Tuple, Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

# Lazy import for performance and to avoid circular dependencies
def ensure_pk_web_server_status_checked_on_remote_target(target_device_name: str) -> Tuple[bool, Optional[int]]:
    """
    remote_target에서 pk_web_server의 상태를 확인합니다.

    Args:
        target_device_name (str): remote_target 장치 이름 (예: 'JETSON_AGX_XAVIER').

    Returns:
        Tuple[bool, Optional[int]]: 웹 서버가 실행 중이면 (True, PID), 아니면 (False, None).
    """
    try:
        from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
        from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
        
        logging.info(f"[{target_device_name}] remote_target에서 pk_web_server 상태를 확인합니다.")

        remote_target_ip = ensure_env_var_completed(f"{target_device_name}_IP")
        remote_target_user_id = ensure_env_var_completed(f"{target_device_name}_USER")
        remote_target_user_pw = ensure_env_var_completed(f"{target_device_name}_PW")

        if not all([remote_target_ip, remote_target_user_id, remote_target_user_pw]):
            logging.error(f"remote_target 연결 환경 변수 ({target_device_name}_IP, {target_device_name}_USER, {target_device_name}_PW)가 설정되지 않았습니다.")
            logging.info("ensure_env_var_completed를 통해 설정합니다.")
            remote_target_ip = ensure_env_var_completed(f"{target_device_name}_IP")
            remote_target_user_id = ensure_env_var_completed(f"{target_device_name}_USER")
            remote_target_user_pw = ensure_env_var_completed(f"{target_device_name}_PW")
            if not all([remote_target_ip, remote_target_user_id, remote_target_user_pw]):
                logging.error("remote_target 연결 정보를 설정할 수 없습니다. 원격 상태 확인을 중단합니다.")
                return False, None

        controller = PkRemoteTargetEngine(
            identifier=PkDevice.jetson_agx_xavier, # TODO: 이 부분은 target_device_name에 따라 동적으로 변경될 수 있도록 수정 필요
            
            ip=remote_target_ip,
            user_n=remote_target_user_id,
            pw=remote_target_user_pw
        )
        
        # Get the web server port from environment variable
        web_server_port = ensure_env_var_completed("PK_WEB_SERVER_API_PORT")
        if not web_server_port:
            logging.error("웹 서버 포트 환경 변수 'PK_WEB_SERVER_API_PORT'가 설정되지 않았습니다. 상태 확인 불가.")
            return False, None

        # uvicorn 프로세스를 찾고, 해당 포트가 열려 있는지 확인하는 명령
        # 첫 번째 명령: uvicorn 프로세스 ID 찾기
        cmd_find_pid = "ps aux | grep 'uvicorn main:app' | grep -v grep | awk '{print $2}'"
        stdout_pid, stderr_pid, exit_code_pid = controller.ensure_command_to_remote_target(
            cmd=cmd_find_pid,
            timeout_seconds=5,
            use_sudo=False # ps aux는 sudo 필요 없음
        )
        logging.debug(f"ps aux command output: stdout={stdout_pid}, stderr={stderr_pid}, exit_code={exit_code_pid}")

        pid = None
        if stdout_pid:
            pids = [int(p.strip()) for p in stdout_pid if p.strip().isdigit()]
            if pids:
                pid = pids[0]
                logging.debug(f"uvicorn process found with PID: {pid}")
            else:
                logging.debug("uvicorn process not found.")
        else:
            logging.debug("uvicorn process not found (stdout empty).")

        # 두 번째 명령: 웹 서버 포트 리스닝 확인
        cmd_check_port = f"netstat -tuln | grep ':{web_server_port}'"
        stdout_port, stderr_port, exit_code_port = controller.ensure_command_to_remote_target(
            cmd=cmd_check_port,
            timeout_seconds=5,
            use_sudo=False # netstat는 sudo 필요 없음
        )
        logging.debug(f"netstat command output: stdout={stdout_port}, stderr={stderr_port}, exit_code={exit_code_port}")

        port_listening = False
        if stdout_port and any(f":{web_server_port}" in line for line in stdout_port):
            port_listening = True
            logging.debug(f"Web server port {web_server_port} is listening.")
        else:
            logging.debug(f"Web server port {web_server_port} is not listening.")

        if pid and port_listening:
            logging.info(f"pk_web_server가 실행 중입니다. PID: {pid}, Port: {web_server_port}")
            alert_as_gui(f"pk_web_server가 실행 중입니다. PID: {pid}, Port: {web_server_port}")
            return True, pid
        else:
            logging.info("pk_web_server가 실행 중이지 않습니다.")
            alert_as_gui("pk_web_server가 실행 중이지 않습니다.")
            return False, None

    except ImportError as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False, None
    except Exception as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False, None
