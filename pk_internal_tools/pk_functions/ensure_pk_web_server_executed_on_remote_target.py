import logging
import traceback
from textwrap import dedent

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_objects.pk_directories import D_REMOTE_WEB_SERVER_ROOT


# Lazy import for performance and to avoid circular dependencies
def ensure_pk_web_server_executed_on_remote_target(target_device_name: str, port: int = 8000) -> bool:
    """
    remote_target에서 pk_web_server를 실행합니다.

    Args:
        target_device_name (str): remote_target 장치 이름 (예: 'JETSON_AGX_XAVIER').
        port (int): 웹 서버가 실행될 포트 번호.

    Returns:
        bool: 웹 서버 실행 명령이 성공적으로 전송되었으면 True, 아니면 False.
    """
    try:
        from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_functions.ensure_env_var_saved import ensure_env_var_saved
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
        from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine

        # 함수 내에서 로깅 초기화. 이 함수는 다른 모듈에서 임포트될 수 있기 때문에 basicConfig 대신 이 방식을 사용.
        # ensure_pk_system_log_initialized는 래퍼에서만 호출되므로 여기서 직접 설정하지 않음.
        # 이 파일은 함수 파일이므로 if __name__ == '__main__': 블록을 가지지 않습니다.

        logging.info("remote_target에서 웹 서버를 실행합니다.")
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
                logging.error("remote_target 연결 정보를 설정할 수 없습니다. 원격 실행을 중단합니다.")
                return False

        # remote_target 컨트롤러 생성
        controller = PkRemoteTargetEngine(
            identifier=PkDevice.jetson_agx_xavier,  # TODO: 이 부분은 target_device_name에 따라 동적으로 변경될 수 있도록 수정 필요
            
            ip=remote_target_ip,  # IP는 여기서 제공
            user_n=remote_target_user_id,  # 사용자명 제공
            pw=remote_target_user_pw  # 비밀번호 제공
        )

        remote_web_server_root = D_REMOTE_WEB_SERVER_ROOT  # remote_target에 배포된 웹 서버 디렉토리 경로

        try:
            logging.info(f"remote_target의 {remote_web_server_root}에서 통합 웹 서버를 시작합니다...")
            logging.info(f"서버 접속 URL: http://{remote_target_ip}:{port}")

            # 원격에서 디렉토리로 이동 후 uvicorn으로 FastAPI 앱 실행
            # app은 pk_web_server/main.py에 정의되어 있다고 가정
            # --app-dir을 사용하여 경로를 지정하거나, 직접 cd 후 실행. 여기서는 cd 후 실행 방식을 사용합니다.
            # Uvicorn 실행 파일 경로를 controller.remote_target에서 가져옵니다.
            uvicorn_executable_path = controller.remote_target.uvicorn_path
            if not uvicorn_executable_path:
                logging.error("Uvicorn 실행 파일 경로를 찾을 수 없습니다. 웹 서버 시작 불가.")
                alert_as_gui("Uvicorn 실행 파일 경로를 찾을 수 없어 웹 서버 시작 실패.")
                return False

            cmd = dedent(f"""
                cd {remote_web_server_root} && \
                nohup {uvicorn_executable_path} main:app --host 0.0.0.0 --port {port} > /tmp/pk_unified_web_server.log 2>&1 &
            """).strip()

            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
                cmd=cmd,
                timeout_seconds=10,
                use_sudo=False,
            )

            import time
            from pk_internal_tools.pk_functions.ensure_pk_web_server_status_checked_on_remote_target import ensure_pk_web_server_status_checked_on_remote_target

            if exit_code == 0:
                logging.info("웹 서버 시작 명령이 성공적으로 전송되었습니다. 서버 활성화 확인 중...")
                
                max_attempts = 10 # 2초 간격으로 10번 시도 -> 총 20초 대기
                delay_between_attempts = 2 # 초
                server_is_running = False
                
                for attempt in range(max_attempts):
                    logging.info(f"웹 서버 상태 확인 시도 중... (시도 {attempt + 1}/{max_attempts})")
                    is_running, pid = ensure_pk_web_server_status_checked_on_remote_target(target_device_name)
                    if is_running:
                        server_is_running = True
                        logging.info(f"웹 서버가 성공적으로 활성화되었습니다. PID: {pid}")
                        break
                    else:
                        logging.warning(f"웹 서버가 아직 활성화되지 않았습니다. {delay_between_attempts}초 후 다시 시도합니다.")
                        time.sleep(delay_between_attempts)
                
                if server_is_running:
                    ensure_env_var_saved(key_name="PK_WEB_SERVER_URL", value=f'http://{remote_target_ip}:{port}')
                    pk_web_server_url = ensure_env_var_completed(key_name="PK_WEB_SERVER_URL")
                    text = dedent(f"""
                        pk_web_server is started at remote_target from {remote_web_server_root}
                        url: {pk_web_server_url}
                        access: ssh {remote_target_user_id}@{remote_target_ip}
                        log checking: 'tail -f /tmp/pk_unified_web_server.log'
                        stop: 'pkill -f uvicorn main:app' (또는 프로세스 ID로)
                    """).strip()
                    alert_as_gui(text)
                    return True
                else:
                    text = "웹 서버가 지정된 시간 내에 활성화되지 않았습니다."
                    logging.error(text)
                    alert_as_gui(text)
                    return False
            else:
                text = "통합 웹 서버 시작 실패"
                logging.error(text)
                alert_as_gui(text)
                if stderr:
                    for line in stderr:
                        logging.error("  %s", line)
                return False

        except Exception as inner_e:
            ensure_debugged_verbose(traceback=traceback, e=inner_e)
            return False
    except ImportError as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False
    except Exception as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
        return False
