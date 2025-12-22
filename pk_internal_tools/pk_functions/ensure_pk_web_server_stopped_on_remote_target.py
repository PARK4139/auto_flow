import logging
import traceback
from textwrap import dedent
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

# Lazy import for performance and to avoid circular dependencies
def ensure_pk_web_server_stopped_on_remote_target(target_device_name: str) -> bool:
    """
    remote_target에서 pk_web_server를 중지합니다.

    Args:
        target_device_name (str): remote_target 장치 이름 (예: 'JETSON_AGX_XAVIER').

    Returns:
        bool: 웹 서버 중지 명령이 성공적으로 전송되었으면 True, 아니면 False.
    """
    try:
        from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
        from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
        from pk_internal_tools.pk_functions.ensure_pk_web_server_status_checked_on_remote_target import ensure_pk_web_server_status_checked_on_remote_target
        
        logging.info(f"[{target_device_name}] remote_target에서 pk_web_server를 중지합니다.")

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
                logging.error("remote_target 연결 정보를 설정할 수 없습니다. 원격 중지를 중단합니다.")
                return False

        controller = PkRemoteTargetEngine(
            identifier=PkDevice.jetson_agx_xavier, # TODO: 이 부분은 target_device_name에 따라 동적으로 변경될 수 있도록 수정 필요
            
            ip=remote_target_ip,
            user_n=remote_target_user_id,
            pw=remote_target_user_pw
        )
        
        # 먼저 서버가 실행 중인지 확인하고 PID를 얻습니다.
        is_running, pid = ensure_pk_web_server_status_checked_on_remote_target(target_device_name)

        if is_running and pid:
            # PID를 사용하여 프로세스 종료
            cmd_stop = f"kill {pid}"
            logging.info(f"PID {pid}를 사용하여 pk_web_server 프로세스를 종료합니다.")
        else:
            # PID를 찾을 수 없거나 실행 중이 아니면 pkill 시도
            cmd_stop = "pkill -f 'uvicorn main:app'"
            logging.info("pk_web_server 프로세스를 찾을 수 없거나 실행 중이지 않아 pkill을 시도합니다.")

        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=cmd_stop,
            timeout_seconds=10
        )

        if exit_code == 0:
            logging.info("pk_web_server 중지 명령이 성공적으로 전송되었습니다.")
            alert_as_gui("pk_web_server가 remote_target에서 성공적으로 중지되었습니다.")
            return True
        else:
            logging.error(f"pk_web_server 중지 실패: {stderr}")
            alert_as_gui(f"pk_web_server 중지 실패: {stderr}")
            return False

    except ImportError as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False
    except Exception as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False
