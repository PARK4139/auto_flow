import json
import logging

from pk_internal_tools.pk_functions import ensure_value_completed
from pk_internal_tools.pk_objects.pk_identifier import PkIdentifier, PkDevice
from pk_internal_tools.pk_objects.pk_target import PkTarget
from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForPkWirelessTargetController


class PkWirelessTargetController(PkIdentifier):
    wireless_target: PkTarget = None
    _sudo_nopasswd_ready: bool = False

    def __init__(self, identifier: "PkDevice" = PkDevice.undefined, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None, setup_op: "SetupOpsForPkWirelessTargetController" = SetupOpsForPkWirelessTargetController.INITIALIZE_NONE):
        import logging

        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified

        super().__init__(identifier)

        self.window_title_temp = get_window_title_temp_identified(__file__)
        self._setup_op = setup_op
        self._init_kwargs = dict(ip=ip, pw=pw, hostname=hostname, port=port, user_n=user_n, f_local_ssh_public_key=f_local_ssh_public_key, f_local_ssh_private_key=f_local_ssh_private_key, nick_name=nick_name)
        self.ensure_executed_by_setup_op(setup_op, **self._init_kwargs)

        # Initialize PkWslController if WSL_DISTRO setup is requested

        self._ssh_client = None
        self._sftp_client = None
        self._connect()  # Automatically connect on initialization

        logging.debug(f'{get_caller_name()} is initialized')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()

    def _disconnect(self):
        import logging

        if self._sftp_client:
            self._sftp_client.close()
            self._sftp_client = None
            logging.debug("SFTP client disconnected.")
        if self._ssh_client:
            self._ssh_client.close()
            self._ssh_client = None
            logging.debug("SSH client disconnected.")

    def _connect(self, max_retries=5, retry_delay_seconds=5):
        import logging
        import time

        import paramiko

        if self._ssh_client:
            # Check if the connection is still active
            try:
                if self._ssh_client.get_transport() and self._ssh_client.get_transport().is_active():
                    logging.debug("SSH connection is already active.")
                    return
            except Exception as e:
                logging.warning(f"SSH connection check failed: {e}. Reconnecting...")
                self._disconnect()

        self._ssh_client = paramiko.SSHClient()
        self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for attempt in range(max_retries):
            connected = False
            # n. Try public key authentication
            try:
                if self.wireless_target and self.wireless_target.f_local_ssh_private_key:
                    logging.info(f"Attempting SSH connection with public key (Attempt {attempt + 1}/{max_retries})...")
                    key = paramiko.Ed25519Key(filename=self.wireless_target.f_local_ssh_private_key)
                    self._ssh_client.connect(hostname=self.wireless_target.ip, port=self.wireless_target.port, username=self.wireless_target.user_name, pkey=key, timeout=10)
                    connected = True
                    logging.info("SSH connection successful with public key.")
                else:
                    logging.debug("Private key not provided, skipping public key authentication.")
            except Exception as e:
                logging.warning(f"Public key authentication failed: {e}")

            # n. Fallback to password authentication
            if not connected:
                try:
                    if self.wireless_target and self.wireless_target.pw:
                        logging.info(f"Attempting SSH connection with password (Attempt {attempt + 1}/{max_retries})...")
                        self._ssh_client.connect(hostname=self.wireless_target.ip, port=self.wireless_target.port, username=self.wireless_target.user_name, password=self.wireless_target.pw, timeout=10)
                        connected = True
                        logging.info("SSH connection successful with password.")
                    else:
                        logging.debug("Password not provided, skipping password authentication.")
                except Exception as e:
                    logging.warning(f"Password authentication failed: {e}")

            if connected:
                return  # Exit loop on success

            if attempt < max_retries - 1:
                logging.warning(f"SSH connection failed. Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)

        # If all retries fail
        self._ssh_client = None  # Ensure client is None if connection failed
        logging.error("All SSH connection attempts failed.")
        raise ConnectionError("Failed to connect to SSH target after multiple retries.")

    def ensure_executed_by_setup_op(self, setup_ops: "SetupOpsForPkWirelessTargetController", *, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None):
        import logging

        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForPkWirelessTargetController

        if setup_ops & SetupOpsForPkWirelessTargetController.SELF:
            self.set_self(
                ip=ip, pw=pw, hostname=hostname, port=port, user_n=user_n,
                f_local_ssh_public_key=f_local_ssh_public_key,
                f_local_ssh_private_key=f_local_ssh_private_key,
                nick_name=nick_name,
            )
            logging.debug("set_self() done")

        if setup_ops & SetupOpsForPkWirelessTargetController.TARGET:
            # 기존 로직: identifier가 기본 WSL이면 target 설정 생략
            if not self.identifier == PkDevice.undefined:
                self.set_wireless_target()
                logging.debug("set_target() done")
            else:
                logging.debug("set_target() skipped for wsl_distro_default")

    def set_self(self, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None):
        self.ip = ip
        self.pw = pw
        self.hostname = hostname
        self.port = port
        self.user_n = user_n
        self.f_local_ssh_public_key = f_local_ssh_public_key
        self.f_local_ssh_private_key = f_local_ssh_private_key
        self.nick_name = nick_name

    def ensure_wireless_target_distro_package_installed(self, distro_package_name):
        import logging

        from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
        from pk_internal_tools.pk_functions.ensure_signature_found_in_lines import ensure_signature_found_in_lines
        from pk_internal_tools.pk_functions.ensure_general_ubuntu_pkg import ensure_general_ubuntu_pkg
        from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21

        # TODO : windows/linux 에 따라 다르게 구현 필요.
        #  distro_pkg_n 는 windows 라면 application_name

        if not is_internet_connected_2025_10_21():
            logging.debug(f'''can not install ubuntu pakage ({distro_package_name}) for internet not connected  ''')
            raise
        if distro_package_name == 'docker':
            std_outs, std_errs = self.ensure_command_to_wireless_target(cmd='docker --version')
            if std_outs is None:  # Added check for None
                logging.error(f"Failed to get docker version from remote OS. SSH connection might be down.")
                return False
            if ensure_signature_found_in_lines(signature="The cmd 'docker' could not be found", lines=std_outs):
                logging.debug("docker is not installed in wsl")
                self.ensure_wireless_target_distro_docker_installed()
        elif distro_package_name == 'net-tools':
            ensure_not_prepared_yet_guided()
        else:
            # std_outs, std_errs = ensure_command_to_remote_os_with_pubkey(cmd=f'{ubuntu_pkg_n} --version')
            std_outs, std_errs = self.ensure_command_to_wireless_target(cmd=f'sudo apt list --installed | grep {distro_package_name}')
            if std_outs is None:
                logging.error(f"Failed to list installed packages for {distro_package_name} from remote OS. SSH connection might be down.")
                return False
            if ensure_signature_found_in_lines(signature='installed', lines=std_outs):
                logging.debug(f"{distro_package_name} is installed in {self.wireless_target.distro_name}")
                ensure_general_ubuntu_pkg(ubuntu_pkg_n=distro_package_name)
        return True

    def ensure_command_to_wireless_target_with_pubkey(self, cmd):
        import logging
        import traceback

        import paramiko

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

        if not self.wireless_target or not self.wireless_target.ip:
            logging.error("Target is not properly configured. IP address is missing.")
            return None, ["Target not configured"]

        logging.debug(
            f"Attempting to execute command on target:\n"
            f"  - Host: {self.wireless_target.ip}:{self.wireless_target.port}\n"
            f"  - User: {self.wireless_target.user_name}\n"
            f"  - Command: {cmd}"
        )

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False

        # n. 공개 키 인증 시도
        try:
            if self.wireless_target.f_local_ssh_private_key:
                logging.info("SSH 공개 키로 연결을 시도합니다...")
                key_private = paramiko.Ed25519Key(filename=self.wireless_target.f_local_ssh_private_key)
                ssh.connect(hostname=self.wireless_target.ip, port=self.wireless_target.port, username=self.wireless_target.user_name, pkey=key_private, timeout=10)
                connected = True
                logging.info("SSH 공개 키로 연결에 성공했습니다.")
            else:
                logging.warning("SSH 비공개 키가 제공되지 않았습니다.")
        except Exception as e:
            logging.warning(f"SSH 공개 키 인증에 실패했습니다: {e}")

        # n. 키 인증 실패 시 암호 인증으로 대체
        if not connected and self.wireless_target.pw:
            try:
                logging.info("SSH 암호로 연결을 시도합니다...")
                ssh.connect(hostname=self.wireless_target.ip, port=self.wireless_target.port, username=self.wireless_target.user_name, password=self.wireless_target.pw, timeout=10)
                connected = True
                logging.info("SSH 암호로 연결에 성공했습니다.")
            except Exception as e:
                logging.error(f"SSH 암호 인증도 실패했습니다: {e}")

        if not connected:
            logging.error("모든 SSH 인증 방법에 실패했습니다.")
            ensure_debug_loged_verbose(traceback)
            logging.error("SSH 연결에 실패했습니다. 다음 사항을 확인해 주십시오:")
            logging.error(r"1. 대상 장치의 IP 주소, 사용자 이름, 포트가 정확한지 확인하십시오.")
            logging.error(r"2. 대상 장치에서 SSH 서버가 실행 중인지 확인하십시오.")
            logging.error(r"3. 방화벽이 SSH 포트(기본 22) 연결을 차단하지 않는지 확인하십시오.")
            logging.error(r"4. 공개 키 인증의 경우, 공개 키가 대상의 `~/.ssh/authorized_keys`에 올바르게 등록되었는지 확인하십시오.")
            logging.error(r"5. 암호 인증의 경우, 암호가 정확한지 확인하십시오.")
            return None, ["SSH connection failed"]

        # 연결 성공 시 명령어 실행
        try:
            std_outs, std_err_list = [], []
            cmd_with_sudo_s = f"sudo -S {cmd}"
            logging.debug(f'Executing command: {cmd_with_sudo_s}')

            stdin, stdout, stderr = ssh.exec_command(cmd_with_sudo_s)
            # 암호가 필요한 sudo를 위해 암호를 stdin으로 전달
            if self.wireless_target.pw:
                stdin.write(self.wireless_target.pw + '\n')
                stdin.flush()

            stdout_str = stdout.read().decode('utf-8', errors='ignore')
            stderr_str = stderr.read().decode('utf-8', errors='ignore')

            if stdout_str:
                std_outs = stdout_str.splitlines()
                logging.debug("Command stdout:")
                for line in std_outs:
                    logging.debug(f"  {line}")

            if stderr_str:
                std_err_list = stderr_str.splitlines()
                # sudo 암호 프롬프트는 오류가 아니므로 필터링
                if any("sudo: a password is required" in line for line in std_err_list):
                    pass  # Not a real error in this context
                elif std_err_list:
                    logging.error("Command stderr:")
                    for line in std_err_list:
                        logging.error(f"  {line}")

            # 성공했지만 warning이 있는 경우, 에러 리스트를 비웁니다.
            if std_outs and std_err_list:
                logging.warning(f"Command executed with warnings: {std_err_list}")
                std_err_list = []

            if QC_MODE:
                logging.debug(f'''std_outs={std_outs}''')
                logging.debug(f'''std_err_list={std_err_list}''')

            return std_outs, std_err_list

        except Exception as e:
            logging.error(f"명령어 실행 중 오류가 발생했습니다: {e}")
            ensure_debug_loged_verbose(traceback)
            return None, [str(e)]
        finally:
            ssh.close()

    def ensure_wireless_target_distro_docker_installed(self):
        import logging

        self._ensure_sudo_nopasswd_for_user()

        def _run(cmd: str, desc: str, *, timeout: int = 120, use_sudo: bool = True):
            logging.debug("[docker-install] 실행 준비 (%s): %s", desc, cmd)
            stdout, stderr, exit_status = self.ensure_command_to_wireless_target(
                cmd=cmd,
                timeout_seconds=timeout,
                use_sudo=use_sudo,
            )
            logging.debug(
                "[docker-install] 실행 완료 (%s)\n"
                "  - exit_status: %s\n"
                "  - stdout: %s\n"
                "  - stderr: %s",
                desc,
                exit_status,
                stdout if stdout else "<empty>",
                stderr if stderr else "<empty>",
            )
            if exit_status != 0:
                raise RuntimeError(f"[docker-install] 명령 실패: {desc}")
            return stdout, stderr, exit_status

        target_user = getattr(self.wireless_target, "user_name", "pk")

        # 0) 필수 패키지
        _run("apt update", "APT 업데이트")
        _run(
            "apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release",
            "Docker 의존 패키지 설치",
        )

        # n. Docker 설치 (docker.io) - Ubuntu LTS 호환
        _run("apt install -y docker.io", "Docker 패키지 설치 (docker.io)", timeout=300)

        # 4) docker 그룹 생성 및 사용자 추가
        _run("groupadd -f docker", "docker 그룹 생성")
        _run(f"usermod -aG docker {target_user}", "타겟 사용자를 docker 그룹에 추가")

        # 5) docker 서비스 재시작
        _run("systemctl enable --now docker", "Docker 서비스 활성화")

    def ensure_file_transferred_to_target(self, local_path: str, remote_path: str) -> bool:
        import logging
        import traceback

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

        self._connect()  # Ensure connection is active
        if not self._ssh_client:
            logging.error("Cannot transfer file, SSH client is not connected.")
            return False

        logging.info(
            f"Attempting to transfer file via SFTP using existing session:\n"
            f"  - Local Path: {local_path}\n"
            f"  - Remote Path: {remote_path}"
        )

        try:
            if not self._sftp_client or self._sftp_client.sock.closed:
                self._sftp_client = self._ssh_client.open_sftp()

            self._sftp_client.put(local_path, remote_path)
            logging.info(f"File transfer successful: {local_path} -> {self.wireless_target.ip}:{remote_path}")
            return True
        except Exception as e:
            logging.error(f"SFTP operation failed: {e}")
            ensure_debug_loged_verbose(traceback)
            # In case of error, close the sftp client to force re-opening on next attempt
            if self._sftp_client:
                self._sftp_client.close()
                self._sftp_client = None
            return False
        # The underlying SSH connection is not closed here

    def ensure_command_to_wireless_target(self, cmd, timeout_seconds=30, use_sudo=True):
        import logging
        import time
        import traceback

        import select

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

        self._connect()  # Ensure connection is active
        if not self._ssh_client:
            logging.error("Cannot execute command, SSH client is not connected.")
            return None, ["SSH client not connected"], -1

        logging.debug(
            f"Executing command on target:\n"
            f"  - Host: {self.wireless_target.ip}:{self.wireless_target.port}\n"
            f"  - User: {self.wireless_target.user_name}\n"
            f"  - Command: {cmd}"
        )

        channel = None
        try:
            std_outs_raw = []
            std_err_raw = []
            cmd_to_execute = f"sudo -S {cmd}" if use_sudo else cmd
            logging.debug(f'Executing command: {cmd_to_execute}')

            channel = self._ssh_client.get_transport().open_session()
            channel.set_combine_stderr(True)  # Combine stdout and stderr
            channel.exec_command(cmd_to_execute)

            # Send password for sudo if needed immediately to avoid blocking
            if use_sudo and self.wireless_target and self.wireless_target.pw:
                try:
                    transport = self._ssh_client.get_transport()
                    if transport and transport.is_active():
                        channel.send(self.wireless_target.pw + '\n')
                        logging.debug("Sent sudo password immediately after command execution.")
                    else:
                        logging.warning("SSH transport inactive; cannot send sudo password immediately.")
                except Exception as send_error:
                    logging.warning("Failed to send sudo password immediately: %s", send_error)

            # Since stdout/stderr are combined, we read from one stream
            stdout_channel = channel.makefile('r', -1)

            # Non-blocking read with select
            start_time = time.time()
            while not channel.exit_status_ready():
                if time.time() - start_time > timeout_seconds:
                    logging.error(f"Command '{cmd_to_execute}' timed out after {timeout_seconds} seconds.")
                    return None, [f"Command timed out after {timeout_seconds} seconds."], -1

                rlist, _, _ = select.select([channel], [], [], 0.1)
                if channel in rlist:
                    line = stdout_channel.readline()
                    if not line:
                        break
                    line = line.strip()
                    std_outs_raw.append(line)
                    if use_sudo and "[sudo] password for" in line:
                        logging.debug("Sudo password prompt detected. Sending password again.")
                        try:
                            transport = self._ssh_client.get_transport()
                            if transport and transport.is_active():
                                channel.send(self.wireless_target.pw + '\n')
                            else:
                                logging.warning("SSH transport inactive while attempting to resend sudo password.")
                        except Exception as send_error:
                            logging.warning("Failed to send sudo password on prompt: %s", send_error)

            # Capture any remaining data
            for line in stdout_channel.readlines():
                std_outs_raw.append(line.strip())

            exit_status = channel.recv_exit_status()
            logging.debug(f"Command exit status: {exit_status}")

            # Since output is combined, std_err_list is based on exit_status
            std_outs = std_outs_raw
            std_err_list = std_outs_raw if exit_status != 0 else []

            if std_outs:
                logging.debug("Command output:")
                for line in std_outs:
                    logging.debug(f"  {line}")

            return std_outs, std_err_list, exit_status

        except Exception as e:
            logging.error(f"An error occurred while executing command: {e}")
            ensure_debug_loged_verbose(traceback)
            return None, [str(e)], -1
        finally:
            if channel:
                channel.close()
            # The main SSH client connection is NOT closed here anymore

    def get_f_local_ssh_public_key(self):
        pass

    def set_wireless_target(self, config: dict = None):

        from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        from pk_internal_tools.pk_objects.pk_target import PkTarget
        from pk_internal_tools.pk_objects.pk_directories import D_USERPROFILE
        from pk_internal_tools.pk_objects.pk_device_registry import device_registry
        from pathlib import Path
        
        # 기본 SSH 키 경로 정의
        F_LOCAL_SSH_PUBLIC_KEY = D_USERPROFILE / ".ssh" / "id_ed25519.pub"
        F_LOCAL_SSH_PRIVATE_KEY = D_USERPROFILE / ".ssh" / "id_ed25519"

        func_n = get_caller_name()
        
        # config가 None이면 빈 dict로 초기화
        if config is None:
            config = {}
        
        # identifier 확인 및 처리
        identifier = config.get('identifier')
        
        # identifier가 이미 등록되어 있으면 저장된 정보 가져오기
        if identifier:
            stored_controller, stored_target = device_registry.get_or_register(identifier)
            if stored_target:
                # 저장된 target 정보로 config 병합 (입력된 config가 우선)
                config = {**stored_target, **config}
                logging.info(f"저장된 디바이스 정보 사용: identifier='{identifier.value}'")
        
        if identifier is None:
            key_name = 'target_identifier'
            pk_devices_enum = [PkDevice.jetson_agx_xavier, PkDevice.jetson_nano, PkDevice.arduino_nano, PkDevice.arduino_nano_esp32]
            pk_devices = [item.value for item in pk_devices_enum]
            if QC_MODE:
                pk_device = PkDevice.jetson_agx_xavier.value
            else:
                pk_device = ensure_value_completed(
                    key_name=key_name,
                    func_n=func_n,
                    options=pk_devices,
                    guide_text="pk_device 를 선택해주세요"
                )

            if pk_device:
                identifier = next((item for item in pk_devices_enum if item.value == pk_device), None)
                config['identifier'] = identifier
            else:
                raise ValueError("디바이스 identifier를 선택하지 않았습니다.")

        # Define keys for user input
        user_input_keys = {
            'user_name': 'target_user_name',
            'ip': 'target_ip',
            'pw': 'target_pw',
            'hostname': 'target_hostname',
            'port': 'target_port',
            'f_local_ssh_public_key': 'target_f_local_ssh_public_key',
            'f_local_ssh_private_key': 'target_f_local_ssh_private_key',
            'nick_name': 'target_nick_name',
            'distro_name': 'target_distro_name',
        }

        # Xavier specific settings
        if identifier == PkDevice.jetson_agx_xavier:
            user_input_keys.update({
                'user_name': "pk_xavier_user_id",
                'ip': "pk_xavier_ip",
                'pw': "pk_xavier_pw",
            })
            if QC_MODE:
                config['f_local_ssh_public_key'] = config.get('f_local_ssh_public_key') or F_LOCAL_SSH_PUBLIC_KEY
                config['f_local_ssh_private_key'] = config.get('f_local_ssh_private_key') or F_LOCAL_SSH_PRIVATE_KEY
                config['nick_name'] = config.get('nick_name') or "pk jetson xavier"
                config['distro_name'] = config.get('distro_name') or "Ubuntu 20.04 LTS"
                config['hostname'] = config.get('hostname') or 'pk-xavier'
                config['port'] = config.get('port') or 22

        # Get any remaining None values from the user
        for key in ['ip', 'pw', 'hostname', 'port', 'user_name', 'f_local_ssh_public_key', 'f_local_ssh_private_key', 'nick_name', 'distro_name']:
            if config.get(key) is None:
                input_key = user_input_keys.get(key)
                if key == 'distro_name':
                    pk_devices = ["windows", "linux", "macos", "android"] + self.get_wsl_distro_names_installed()
                    config[key] = ensure_env_var_completed_2025_11_24(key_name=input_key, func_n=func_n, options=pk_devices)
                else:
                    config[key] = ensure_env_var_completed_2025_11_24(key_name=input_key, func_n=func_n)

        self.wireless_target = PkTarget(**config)
        
        # 레지스트리에 등록/업데이트 (identifier로 저장된 정보 유지)
        device_registry.register(identifier, self, target_config=config)

    def ensure_self_info_printed(self):
        import json
        import logging

        self_dict = {
            "identifier": self.identifier.value if self.identifier else None,
            "nick_name": self.nick_name,
            "ip": getattr(self, 'ip', None),
            "hostname": getattr(self, 'hostname', None),
            "port": getattr(self, 'port', None),
            "user_n": getattr(self, 'user_n', None),
            "f_local_ssh_public_key": str(getattr(self, 'f_local_ssh_public_key', None)),
            "f_local_ssh_private_key": str(getattr(self, 'f_local_ssh_private_key', None)),
            # Password ('pw') is intentionally omitted for security.
        }

        pretty_json = json.dumps(self_dict, indent=4, ensure_ascii=False)
        logging.debug(f"PkWirelessTargetController (self) info:\n{pretty_json}")
        return pretty_json

    def ensure_wireless_target_info_printed(self):
        import logging

        logging.debug(f'self.target.to_json()={self.wireless_target.to_json()}')
        return

    def ensure_wireless_target_effective_info_printed(self):
        import json
        import logging

        # target 객체 → dict
        target_dict = self.wireless_target.to_dict()

        # None 값 제거
        effective_dict = {k: v for k, v in target_dict.items() if v is not None}

        # JSON 문자열 변환
        pretty_json = json.dumps(effective_dict, indent=4, ensure_ascii=False)

        logging.debug(pretty_json)
        return pretty_json

    def ensure_self_effective_info_printed(self):

        # Manually construct a dictionary from self's attributes
        self_dict = {
            "identifier": self.identifier.value if self.identifier else None,
            "nick_name": self.nick_name,
            "ip": getattr(self, 'ip', None),
            "hostname": getattr(self, 'hostname', None),
            "port": getattr(self, 'port', None),
            "user_n": getattr(self, 'user_n', None),
            "f_local_ssh_public_key": str(getattr(self, 'f_local_ssh_public_key', None)),
            "f_local_ssh_private_key": str(getattr(self, 'f_local_ssh_private_key', None)),
            # Password ('pw') is intentionally omitted for security.
        }

        # Filter out None values
        effective_dict = {k: v for k, v in self_dict.items() if v is not None}

        # Convert to pretty JSON string
        pretty_json = json.dumps(effective_dict, indent=4, ensure_ascii=False)

        logging.debug(f"PkWirelessTargetController (self) effective info:\n{pretty_json}")
        return pretty_json

    def get_sh_quote(self, s: str) -> str:

        # TODO renaming
        return "'" + s.replace("'", "'\"'\"'") + "'"

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------
    def _ensure_sudo_nopasswd_for_user(self):
        import logging
        import textwrap

        if self._sudo_nopasswd_ready:
            return

        target_user = getattr(self.wireless_target, "user_name", None)
        if not target_user:
            logging.warning("타겟 사용자 정보를 찾을 수 없어 sudo NOPASSWD 구성이 필요합니다.")
            return

        fragment_path = f"/etc/sudoers.d/pk_{target_user}_nopasswd"
        entry_text = f"{target_user} ALL=(ALL) NOPASSWD:ALL"
        entry_text_escaped = entry_text.replace('"', r'\"')

        def _run(cmd: str, desc: str, use_sudo: bool = True):
            logging.debug("[sudo-nopasswd] %s -> %s", desc, cmd)
            stdout, stderr, exit_status = self.ensure_command_to_wireless_target(
                cmd=cmd,
                timeout_seconds=60,
                use_sudo=use_sudo,
            )
            logging.debug(
                "[sudo-nopasswd] 완료 (%s) exit=%s stdout=%s stderr=%s",
                desc,
                exit_status,
                stdout if stdout else "<empty>",
                stderr if stderr else "<empty>",
            )
            return stdout, stderr, exit_status

        # 이미 구성되어 있는지 확인
        _, _, check_exit = _run(
            cmd=f"test -f {fragment_path} && grep -q \"{entry_text}\" {fragment_path}",
            desc="기존 sudoers 항목 확인",
        )
        if check_exit == 0:
            logging.info("타겟 사용자 sudo NOPASSWD 설정이 이미 구성되어 있습니다.")
            self._sudo_nopasswd_ready = True
            return

        logging.info("타겟 사용자 sudo NOPASSWD 설정을 구성합니다.")
        script = textwrap.dedent(
            f"""
            set -e
            tmp_file=$(mktemp)
            printf '%s\\n' "{entry_text_escaped}" > "$tmp_file"
            install -o root -g root -m 440 "$tmp_file" "{fragment_path}"
            rm -f "$tmp_file"
            visudo -cf /etc/sudoers
            """
        ).strip()
        _run(
            cmd=f"bash -lc {self.get_sh_quote(script)}",
            desc="sudoers 조각 생성",
        )

        self._sudo_nopasswd_ready = True

    # -------------------------------------------------------------------------
    # Python module helpers (e.g., ensure 'requests' installed)
    # -------------------------------------------------------------------------
    def ensure_requests_module_available(self) -> bool:
        import logging

        logging.info("타겟 장치에서 'requests' 모듈 설치 여부를 확인합니다.")

        def _normalize_output(data):
            if data is None:
                return "<empty>"
            if isinstance(data, (list, tuple)):
                return "\n".join(str(item) for item in data).strip()
            return str(data).strip()

        def _run(cmd: str, desc: str, use_sudo: bool):
            logging.debug("[requests-check] 실행 준비: %s -> %s", desc, cmd)
            result = self.ensure_command_to_wireless_target(
                cmd=cmd,
                timeout_seconds=120,
                use_sudo=use_sudo,
            )
            stdout, stderr, exit_status = result
            logging.debug(
                "[requests-check] 실행 완료 (%s)\n"
                "  - exit_status: %s\n"
                "  - stdout: %s\n"
                "  - stderr: %s",
                desc,
                exit_status,
                _normalize_output(stdout),
                _normalize_output(stderr),
            )
            return result

        def _verify(stage: str) -> bool:
            _, _, exit_status = _run(
                'python3 -c "import requests"',
                f"requests import test ({stage})",
                use_sudo=False,
            )
            if exit_status == 0:
                logging.info("[requests-check] '%s' 단계에서 import 성공", stage)
                return True
            logging.debug("[requests-check] '%s' 단계에서 import 실패", stage)
            return False

        if _verify("pre-install"):
            logging.info("'requests' 모듈이 이미 설치되어 있습니다.")
            return True

        logging.info("'requests' 모듈이 설치되어 있지 않아 설치를 시도합니다.")
        install_cmd = "python3 -m pip install --user requests"
        _, _, exit_status = _run(install_cmd, "requests install (user pip)", use_sudo=False)
        if exit_status != 0:
            logging.error("'%s' 명령이 실패했습니다 (exit=%s). 설치를 중단합니다.", install_cmd, exit_status)
            return False

        logging.info("'requests' 설치 명령이 성공했습니다. 설치 확인을 진행합니다.")
        if _verify("post-install"):
            logging.info("'requests' 모듈이 정상적으로 import 됩니다.")
            return True

        logging.error("설치 후에도 'requests' 모듈 import 에 실패했습니다.")
        return False
