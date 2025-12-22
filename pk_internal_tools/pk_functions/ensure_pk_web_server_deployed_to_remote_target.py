import ipaddress
import logging
import traceback
from textwrap import dedent

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_remote_path_by_user_name import get_remote_path_by_user_name


def ensure_pk_web_server_deployed_to_remote_target(target_device_name: str) -> bool:
    """
    remote_target에 pk_web_server를 배포합니다.

    Args:
        target_device_name (str): remote_target 장치 이름 (예: 'JETSON_AGX_XAVIER').

    Returns:
        bool: 웹 서버 배포 명령이 성공적으로 전송되었으면 True, 아니면 False.
    """
    try:
        from pk_internal_tools.pk_functions.ensure_remote_target_debugged import ensure_remote_target_debugged
        from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
        from pk_internal_tools.pk_objects.pk_directories import D_PK_WEB_SERVER, D_PK_FUNCTIONS, D_PK_OBJECTS, D_REMOTE_PK_SYSTEM_ROOT_TEMPLATE, D_REMOTE_PK_WEB_SERVER_ROOT_TEMPLATE, D_REMOTE_PK_FUNCTIONS_TEMPLATE, D_REMOTE_PK_OBJECTS_TEMPLATE
        from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_functions.ensure_env_var_saved import ensure_env_var_saved
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
        from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine

        logging.info(f"[{target_device_name}] remote_target에 pk_web_server를 배포합니다.")

        remote_target_ip = ensure_env_var_completed(f"{target_device_name}_IP")
        remote_target_user_id = ensure_env_var_completed(f"{target_device_name}_USER")
        remote_target_user_pw = ensure_env_var_completed(f"{target_device_name}_PW")

        # remote_target_ip 유효성 검사
        try:
            ipaddress.ip_address(remote_target_ip)
        except ValueError:
            error_text = f"잘못된 IP 주소 형식입니다: {remote_target_ip}. {target_device_name}_IP 환경 변수를 확인해주세요."
            ensure_remote_target_debugged(error_text)
            return False

        if not all([remote_target_ip, remote_target_user_id, remote_target_user_pw]):
            logging.error("remote_target 연결 정보를 설정할 수 없습니다. 원격 배포를 중단합니다.")
            return False

        controller = PkRemoteTargetEngine(
            identifier=PkDevice.jetson_agx_xavier,  # TODO: 이 부분은 target_device_name에 따라 동적으로 변경될 수 있도록 수정 필요

            ip=remote_target_ip,
            user_n=remote_target_user_id,
            pw=remote_target_user_pw
        )
        logging.debug(f"Initialized PkRemoteTargetEngine with IP: {remote_target_ip}, User: {remote_target_user_id}")

        controller._ensure_sudo_nopasswd_for_user()

        # Path 객체의 / 연산자를 사용하여 경로를 정확하게 결합하고, 최종적으로 str()로 변환
        # 원격 타겟의 홈 디렉토리를 기반으로 pk_system 경로 설정
        remote_pk_system_root = get_remote_path_by_user_name(D_REMOTE_PK_SYSTEM_ROOT_TEMPLATE, controller.remote_target.user_name).as_posix()
        logging.debug(f"remote_pk_system_root (from template): {remote_pk_system_root}")
        remote_pk_web_server_root = get_remote_path_by_user_name(D_REMOTE_PK_WEB_SERVER_ROOT_TEMPLATE, controller.remote_target.user_name).as_posix()
        logging.debug(f"remote_pk_web_server_root (from template): {remote_pk_web_server_root}")
        remote_pk_functions = get_remote_path_by_user_name(D_REMOTE_PK_FUNCTIONS_TEMPLATE, controller.remote_target.user_name).as_posix()
        logging.debug(f"remote_pk_functions (from template): {remote_pk_functions}")
        remote_pk_objects = get_remote_path_by_user_name(D_REMOTE_PK_OBJECTS_TEMPLATE, controller.remote_target.user_name).as_posix()
        logging.debug(f"remote_pk_objects (from template): {remote_pk_objects}")

        # 1. remote_target에 pk_system 디렉토리 구조 생성 (필요한 경우)
        logging.info(f"remote_target에 {remote_pk_system_root} 디렉토리 구조를 생성합니다...")
        cmd_mkdir = (
            f"bash -c \""
            f"mkdir -p {remote_pk_web_server_root} && "
            f"mkdir -p {remote_pk_functions} && "
            f"mkdir -p {remote_pk_objects}"
            f"\""
        )
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=cmd_mkdir,
            timeout_seconds=30,
        )
        if exit_code != 0:
            error_text = f"#pk_error\n\nstdout={stdout}\nstderr={stderr}"
            ensure_remote_target_debugged(error_text)
            return False

        # 2. scp 설치 확인 및 설치
        logging.info("원격 타겟에 scp 설치를 확인하고 필요한 경우 설치합니다.")
        if not controller.ensure_scp_installed_at_remote_target():
            logging.error("scp 설치 또는 확인에 실패했습니다. 파일 복사를 진행할 수 없습니다.")
            return False

        # 3. pip 및 uvicorn 설치 확인 및 설치
        logging.info("원격 타겟에 python3-pip 및 uvicorn 설치를 확인하고 필요한 경우 설치합니다.")

        # python3-pip 설치 확인 및 설치
        cmd_check_pip = "dpkg -s python3-pip"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(cmd=cmd_check_pip, use_sudo=False)
        if exit_code != 0 or "Status: install ok installed" not in "\n".join(stdout):
            logging.info("python3-pip이 설치되어 있지 않아 설치를 시도합니다.")
            cmd_install_pip = "apt update && apt install -y python3-pip"
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(cmd=cmd_install_pip, timeout_seconds=120)
            if exit_code != 0:
                error_text = f"#pk_error\n\npython3-pip 설치 실패. stdout={stdout}\nstderr={stderr}"
                ensure_remote_target_debugged(error_text)
                return False
            logging.info("python3-pip 설치 완료.")
        else:
            logging.info("python3-pip이 이미 설치되어 있습니다.")

        # uvicorn 설치 확인 및 설치
        cmd_check_uvicorn = "python3 -m uvicorn --version"
        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(cmd=cmd_check_uvicorn, use_sudo=False)
        if exit_code != 0:  # uvicorn --version 명령이 실패하면 설치되어 있지 않음
            logging.info("uvicorn이 설치되어 있지 않아 설치를 시도합니다.")
            cmd_install_uvicorn = "python3 -m pip install uvicorn"
            stdout, stderr, exit_code = controller.ensure_command_to_remote_target(cmd=cmd_install_uvicorn, use_sudo=False, timeout_seconds=120)  # pip install은 sudo 필요 없음
            if exit_code != 0:
                error_text = f"#pk_error\n\nuvicorn 설치 실패. stdout={stdout}\nstderr={stderr}"
                ensure_remote_target_debugged(error_text)
                return False
            logging.info("uvicorn 설치 완료.")
        else:
            logging.info("uvicorn이 이미 설치되어 있습니다.")

                # Uvicorn 실행 파일의 절대 경로 찾기 및 저장

                logging.info("uvicorn 실행 파일의 절대 경로를 찾고 PkTarget 객체에 저장합니다.")

                

                # pip show uvicorn을 통해 설치 경로 확인

                cmd_get_pip_location = "python3 -m pip show uvicorn | grep Location"

                stdout_pip_show, stderr_pip_show, exit_code_pip_show = controller.ensure_command_to_remote_target(

                    cmd=cmd_get_pip_location, use_sudo=False, timeout_seconds=10

                )

        

                uvicorn_path = None

                if exit_code_pip_show == 0 and stdout_pip_show:

                    location_line = [line for line in stdout_pip_show if "Location:" in line]

                    if location_line:

                        pip_install_location = location_line[0].split("Location:")[1].strip()

                        # 일반적으로 파이썬 스크립트는 bin 또는 Scripts 디렉토리에 위치

                        # Linux/Unix-like 시스템에서는 bin 디렉토리에 있을 가능성이 높음

                        uvicorn_path_candidate = f"{pip_install_location}/bin/uvicorn"

                        

                        # 실제 파일 존재 여부 확인

                        cmd_check_file_exists = f"test -f {uvicorn_path_candidate} && echo 'exists'"

                        stdout_exists, _, exit_code_exists = controller.ensure_command_to_remote_target(

                            cmd=cmd_check_file_exists, use_sudo=False, timeout_seconds=5

                        )

        

                        if exit_code_exists == 0 and stdout_exists and 'exists' in stdout_exists[0]:

                            uvicorn_path = uvicorn_path_candidate

                        else:

                            # ~/.local/bin/uvicorn 과 같은 경로도 고려 (pip install --user 의 경우)

                            uvicorn_path_candidate_user = f"{controller.remote_target.get_home_directory()}/.local/bin/uvicorn"

                            cmd_check_file_exists_user = f"test -f {uvicorn_path_candidate_user} && echo 'exists'"

                            stdout_exists_user, _, exit_code_exists_user = controller.ensure_command_to_remote_target(

                                cmd=cmd_check_file_exists_user, use_sudo=False, timeout_seconds=5

                            )

                            if exit_code_exists_user == 0 and stdout_exists_user and 'exists' in stdout_exists_user[0]:

                                uvicorn_path = uvicorn_path_candidate_user

        

                if uvicorn_path:

                    logging.info(f"원격에서 Uvicorn 실행 파일 경로 확인: {uvicorn_path}")

                    controller.remote_target.uvicorn_path = uvicorn_path

                else:

                    error_text = f"#pk_error\n\nUvicorn 실행 파일 경로를 원격에서 찾을 수 없습니다. pip show uvicorn stdout={stdout_pip_show}\nstderr={stderr_pip_show}"

                    ensure_remote_target_debugged(error_text)

                    return False

        # 4. 필요한 파일들을 원격 타겟으로 복사 (scp 사용)
        logging.info("필요한 파일들을 원격 타겟으로 복사합니다 (scp 사용)...")

        # 제외할 패턴 목록
        exclude_patterns = ["__pycache__", ".pyc", ".git", ".venv", ".env", ".pytest_cache", "pk_logs", "*.log", "*.tmp"]

        remote_target_user_host = f"{controller.remote_target.user_name}@{controller.remote_target.ip}"
        logging.debug(f"remote_target_user_host: {remote_target_user_host}")

        # 'pk_web_server' 디렉토리 전체 복사
        logging.debug(f"D_PK_WEB_SERVER type: {type(D_PK_WEB_SERVER)}, value: {D_PK_WEB_SERVER}")
        if not controller.ensure_directory_transferred_to_remote_target(
                local_dir_path=D_PK_WEB_SERVER,
                remote_dir_path=f"{remote_pk_system_root}/pk_web_server",
                exclude_patterns=exclude_patterns
        ):
            error_text = f"#pk_error\n\npk_web_server 디렉토리 전송 실패."
            ensure_remote_target_debugged(error_text)
            return False

        # pk_functions 디렉토리 전체 복사
        logging.debug(f"D_PK_FUNCTIONS type: {type(D_PK_FUNCTIONS)}, value: {D_PK_FUNCTIONS}")
        if not controller.ensure_directory_transferred_to_remote_target(
                local_dir_path=D_PK_FUNCTIONS,
                remote_dir_path=f"{remote_pk_system_root}/pk_functions",
                exclude_patterns=exclude_patterns
        ):
            error_text = f"#pk_error\n\npk_functions 디렉토리 전송 실패."
            ensure_remote_target_debugged(error_text)
            return False

        # pk_objects 디렉토리 전체 복사
        logging.debug(f"D_PK_OBJECTS type: {type(D_PK_OBJECTS)}, value: {D_PK_OBJECTS}")
        if not controller.ensure_directory_transferred_to_remote_target(
                local_dir_path=D_PK_OBJECTS,
                remote_dir_path=f"{remote_pk_system_root}/pk_objects",
                exclude_patterns=exclude_patterns
        ):
            error_text = f"#pk_error\n\npk_objects 디렉토리 전송 실패."
            ensure_remote_target_debugged(error_text)
            return False

        # TODO: 필요한 기타 파일 및 디렉토리 복사 (예: __init__.py 등)
        text = dedent(f"""
            pk_web_server 배포가 완료되었습니다.
            원격 접속 정보: ssh {controller.remote_target.user_name}@{controller.remote_target.ip}
            배포 경로: {remote_pk_system_root}
        """)
        alert_as_gui(text)
        logging.info("배포 완료.")
        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
