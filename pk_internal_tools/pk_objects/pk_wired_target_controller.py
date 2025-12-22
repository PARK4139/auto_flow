import logging
import subprocess
import textwrap
import traceback
from enum import Enum
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_command_executed_as_admin import ensure_command_executed_as_admin
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
from pk_internal_tools.pk_functions.ensure_pk_python_file_executed_in_uv_venv_windows import ensure_pk_python_file_executed_in_uv_venv_windows
from pk_internal_tools.pk_functions.ensure_signature_found_in_lines import ensure_signature_found_in_lines
from pk_internal_tools.pk_functions.ensure_signature_found_in_souts_for_milliseconds_limited import ensure_signature_found_in_souts_for_milliseconds_limited
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
from pk_internal_tools.pk_functions.get_milliseconds_from_seconds import get_milliseconds_from_seconds
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
from pk_internal_tools.pk_functions.get_window_title_temp_for_cmd_exe import get_window_title_temp_for_cmd_exe
from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified
from pk_internal_tools.pk_functions.is_internet_connected import is_internet_connected
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_objects.pk_colorful_logging_formatter import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_directories import D_PK_WRAPPERS
from pk_internal_tools.pk_objects.pk_files import F_USBPIPD_MSI, F_LOCAL_SSH_PUBLIC_KEY, F_LOCAL_SSH_PRIVATE_KEY
from pk_internal_tools.pk_objects.pk_files import F_WSL_SSHD_CONFIG
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_identifier import PkIdentifier
from pk_internal_tools.pk_objects.pk_modes import PkModesForSdkManager
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_target import PkTarget
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_ubuntu_package_name import UbuntuPakageName


# 기본 SSH 키 경로 정의


class WslDistrosNotSupportedOfficiallyAnymore(Enum):
    ubuntu_18_04 = "Ubuntu-18.04"


class PkWiredTargetController(PkIdentifier):
    from typing import Optional

    from pk_internal_tools.pk_objects.pk_target import PkTarget

    _wsl: PkTarget = None
    _wired_target: PkTarget = None

    from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

    def __init__(self, identifier: "PkDevice" = PkDevice.undefined, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None):
        super().__init__(identifier)

        self.window_title_temp = get_window_title_temp_identified(__file__)
        self._init_kwargs = dict(ip=ip, pw=pw, hostname=hostname, port=port, user_n=user_n, f_local_ssh_public_key=f_local_ssh_public_key, f_local_ssh_private_key=f_local_ssh_private_key, nick_name=nick_name)
        self.ensure_executed_by_setup_op(**self._init_kwargs)
        logging.debug(f'{get_caller_name()} is initialized')

    def ensure_executed_by_setup_op(self, *, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None) -> None:
        import logging
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice

        self.set_self(
            ip=ip, pw=pw, hostname=hostname, port=port, user_n=user_n,
            f_local_ssh_public_key=f_local_ssh_public_key,
            f_local_ssh_private_key=f_local_ssh_private_key,
            nick_name=nick_name,
        )
        logging.debug("set_self() done")

        if not self.identifier == PkDevice.undefined:
            self.set_wired_target()
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

    @ensure_seconds_measured
    def ensure_usbipd_enabled(self):
        if not self.get_uspipd_version():
            self.ensure_usbipd_installed()

        if not self.is_usbipd_enabled():
            self.ensure_usbipd_installed()

        if not self.get_uspipd_version() and not self.is_usbipd_enabled():
            logging.info("usbipd 가 활성화 되어 있지 않습니다")
            return False

        logging.debug("usbipd가 이미 설치 및 활성화되어 있습니다.")
        return True

    def get_wsl_version(self):
        import logging
        import subprocess

        wsl_version = None
        try:
            result = subprocess.run(["wsl", "--version"], capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            output = result.stdout
            for line in output.splitlines():
                if line.strip().startswith("WSL 버전:") or line.strip().startswith("WSL version:"):
                    wsl_version = line.split(':')[-1].strip()
                    break

            if not wsl_version:
                logging.warning("Could not parse WSL version from 'wsl --version'.")

        except FileNotFoundError:
            logging.error("`wsl.exe` not found. Is WSL installed and in your PATH?")
            wsl_version = "Not Installed"
        except subprocess.CalledProcessError as e:
            logging.warning(f"'wsl --version' failed, possibly an older WSL. Error: {e.stderr}")
            wsl_version = "Unknown (command failed)"

        logging.debug(f"wsl_version={wsl_version}")
        return wsl_version

    def is_wsl_installed(self):
        import logging
        import subprocess
        try:
            # not os.path.exists(r"C:\Windows\System32\wsl.exe")
            subprocess.run(["wsl", "--status"], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            logging.debug("WSL is installed and accessible.")
            return True
        except FileNotFoundError:
            logging.debug("wsl.exe not found. WSL is not installed or not in PATH.")
            return False
        except subprocess.CalledProcessError as e:
            logging.debug(f"WSL command failed: {e.stderr}. WSL might be installed but not functioning correctly.")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while checking WSL installation: {e}")
            return False

    def get_wsl_distro_name_debug(self):

        # pk_* -> 명시적 초기화, ⚠️ 수동 초기화
        # env_var_name = "selected"
        # selected = ensure_value_completed(env_var_name=env_var_name, prompt_message=f"{env_var_name}", options=get_wsl_distro_names_installed())

        # pk_* -> 자동 초기화, ⚠️ 환경변수 selected 를 수정하기 위해서는 selected 수동 수정 필요
        env_var_name = "wsl_distro_name_debug"
        selected = ensure_env_var_completed(env_var_name=env_var_name, prompt_message=f"{env_var_name}", options=self.get_wsl_distro_names_installed())
        wsl_distro_name_debug = selected
        return wsl_distro_name_debug

    def get_wsl_distro_names_installed(self):
        import logging
        import subprocess
        try:
            result = subprocess.run(["wsl", "--list", "--quiet"], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode != 0:
                logging.error(f"Failed to list WSL distros: {result.stderr}")
                return []
            output = result.stdout.replace('\x00', '').strip()
            return [line.strip() for line in output.splitlines() if line.strip()]
        except FileNotFoundError:
            logging.error("wsl.exe not found. WSL is not installed or not in PATH.")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting WSL distro names: {e}")
            return []

    def get_wsl_distro_names_installable(self):
        """Returns a list of installable WSL distro names from 'wsl --list --online'."""
        import logging
        import subprocess
        import re
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback

        if not self.is_wsl_installed():
            logging.warning("WSL이 설치되어 있지 않아 설치 가능한 distro 목록을 가져올 수 없습니다.")
            return []

        try:
            cmd = ["wsl", "--list", "--online"]
            logging.debug(f"WSL 명령 실행: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-16-le', errors='ignore')
            output = result.stdout
            lines = output.strip().splitlines()

            if not lines:
                logging.warning("'wsl --list --online' 명령의 출력이 비어 있습니다.")
                return []

            distro_names = []
            header_found = False
            for i, line in enumerate(lines):
                if "NAME" in line and "FRIENDLY NAME" in line:  # Look for header line
                    header_found = True
                    # Start parsing from the next line
                    for data_line in lines[i + 1:]:  # Start from the line after the header
                        line_content = data_line.strip()
                        if not line_content:
                            continue
                        # Split by multiple spaces to handle variable spacing
                        parts = re.split(r'\s{2,}', line_content)
                        if parts and parts[0]:
                            distro_names.append(parts[0])
                    break  # Stop after processing data lines

            if not header_found:
                logging.warning("Could not find header 'NAME' in 'wsl --list --online' output. Parsing might be incorrect.")
                # Fallback to old parsing if header not found, assuming it's still valid for some cases
                if len(lines) >= 3:
                    for line in lines[2:]:
                        line_content = line.strip()
                        if not line_content:
                            continue
                        parts = re.split(r'\s{2,}', line_content)
                        if parts and parts[0]:
                            distro_names.append(parts[0])

            logging.debug(f"설치 가능한 WSL distro 목록: {distro_names}")
            return distro_names
        except FileNotFoundError:
            logging.error("wsl.exe를 찾을 수 없습니다. WSL이 설치되어 있고 PATH에 등록되어 있는지 확인하세요.")
            return []
        except subprocess.CalledProcessError as e:
            logging.error(f"온라인 WSL distro 목록을 가져오는 데 실패했습니다: {e.stderr}")
            return []
        except Exception as e:
            logging.error(f"설치 가능한 WSL distro을 가져오는 중 예상치 못한 오류가 발생했습니다: {e}")
            ensure_debugged_verbose(traceback, e)
            return []

    def ensure_wsl_distro_installed_by_user_selection(self):
        import logging
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.ensure_command_executed_as_admin import ensure_command_executed_as_admin

        # n. Get list of installable distros
        installable_distros = self.get_wsl_distro_names_installable()
        if not installable_distros:
            logging.error("Could not retrieve a list of installable WSL distributions.")
            ensure_spoken("설치 가능한 WSL distro 목록을 가져올 수 없습니다.")
            return None

        # n. Prompt user for selection
        key_name = 'wsl_distro_to_install'
        prompt_message = "설치할 WSL distro을 선택하세요:"
        selected_distro = ensure_value_completed(
            key_name=key_name,
            func_n="ensure_wsl_distro_installed_by_user_selection",
            options=installable_distros
        )

        if not selected_distro:
            logging.warning("No WSL distribution selected for installation.")
            return None

        # n. Check if it's already installed
        if self.is_wsl_distro_installed(selected_distro):
            logging.info(f"WSL distribution '{selected_distro}' is already installed.")
            ensure_spoken(f"{selected_distro} distro은 이미 설치되어 있습니다.")
            return selected_distro

        # n. Install the selected distro
        logging.info(f"Attempting to install WSL distribution: {selected_distro}")
        ensure_spoken(f"{selected_distro} distro 설치를 시작합니다. 이 작업은 시간이 걸릴 수 있습니다.")

        install_cmd = f"wsl --install -d {selected_distro}"

        # n. Installation requires admin rights.
        _, souts, errs = ensure_command_executed_as_admin(cmd=install_cmd)

        if errs:
            logging.error(f"Failed to install WSL distribution '{selected_distro}'. Error: {errs}")
            ensure_spoken(f"{selected_distro} distro 설치에 실패했습니다.")
            return None

        # n. Verify installation
        if self.is_wsl_distro_installed(selected_distro):
            logging.info(f"Successfully installed WSL distribution: {selected_distro}")
            ensure_spoken(f"{selected_distro} distro이 성공적으로 설치되었습니다.")
            return selected_distro
        else:
            logging.error(f"Installation command for '{selected_distro}' was executed, but verification failed.")
            ensure_spoken(f"{selected_distro} distro 설치 후 확인 과정에서 실패했습니다.")
            return None

    def get_wsl_distro_hostname(self, distro_name):
        import logging
        import subprocess
        try:
            cmd = ["wsl", "-d", distro_name, "--", "hostname"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            hostname = result.stdout.strip()
            return hostname
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to get hostname for {distro_name}: {e.stderr}")
            return None
        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting WSL distro hostname: {e}")
            return None

    def get_wsl_distro_ip(self, distro_name):
        import logging
        import subprocess
        import re
        try:
            cmd = ["wsl", "-d", distro_name, "--", "ip", "addr", "show", "eth0"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            output = result.stdout
            ip_match = re.search(r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', output)
            if ip_match:
                return ip_match.group(1)
            else:
                logging.warning(f"Could not find IP address for {distro_name}.")
                return None
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to get IP address for {distro_name}: {e.stderr}")
            return None
        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting WSL distro IP: {e}")
            return None

    def get_wsl_distro_port(self, distro_name: str) -> Optional[str]:
        import subprocess
        f_ssh_config = self.ensure_wsl_distro_sshd_config_created(distro_name=distro_name)
        if not f_ssh_config:
            logging.error(f"[{distro_name}] sshd_config 파일을 확보하는데 최종 실패했습니다.")
            return None

        # n. Read the file content from WSL
        try:
            logging.debug(f"sshd_config 파일 내용을 WSL에서 읽습니다: {f_ssh_config}")
            cmd = ["wsl", "-d", distro_name, "--", "cat", str(f_ssh_config)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            config_content = result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"WSL에서 sshd_config 파일 읽기 실패: {e.stderr}")
            return None
        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return None
        except Exception as e:
            logging.error(f"sshd_config 파일 읽기 중 예상치 못한 오류 발생: {e}")
            return None

        # n. Auto-fix logic: Uncomment the default port if no other port is active
        PORT_SIGNATURE_COMMENTED = "#Port 22"
        PORT_TO_SET = "Port 22"
        has_commented_port = PORT_SIGNATURE_COMMENTED in config_content
        has_active_port = any(line.strip().startswith("Port") and not line.strip().startswith("#") for line in config_content.splitlines())

        if has_commented_port and not has_active_port:
            logging.warning(f"[{distro_name}] 활성 PORT 없이 기본 PORT가 주석 처리되어 있습니다. 자동 수정을 시도합니다.")
            try:
                new_content = config_content.replace(PORT_SIGNATURE_COMMENTED, PORT_TO_SET, 1)
                f_ssh_config.write_text(new_content, encoding='utf-8')
                logging.info(f"sshd_config 파일을 수정했습니다. '{PORT_SIGNATURE_COMMENTED}' -> '{PORT_TO_SET}'")
                return "22"  # We know the port is 22 now
            except Exception as e:
                logging.error(f"sshd_config 파일 수정 중 오류 발생: {e}. 권한 문제일 수 있습니다.")
                # Fall through to parsing, which will likely return None.

        # n. Parse the content to find the active port
        stdout_lines = config_content.splitlines()
        PORT_PREFIX = "Port"
        port_wsl = None

        for line in stdout_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith(PORT_PREFIX):
                try:
                    port_wsl = line.replace(PORT_PREFIX, "").strip().split()[0]
                    if port_wsl.isdigit():
                        logging.debug(f"추출된 WSL SSH PORT: {port_wsl} ")
                        return port_wsl
                    else:
                        logging.warning(f"추출된 PORT 값 '{port_wsl}'이 유효한 숫자가 아닙니다.")
                        port_wsl = None
                except Exception as e:
                    logging.error(f"PORT 추출 중 오류 발생: {e}")
                    port_wsl = None

        if port_wsl is None:
            logging.debug("sshd_config 파일에서 활성화된 유효한 SSH PORT 설정을 찾을 수 없습니다.")

        return port_wsl

    def get_wsl_distro_pw(self, distro_name):
        import logging
        func_n = get_caller_name()
        try:
            ensure_slept(milliseconds=333)
            key_name = f'wsl_pw_of_{distro_name}'
            selected = ensure_env_var_completed(key_name=key_name, func_n=func_n)
            wsl_pw_of_distro_name = selected
            return wsl_pw_of_distro_name
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting WSL distro password: {e}")
            return None

    def ensure_wsl_distro_executed_with_persistent_session(self, distro_name):
        import logging
        import re
        import subprocess

        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        try:
            cmd = rf'wsl -l -v'
            stdout_list, _ = ensure_command_executed(cmd=cmd, encoding='utf-16-le')

            logging.debug(f"WSL distro 목록 파싱 시작")
            lines = [line.strip() for line in stdout_list if line.strip() and not line.strip().startswith("NAME")]
            for line in lines:
                match = re.match(r"^\*?\s*(?P<name>[^\s]+)\s+(?P<state>[^\s]+)\s+(?P<version>\d+)$", line)
                if match:
                    name = match.group("name")
                    state = match.group("state")
                    if name == distro_name and state == "Running":
                        logging.info(f"WSL distro '{name}'이(가) 설치되어 있고 실행 중입니다.")
                        return True
                    elif name == distro_name and state == "Stopped":
                        logging.info(f"WSL distro '{name}'이(가) 설치되어 있지만 중지 상태입니다. 시작을 시도합니다.")
                        try:
                            # keep wsl session at background for next wsl starting without_cold_start
                            subprocess.Popen(["wsl", "-d", distro_name, "--exec", "sleep", "infinity"])  # 이게 얼마나 강력하면 wsl --shutdown 해도 다시 살아난다.
                            logging.info(f"WSL distro '{name}' 시작 성공.")
                            return True
                        except Exception as e:
                            ensure_debugged_verbose(traceback, e)
                            return False
                else:
                    logging.debug(f"WSL distro 라인 파싱 실패: '{line}'")

            logging.info(f"❌ WSL distro '{distro_name}'이(가) 설치되어 있지 않거나 실행 중이 아닙니다.")
            return False




        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to ensure persistent session for {distro_name}: {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while ensuring WSL persistent session: {e}")
            return False

    def ensure_wsl_distro_sshd_config_created(self, distro_name):
        import logging
        import subprocess
        import textwrap
        try:
            check_cmd = ["wsl", "-d", distro_name, "--", "test", "-f", str(F_WSL_SSHD_CONFIG)]
            result = subprocess.run(check_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                logging.debug(f"sshd_config already exists in {distro_name}.")
                return F_WSL_SSHD_CONFIG
            sshd_config_content = textwrap.dedent("""
            Port 22
            ListenAddress 0.0.0.0
            ListenAddress ::
            PermitRootLogin yes
            PasswordAuthentication yes
            ChallengeResponseAuthentication no
            UsePAM yes
            X11Forwarding yes
            PrintMotd no
            AcceptEnv LANG LC_*
            Subsystem       sftp    /usr/lib/openssh/sftp-server
        """)
            temp_file_path = "/tmp/sshd_config_temp"
            # Use tee to write content, which is more robust for multi-line strings
            write_cmd = ["wsl", "-d", distro_name, "--", "tee", temp_file_path]
            subprocess.run(write_cmd, input=sshd_config_content.encode('utf-8'), check=True, capture_output=True)
            move_cmd = ["wsl", "-d", distro_name, "--", "sudo", "mv", temp_file_path, str(F_WSL_SSHD_CONFIG)]
            subprocess.run(move_cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            chmod_cmd = ["wsl", "-d", distro_name, "--", "sudo", "chmod", "644", str(F_WSL_SSHD_CONFIG)]
            subprocess.run(chmod_cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            logging.info(f"sshd_config created and configured in {distro_name}.")
            return F_WSL_SSHD_CONFIG
        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to create sshd_config for {distro_name}: {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while creating sshd_config: {e}")
            return False

    def get_wsl_distro_config(self):
        wsl_distro_config = self._wsl.to_dict()
        return wsl_distro_config

    def get_wsl_distro_ssh_config_file_contents(self):
        """지정된 WSL distro의 SSH 설정 파일 내용을 가져옵니다."""
        import logging
        import subprocess

        distro_name = self._wsl.distro_name

        cmd = f"wsl -d {distro_name} -- cat {str(F_WSL_SSHD_CONFIG)}"
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to get SSH config from {distro_name}: {e.stderr}")
            return None
        except FileNotFoundError:
            logging.error("`wsl.exe` not found. Is WSL installed and in your PATH?")
            return None

    def get_wsl_distro_info_std_list(self) -> list[str]:
        import logging
        import subprocess

        try:
            if not self.is_wsl_installed():
                ensure_spoken("wsl is not installed")
                return []

            result = subprocess.run(['wsl', '-l', '-v'], capture_output=True, text=True, encoding='utf-8', errors='ignore')

            if result.returncode != 0:
                logging.debug(f"WSL command failed with return code: {result.returncode}")
                if result.stderr:
                    logging.debug(f"WSL error: {result.stderr}")
                return []

            output = result.stdout
            if not output.strip():
                logging.debug("WSL command returned empty output")
                return []

            cleaned_output = output.replace('\x00', '').strip()
            std_list = [line.strip() for line in cleaned_output.splitlines() if line.strip()]

            if QC_MODE:
                logging.debug(f"WSL output lines: {len(std_list)}")
                for i, line in enumerate(std_list):
                    logging.debug(f"Line {i}: '{line}'")

            return std_list

        except FileNotFoundError:
            logging.debug("WSL command not found")
            return []
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            return []

    def ensure_wsl_distro_executed(self, distro_name) -> bool:
        import logging
        import subprocess
        # Removed re and ensure_command_executed imports as they are now in _get_wsl_distro_status

        status = self.get_wsl_distro_status(distro_name)
        if status == "Running":
            logging.info(f"WSL distro '{distro_name}'이(가) 설치되어 있고 실행 중입니다.")
            return True
        elif status == "Stopped":
            logging.info(f"WSL distro '{distro_name}'이(가) 설치되어 있지만 중지 상태입니다. 시작을 시도합니다.")
            try:
                subprocess.run(["wsl", "-d", distro_name, "--exec", "true"], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                logging.info(f"WSL distro '{distro_name}' 시작 성공.")
                return True
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to start WSL distro '{distro_name}': {e.stderr}")
                return False
            except FileNotFoundError:
                logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
                return False
            except Exception as e:
                logging.error(f"An unexpected error occurred while starting WSL distro '{distro_name}': {e}")
                return False
        else:  # status is None (not found or error)
            logging.info(f"❌ WSL distro '{distro_name}'이(가) 설치되어 있지 않거나 실행 중이 아닙니다.")
            return False

    def is_wsl_distro_installed(self, distro_name):
        import logging

        distros_executable = self.get_wsl_distro_names_executable()
        for distro in distros_executable:
            if distro['name'].strip().lower() == distro_name.strip().lower():
                logging.debug(f'"{distro_name} is installed"')
                return True
        logging.debug(f'"{distro_name} is not installed"')
        return False

    def is_wsl_distro_executed(self, distro_name: str) -> bool:
        """
        Checks if a specific WSL distribution is currently in the 'Running' state.

        Args:
            distro_name: The name of the WSL distribution to check.

        Returns:
            True if the distribution is running, False otherwise.
        """
        import logging

        status = self.get_wsl_distro_status(distro_name)
        if status == "Running":
            logging.debug(f"WSL distro '{distro_name}' is running.")
            return True
        else:
            logging.debug(f"WSL distro '{distro_name}' is not running (State: {status}).")
            return False

    def get_wsl_distro_status(self, distro_name) -> Optional[str]:
        import logging
        import re
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

        try:
            cmd = rf'wsl -l -v'
            stdout_list, _ = ensure_command_executed(cmd=cmd, encoding='utf-16-le')

            logging.debug(f"WSL distro 목록 파싱 시작")
            lines = [line.strip() for line in stdout_list if line.strip() and not line.strip().startswith("NAME")]
            for line in lines:
                match = re.match(r"^\*?\s*(?P<name>[^\s]+)\s+(?P<state>[^\s]+)\s+(?P<version>\d+)$", line)
                if match:
                    name = match.group("name")
                    state = match.group("state")
                    if name == distro_name:
                        logging.debug(f"Found WSL distro '{distro_name}' with state '{state}'.")
                        return state
                else:
                    logging.debug(f"WSL distro 라인 파싱 실패: '{line}'")
            logging.debug(f"WSL distro '{distro_name}' not found in list.")
            return None  # Distro not found
        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting WSL distro status: {e}")
            return None

    def ensure_wsl_distro_executed_fallback(self, distro_name, persistent: bool = False) -> bool:
        import logging
        import subprocess
        try:
            if persistent:
                logging.info(f"WSL distro '{distro_name}' is stopped. Attempting to start persistently.")
                subprocess.Popen(["wsl", "-d", distro_name, "--exec", "sleep", "infinity"])
            else:
                logging.info(f"WSL distro '{distro_name}'이(가) 중지 상태입니다. 시작을 시도합니다.")
                subprocess.run(["wsl", "-d", distro_name, "--exec", "true"], check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')

            logging.info(f"WSL distro '{distro_name}' started successfully.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to start WSL distro '{distro_name}': {e.stderr}")
            return False
        except FileNotFoundError:
            logging.error("wsl.exe not found. Is WSL installed and in your PATH?")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while starting WSL distro '{distro_name}': {e}")
            return False

    def setup_wsl_distro(self):
        func_n = get_caller_name()

        installed = self.is_wsl_installed()
        if not installed:
            ensure_spoken("this process need wsl, but not installed")
            return

        wsl_distro_name = None
        another_option = "ANOTHER WSL DISTRO AVAILABLE"
        if QC_MODE:
            while True:
                key_name = 'wsl_distro_name_for_debug'
                options = self.get_wsl_distro_names_installed() + [another_option]
                selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
                if selected == another_option:
                    question = f'do you want to install another wsl distro and use it'
                    ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                    if ok == PkTexts.YES:
                        self.ensure_wsl_distro_installed_by_user_selection()
                        continue
                wsl_distro_name = selected
                break
        else:
            while True:
                key_name = 'wsl_distro_name'
                options = self.get_wsl_distro_names_installed() + [another_option]
                selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=options)
                if selected == another_option:
                    question = f'do you want to install another wsl distro and use it'
                    ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                    if ok == PkTexts.YES:
                        self.ensure_wsl_distro_installed_by_user_selection()
                        continue
                wsl_distro_name = selected
                break

        sessions_enabled = self.ensure_wsl_distro_executed(distro_name=wsl_distro_name)
        if not sessions_enabled:
            ensure_spoken("wsl persistaent sessions is not enabled")
            return

        f_ssh_config = self.ensure_wsl_distro_sshd_config_created(distro_name=wsl_distro_name)
        if QC_MODE:
            wsl = PkTarget(
                identifier=wsl_distro_name,
                user_name="pk",
                f_local_ssh_public_key=F_LOCAL_SSH_PUBLIC_KEY,
                f_local_ssh_private_key=F_LOCAL_SSH_PRIVATE_KEY,
                nick_name="wsl_distro_nick_name",
                distro_name=wsl_distro_name,
                hostname=self.get_wsl_distro_hostname(wsl_distro_name),
                ip=self.get_wsl_distro_ip(distro_name=wsl_distro_name),
                pw=self.get_wsl_distro_pw(distro_name=wsl_distro_name),
                port=self.get_wsl_distro_port(distro_name=wsl_distro_name),
            )
            self._wsl = wsl
            return

        key_name = 'wsl_distro_user_n'
        selected = ensure_value_completed(key_name=key_name, func_n=func_n)
        wsl_distro_user_n = selected

        key_name = 'wsl_distro_f_local_ssh_public_key'
        selected = ensure_env_var_completed(key_name=key_name, func_n=func_n)
        wsl_distro_f_local_ssh_public_key = selected

        key_name = 'wsl_distro_f_local_ssh_private_key'
        selected = ensure_env_var_completed(key_name=key_name, func_n=func_n)
        wsl_distro_f_local_ssh_private_key = selected

        key_name = 'wsl_distro_nick_name'
        selected = ensure_env_var_completed(key_name=key_name, func_n=func_n)
        wsl_distro_nick_name = selected

        wsl = PkTarget(
            identifier=wsl_distro_user_n,
            user_name=wsl_distro_user_n,
            f_local_ssh_public_key=wsl_distro_f_local_ssh_public_key,
            f_local_ssh_private_key=wsl_distro_f_local_ssh_private_key,
            nick_name=wsl_distro_nick_name,
            distro_name=wsl_distro_name,
            hostname=self.get_wsl_distro_hostname(wsl_distro_name),
            ip=self.get_wsl_distro_ip(wsl_distro_name),
            pw=self.get_wsl_distro_pw(wsl_distro_name),
            port=self.get_wsl_distro_port(wsl_distro_name),
        )
        self._wsl = wsl

    def get_wsl_distros_data(self):
        # TODO : wsl 에 설치된 distro 정보들을 수집할때 필요
        import logging
        import re

        """WSL distro의 상세 정보를 구조화된 데이터로 반환합니다."""
        distro_info_list = self.get_wsl_distro_info_std_list()
        if not distro_info_list or len(distro_info_list) < 2:
            logging.info("Could not retrieve WSL distro information.")
            return None

        distros = distro_info_list[1:]
        data = {"distros": []}
        for line in distros:
            line = line.lstrip('*').strip()
            parts = re.split(r'\s+', line, 2)
            if len(parts) >= 3:
                name = parts[0]
                state = parts[1]
                version = parts[2]
                data["distros"].append({
                    "name": name,
                    "state": state,
                    "version": version,
                })
        return data

    def get_installed_distro_names(self) -> list[str]:
        import subprocess
        try:
            result = subprocess.run(['wsl', '--list', '--quiet'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode != 0:
                return []
            output = result.stdout.replace('\x00', '').strip()
            return [line.strip() for line in output.splitlines() if line.strip()]
        except Exception as e:
            logging.error("Failed to get installed WSL distro names.")
            return []

    @ensure_seconds_measured
    def ensure_usb_bridge_between_windows_and_wsl_established(self):
        import logging

        # wsl distro lsusb 설치
        if not self.ensure_wsl_distro_ubuntu_pkg_installed(UbuntuPakageName.usbutils):
            ensure_command_executed(cmd='sudo apt install -y usbutils')

        # windows usbipd 설치
        self.ensure_usbipd_enabled()

        # target 리커버리 모드진입
        bus_id = self.ensure_target_recovery_mode_entered()
        if not bus_id:
            logging.warning('bus_id is not found')
            return False

        logging.debug(rf'''bus_id={bus_id}  ''')

        # 바인딩 하지 않을 wsl distro 해제, 다른 wsl distro 에서 USB_ID 점유 예방
        for wsl_distro_name_installed in self.get_wsl_distro_names_installed():
            if wsl_distro_name_installed != self._wsl.distro_name:
                ensure_command_executed(cmd=f"wsl --terminate -d {wsl_distro_name_installed}")
                # TODO fix: 엔코딩 깨짐

        # ensure_command_executed(cmd=f"wsl -d {self._wsl.distro_name} -- exit")
        self.ensure_wsl_distro_session_alived(self._wsl.distro_name)
        ensure_command_executed(cmd=rf"usbipd unbind -b {bus_id}", encoding='utf-8')
        # ensure_command_executed_as_admin(cmd=rf"usbipd bind --force -b {bus_id}")  # --force can make usb bridge Timeout problem when Xavier AGX flashing
        ensure_command_executed_as_admin(cmd=rf"usbipd bind -b {bus_id}")
        ensure_command_executed(cmd=rf'start "{get_window_title_temp()}" usbipd attach --wsl --busid {bus_id} --auto-attach', mode='a')

        # pk_* -> milliseconds_limited loop
        if self._wsl.distro_name == "Ubuntu-18.04":
            signature = 'NVidia Corp.'
        else:
            signature = "NVIDIA Corp. APX"
        is_found = ensure_signature_found_in_souts_for_milliseconds_limited(
            cmd=rf"wsl -d {self._wsl.distro_name} lsusb",
            signature=signature,
            milliseconds_limited=get_milliseconds_from_seconds(seconds=30),
        )
        if not is_found:
            return False

        guide_text_if_found = "usb bridge established between windows and wsl"
        logging.debug(rf'''{guide_text_if_found}  ''')

        return True

    @ensure_seconds_measured
    def ensure_wsl_distros_enabled_with_persistent_session(self):
        import logging
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        try:
            for distro_name in self.get_wsl_distro_names_executable():
                if self.ensure_wsl_distro_executed_with_persistent_session(distro_name):
                    logging.debug("WSL distros enabled with persistent sessions")
                else:
                    logging.debug("Failed to start WSL distros with persistent sessions")
                    return False
            return True
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
        finally:
            pass

    def ensure_command_to_wsl_distro_like_human_deprecated(self, cmd, distro_name, wsl_window_title_seg, exit_mode=False):
        import logging

        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person import ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person
        from pk_internal_tools.pk_functions.open_and_move_wsl_console_to_front import open_and_move_wsl_console_to_front
        from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
        from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
        from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
        import time
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        timeout = 20
        start_time = time.time()
        while 1:
            if is_window_opened(window_title_seg=wsl_window_title_seg):
                break
            open_and_move_wsl_console_to_front(distro_name=distro_name, window_title_seg=wsl_window_title_seg)
            logging.debug(time.time() - start_time)
            if time.time() - start_time > timeout:
                break
            ensure_slept(seconds=0.5)

        std_output_stream = ""
        timeout = 5
        start_time = time.time()
        while 1:
            if ensure_window_to_front(wsl_window_title_seg):
                ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text=cmd, wsl_mode=True)
                ensure_pressed("enter")
                break
            ensure_window_to_front(wsl_window_title_seg)

            # 5초가 지났는지 확인
            logging.debug(time.time() - start_time)
            if time.time() - start_time > timeout:
                logging.debug("5 seconds passed. Exiting loop.")
                break
            ensure_slept(seconds=0.5)  # CPU 점유율을 낮추기 위해 약간의 대기

        if exit_mode == True:
            timeout = 5
            start_time = time.time()
            while 1:
                if ensure_window_to_front(wsl_window_title_seg):
                    ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text="exit", wsl_mode=True)
                    ensure_pressed("enter")
                    ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text="exit", wsl_mode=True)
                    ensure_pressed("enter")
                    break
                else:
                    ensure_window_to_front(wsl_window_title_seg)
                logging.debug(time.time() - start_time)
                if time.time() - start_time > timeout:
                    logging.debug("5 seconds passed. Exiting loop.")
                    break
                ensure_slept(seconds=0.5)  # CPU 점유율을 낮추기 위해 약간의 대기

        # return std_output_stream

    def ensure_wsl_distro_executed_like_human(self, window_title_seg):
        from pk_internal_tools.pk_functions.open_and_move_wsl_console_to_front import open_and_move_wsl_console_to_front
        from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
        from pk_internal_tools.pk_functions.is_window_opened import is_window_opened

        if not is_window_opened(window_title_seg=window_title_seg):
            open_and_move_wsl_console_to_front(distro_name=self._wsl.distro_name, window_title_seg=window_title_seg)
        while 1:
            if ensure_window_to_front(window_title_seg):
                break
            ensure_window_to_front(window_title_seg)

    def ensure_command_to_wsl_distro_like_human(self, cmd, window_title_seg, sleep_time=500):
        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
        from pk_internal_tools.pk_functions.ensure_writen_like_human import ensure_writen_like_human
        from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
        self.ensure_wsl_distro_executed_like_human(window_title_seg=window_title_seg)
        ensure_writen_like_human(cmd)
        ensure_slept(milliseconds=sleep_time)
        ensure_pressed('enter')

    def ensure_wsl_distro_ubuntu_pkg_installed(self, ubuntu_pkg_name: "UbuntuPakageName"):
        """WSL distro에 지정된 우분투 패키지를 설치합니다."""
        import logging
        import subprocess
        pkg_name = ubuntu_pkg_name.value

        distro_name = self._wsl.distro_name

        # Define command strings at the top
        check_cmd = f"wsl -d {distro_name} -- dpkg -s {pkg_name}"
        update_cmd = f"wsl -d {distro_name} -- sudo apt-get update"
        install_cmd = f"wsl -d {distro_name} -- sudo apt-get install -y {pkg_name}"
        verify_cmd = f"wsl -d {distro_name} -- dpkg -s {pkg_name}"

        # 패키지 설치 여부 확인
        check_cmd_parts = check_cmd.split()
        logging.debug(textwrap.dedent(f"""
            cmd                      | {' '.join(check_cmd_parts)}
            distro_name              | {distro_name}
            pkg_name                 | {pkg_name}
            mode                     | sync
            encoding                 | utf-8
        """))
        try:
            result = subprocess.run(check_cmd_parts, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0 and "Status: install ok installed" in result.stdout:
                logging.info(f"Package '{pkg_name}' is already installed in {distro_name}.")
                return True
            elif result.returncode != 0:
                logging.debug(f"Command failed with exit code {result.returncode}: {' '.join(check_cmd_parts)}")
                if result.stdout:
                    logging.debug(f"Stdout: {result.stdout}")
                if result.stderr:
                    logging.debug(f"Stderr: {result.stderr}")
        except FileNotFoundError:
            logging.debug(f"Command not found: {' '.join(check_cmd_parts)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during check_cmd execution: {e}")
            # Optionally re-raise or handle more specifically

        # Package is not installed or check failed, proceed with installation.
        logging.info(f"Package '{pkg_name}' not found in {distro_name}. Attempting to install...")

        try:
            #
            logging.debug(PK_UNDERLINE)
            update_cmd_parts = update_cmd.split()
            logging.debug(textwrap.dedent(f"""
                cmd                      | {' '.join(update_cmd_parts)}
                distro_name              | {distro_name}
                pkg_name                 | {pkg_name}
                mode                     | sync
                encoding                 | utf-8
            """))
            update_result = subprocess.run(update_cmd_parts, capture_output=True, text=True, encoding='utf-8')
            if update_result.returncode == 0:
                logging.info(f"apt update successful for {pkg_name}.")
            else:
                logging.warning(f"apt update failed for {pkg_name}. Exit Code: {update_result.returncode}")
                if update_result.stdout:
                    logging.warning(f"Stdout: {update_result.stdout}")
                if update_result.stderr:
                    logging.warning(f"Stderr: {update_result.stderr}")

            #
            logging.debug(PK_UNDERLINE)
            install_cmd_parts = install_cmd.split()
            logging.debug(textwrap.dedent(f"""
                cmd                      | {' '.join(install_cmd_parts)}
                distro_name              | {distro_name}
                pkg_name                 | {pkg_name}
                mode                     | sync
                encoding                 | utf-8
            """))
            install_result = subprocess.run(install_cmd_parts, capture_output=True, text=True, encoding='utf-8')
            if install_result.returncode == 0:
                logging.info(f"Package '{pkg_name}' installation command succeeded.")
            else:
                logging.error(f"Package '{pkg_name}' installation command failed. Exit Code: {install_result.returncode}")
                if install_result.stdout:
                    logging.error(f"Stdout: {install_result.stdout}")
                if install_result.stderr:
                    logging.error(f"Stderr: {install_result.stderr}")
                return False

            # Verify installation after attempting to install
            logging.debug(PK_UNDERLINE)
            verify_cmd_parts = verify_cmd.split()
            logging.debug(textwrap.dedent(f"""
                cmd                      | {' '.join(verify_cmd_parts)}
                distro_name              | {distro_name}
                pkg_name                 | {pkg_name}
                mode                     | sync
                encoding                 | utf-8
            """))
            verify_result = subprocess.run(verify_cmd_parts, capture_output=True, text=True, encoding='utf-8')
            if "Status: install ok installed" in verify_result.stdout:
                logging.info(f"Package '{pkg_name}' is successfully installed and verified in {distro_name}.")
                return True
            else:
                logging.error(f"Package '{pkg_name}' installation verification failed in {distro_name}. Exit Code: {verify_result.returncode}")
                if verify_result.stdout:
                    logging.error(f"Stdout: {verify_result.stdout}")
                if verify_result.stderr:
                    logging.error(f"Stderr: {verify_result.stderr}")
                return False

        except FileNotFoundError:
            logging.error("`wsl.exe` not found. Is WSL installed and in your PATH?")
            return False
        except Exception as e:  # Catch any other unexpected errors during subprocess execution
            logging.error(f"An unexpected error occurred during package installation: {e}")
            return False

    def ensure_wsl_distro_enabled(self, distro_name, f_local_ssh_public_key):
        from pk_internal_tools.pk_functions.ensure_wsl_distro_install import ensure_wsl_distro_install

        import logging
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        import base64

        if is_os_windows():
            if not self.is_wsl_distro_installed(distro_name=distro_name):
                ensure_wsl_distro_install(distro_name=distro_name)
                if not self.is_wsl_distro_installed(distro_name=distro_name):
                    logging.debug(rf"{distro_name} install  ")
                    raise

            # Ensure openssh-server is installed
            logging.debug(f"Checking openssh-server installation status in {distro_name}...")
            check_ssh_install_cmd = f"wsl -d {distro_name} dpkg -s openssh-server"
            ssh_install_status_outs, ssh_install_status_errs = ensure_command_executed(check_ssh_install_cmd)

            if ssh_install_status_outs and "install ok installed" in " ".join(ssh_install_status_outs):
                logging.debug(f"openssh-server is already installed in {distro_name}. Skipping installation.")
            else:
                logging.debug(f"openssh-server not found or not fully installed. Installing in {distro_name}...")
                install_ssh_cmd = f"wsl -d {distro_name} sudo apt update && wsl -d {distro_name} sudo apt install -y openssh-server"
                install_ssh_outs, install_ssh_errs = ensure_command_executed(install_ssh_cmd)
                if install_ssh_errs:
                    logging.error(f"Failed to install openssh-server in {distro_name}: {install_ssh_errs}")
                    raise RuntimeError(f"Failed to install openssh-server in {distro_name}")
                logging.debug(f"openssh-server installation completed in {distro_name}.")

            # Add public key to authorized_keys
            logging.debug(f"Setting up authorized_keys for {distro_name}...")
            # Create .ssh directory and set permissions
            create_ssh_dir_cmd = f"wsl -d {distro_name} mkdir -p ~/.ssh"
            create_ssh_dir_outs, create_ssh_dir_errs = ensure_command_executed(create_ssh_dir_cmd)
            if create_ssh_dir_errs:
                logging.error(f"Failed to create ~/.ssh directory in {distro_name}: {create_ssh_dir_errs}")
                raise RuntimeError(f"Failed to create ~/.ssh directory in {distro_name}")

            chmod_ssh_dir_cmd = f"wsl -d {distro_name} chmod 700 ~/.ssh"
            chmod_ssh_dir_outs, chmod_ssh_dir_errs = ensure_command_executed(chmod_ssh_dir_cmd)
            if chmod_ssh_dir_errs:
                logging.error(f"Failed to set permissions on ~/.ssh directory in {distro_name}: {chmod_ssh_dir_errs}")
                raise RuntimeError(f"Failed to set permissions on ~/.ssh directory in {distro_name}")

            # Base64 encode the public key content
            # encoded_public_key = base64.b64encode(str(f_local_ssh_public_key).encode('utf-8')).decode('utf-8')

            # Base64 encode the public key **content**, not the path
            try:
                pub_key_content = Path(f_local_ssh_public_key).read_text(encoding='utf-8').strip() + "\n"
            except Exception as e:
                logging.error(f"Failed to read local public key file: {f_local_ssh_public_key} ({e})")
                raise
            encoded_public_key = base64.b64encode(pub_key_content.encode('utf-8')).decode('utf-8')

            # Define a temporary file path in WSL
            temp_pub_key_file = "/tmp/temp_id_rsa.pub"

            # Write the base64 encoded key to a temp file, then decode it in WSL
            write_pub_key_cmd = f"wsl -d {distro_name} bash -c \"echo '{encoded_public_key}' | base64 -d > {temp_pub_key_file}\""

            write_pub_key_outs, write_pub_key_errs = ensure_command_executed(write_pub_key_cmd)
            if write_pub_key_errs:
                logging.error(f"Failed to write public key to temp file in {distro_name}: {write_pub_key_errs}")
                raise RuntimeError(f"Failed to write public key to temp file in {distro_name}")

            # Check if temp_pub_key_file exists before appending
            check_temp_file_cmd = f"wsl -d {distro_name} test -f {temp_pub_key_file}"
            check_temp_file_outs, check_temp_file_errs = ensure_command_executed(check_temp_file_cmd)
            if check_temp_file_errs:
                logging.error(f"Temporary public key file {temp_pub_key_file} does not exist or is inaccessible in {distro_name}: {check_temp_file_errs}")
                raise RuntimeError(f"Temporary public key file {temp_pub_key_file} not found in {distro_name}")

            append_pub_key_cmd = f"wsl -d {distro_name} bash -c \"cat {temp_pub_key_file} >> ~/.ssh/authorized_keys\""
            append_pub_key_outs, append_pub_key_errs = ensure_command_executed(append_pub_key_cmd)
            if append_pub_key_errs:
                logging.error(f"Failed to append public key to authorized_keys in {distro_name}: {append_pub_key_errs}")
                raise RuntimeError(f"Failed to append public key to authorized_keys in {distro_name}")

            # Set permissions on authorized_keys
            chmod_auth_keys_cmd = f"wsl -d {distro_name} chmod 600 ~/.ssh/authorized_keys"
            chmod_auth_keys_outs, chmod_auth_keys_errs = ensure_command_executed(chmod_auth_keys_cmd)
            if chmod_auth_keys_errs:
                logging.error(f"Failed to set permissions on authorized_keys in {distro_name}: {chmod_auth_keys_errs}")
                raise RuntimeError(f"Failed to set permissions on authorized_keys in {distro_name}")

            # Remove temporary public key file
            rm_temp_pub_key_cmd = f"wsl -d {distro_name} rm {temp_pub_key_file}"
            rm_temp_pub_key_outs, rm_temp_pub_key_errs = ensure_command_executed(rm_temp_pub_key_cmd)
            if rm_temp_pub_key_errs:
                logging.warning(f"Failed to remove temporary public key file in {distro_name}: {rm_temp_pub_key_errs}")
                # Not a critical error, just log warning

            logging.debug(f"authorized_keys setup completed for {distro_name}.")

            # Ensure SSH service is running and enabled
            logging.debug(f"Checking SSH service status in {distro_name}...")
            check_ssh_active_cmd = f"wsl -d {distro_name} sudo systemctl is-active ssh"
            ssh_active_outs, ssh_active_errs = ensure_command_executed(check_ssh_active_cmd)
            if not ssh_active_outs or "active" not in " ".join(ssh_active_outs):
                logging.debug(f"SSH service not active. Starting in {distro_name}...")
                start_ssh_cmd = f"wsl -d {distro_name} sudo systemctl start ssh"
                start_ssh_outs, start_ssh_errs = ensure_command_executed(start_ssh_cmd)
                if start_ssh_errs:
                    logging.error(f"Failed to start SSH service in {distro_name}: {start_ssh_errs}")
                    raise RuntimeError(f"Failed to start SSH service in {distro_name}")
                logging.debug(f"SSH service started in {distro_name}.")

            check_ssh_enabled_cmd = f"wsl -d {distro_name} sudo systemctl is-enabled ssh"
            ssh_enabled_outs, ssh_enabled_errs = ensure_command_executed(check_ssh_enabled_cmd)
            if not ssh_enabled_outs or "enabled" not in " ".join(ssh_enabled_outs):
                logging.debug(f"SSH service not enabled. Enabling in {distro_name}...")
                enable_ssh_cmd = f"wsl -d {distro_name} sudo systemctl enable ssh"
                enable_ssh_outs, enable_ssh_errs = ensure_command_executed(enable_ssh_cmd)
                if enable_ssh_errs:
                    logging.error(f"Failed to enable SSH service in {distro_name}: {enable_ssh_errs}")
                logging.debug(f"SSH service enabled in {distro_name}.")

            # Add check for sudo service ssh status
            logging.debug(f"Final check for SSH service status in {distro_name} using 'sudo service ssh status'...")
            check_service_status_cmd = f"wsl -d {distro_name} sudo service ssh status"
            service_status_outs, service_status_errs = ensure_command_executed(check_service_status_cmd)

            if service_status_outs:
                logging.debug(f"SSH service status output:")
                for line in service_status_outs:
                    logging.debug(f"{line}")
            if service_status_errs:
                logging.error(f"SSH service status error output:")
                for line in service_status_errs:
                    logging.error(f" {line}")

            # Read and Log sshd_config
            logging.debug(f"Checking sshd_config in {distro_name}...")
            read_sshd_config_cmd = f"wsl -d {distro_name} sudo cat {str(F_WSL_SSHD_CONFIG)}"
            sshd_config_outs, sshd_config_errs = ensure_command_executed(read_sshd_config_cmd)

            if sshd_config_errs:
                logging.error(f"Error reading sshd_config in {distro_name}: {sshd_config_errs}")
            elif sshd_config_outs:
                logging.debug(f"sshd_config content:")
                port_found = False
                listen_address_found = False
                for line in sshd_config_outs:
                    logging.debug(f"{line}")
                    if line.strip().startswith("Port"):  # Check for Port
                        try:
                            port_value = int(line.strip().split()[1])
                            if port_value != 22:
                                logging.warning(f"sshd_config: Port is set to {port_value}, expected 22.")
                            port_found = True
                        except Exception as e:
                            logging.warning(f"sshd_config: Could not parse Port line: {line}")
                    if line.strip().startswith("ListenAddress"):  # Check for ListenAddress
                        try:
                            address_value = line.strip().split()[1]
                            if address_value not in ["0.0.0.0", "::"]:
                                logging.warning(f"sshd_config: ListenAddress is set to {address_value}, expected 0.0.0.0 or ::.")
                            listen_address_found = True
                        except Exception as e:
                            logging.warning(f"sshd_config: Could not parse ListenAddress line: {line}")
                if not port_found:
                    logging.warning("sshd_config: Port directive not found. Defaulting to 22.")
                if not listen_address_found:
                    logging.warning("sshd_config: ListenAddress directive not found. Defaulting to all interfaces.")

            # Read and Log ufw status
            logging.debug(f"Checking ufw status in {distro_name}...")
            ufw_status_cmd = f"wsl -d {distro_name} sudo ufw status"
            ufw_status_outs, ufw_status_errs = ensure_command_executed(ufw_status_cmd)

            if ufw_status_errs:
                logging.error(f"Error checking ufw status in {distro_name}: {ufw_status_errs}")
            elif ufw_status_outs:
                logging.debug(f"ufw status output:")
                ufw_active = False
                port_22_allowed = False
                for line in ufw_status_outs:
                    logging.debug(f"{line}")
                    if "Status: active" in line:
                        ufw_active = True
                    if "22/tcp" in line and ("ALLOW" in line or "ALLOW IN" in line):
                        port_22_allowed = True

                if ufw_active and not port_22_allowed:
                    logging.warning(f"ufw is active in {distro_name} and port 22/tcp is not explicitly allowed. This might block SSH.")
                elif ufw_active and port_22_allowed:
                    logging.debug(f"ufw is active and port 22/tcp is allowed in {distro_name}.")
                elif not ufw_active:
                    logging.debug(f"ufw is inactive in {distro_name}.")
        return True

    def ensure_target_distro_package_installed(self, distro_package_name):
        # TODO : windows/linux 에 따라 다르게 구현 필요.
        #  distro_pkg_n 는 windows 라면 application_name
        import logging
        from pk_internal_tools.pk_functions.ensure_general_ubuntu_pkg import ensure_general_ubuntu_pkg
        from pk_internal_tools.pk_functions.is_internet_connected import is_internet_connected

        if not is_internet_connected():
            logging.debug(f'''can not install ubuntu pakage ({distro_package_name}) for internet not connected  ''')
            raise
        if distro_package_name == 'docker':
            std_outs, std_errs = self.ensure_command_to_remote_target_with_pubkey(cmd='docker --version')
            if std_outs is None:  # Added check for None
                logging.error(f"Failed to get docker version from remote OS. SSH connection might be down.")
                return False
            if ensure_signature_found_in_lines(signature="The cmd 'docker' could not be found", lines=std_outs):
                logging.debug("docker is not installed in wsl")
                self.ensure_target_distro_docker_installed()
        elif distro_package_name == 'net-tools':
            ensure_not_prepared_yet_guided()
        else:
            # std_outs, std_errs = ensure_command_to_remote_os_with_pubkey(cmd=f'{ubuntu_pkg_n} --version')
            std_outs, std_errs = self.ensure_command_to_remote_target_with_pubkey(cmd=f'sudo apt list --installed | grep {distro_package_name}')
            if std_outs is None:
                logging.error(f"Failed to list installed packages for {distro_package_name} from remote OS. SSH connection might be down.")
                return False
            if ensure_signature_found_in_lines(signature='installed', lines=std_outs):
                logging.debug(f"{distro_package_name} is installed in {self._target.distro_name}")
                ensure_general_ubuntu_pkg(ubuntu_pkg_n=distro_package_name)
        return True

    def ensure_target_distro_docker_installed(self):
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(cmd='sudo usermod -aG docker $USER')
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(cmd='sudo apt update')
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(
            cmd='curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg')  # GPG 키 추가
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(
            cmd='sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release')  # wsl docker dependency
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(
            cmd='echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')  # Docker 리포지토리 추가
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(cmd='sudo apt update')
        std_outs, std_err_list = self.ensure_command_to_remote_target_with_pubkey(
            cmd='sudo apt install -y docker-ce docker-ce-cli containerd.io')

    def ensure_command_to_remote_target(self, cmd):
        return self.ensure_command_to_remote_target_with_pubkey(cmd=cmd)

    def ensure_file_transferred_to_remote_target(self, local_path: str, remote_path: str) -> bool:
        """
        SFTP를 사용하여 로컬 파일을 타겟 장치에 전송합니다.
        키 기반 인증을 먼저 시도하고 실패하면 암호 기반 인증으로 대체합니다.
        :param local_path: 로컬 파일 경로
        :param remote_path: 타겟 장치의 원격 경로
        :return: 전송 성공 여부
        """
        import logging
        import paramiko
        import traceback

        logging.info(
            f"Attempting to transfer file via SFTP:\n"
            f"  - Host: {self._wired_target.ip}:{self._wired_target.port}\n"
            f"  - User: {self._target.user_name}\n"
            f"  - Key File: {self._target.f_local_ssh_private_key}\n"
            f"  - Local Path: {local_path}\n"
            f"  - Remote Path: {remote_path}"
        )

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False

        # n. 공개 키 인증 시도
        try:
            if self._target.f_local_ssh_private_key:
                logging.info("SSH 공개 키로 연결을 시도합니다...")
                key_private = paramiko.Ed25519Key(file_name=self._target.f_local_ssh_private_key)
                ssh.connect(hostname=self._target.ip, port=self._target.port, username=self._target.user_name, pkey=key_private, timeout=10)
                connected = True
                logging.info("SSH 공개 키로 연결에 성공했습니다.")
            else:
                logging.warning("SSH 비공개 키가 제공되지 않았습니다.")
        except Exception as e:
            logging.warning(f"SSH 공개 키 인증에 실패했습니다: {e}")

        # n. 키 인증 실패 시 암호 인증으로 대체
        if not connected and self._target.pw:
            try:
                logging.info("SSH 암호로 연결을 시도합니다...")
                ssh.connect(hostname=self._target.ip, port=self._target.port, username=self._target.user_name, password=self._target.pw, timeout=10)
                connected = True
                logging.info("SSH 암호로 연결에 성공했습니다.")
            except Exception as e:
                logging.error(f"SSH 암호 인증도 실패했습니다: {e}")

        if not connected:
            logging.error("모든 SSH 인증 방법에 실패했습니다.")
            ensure_debugged_verbose(traceback, e)
            return False

        # 연결 성공 시 SFTP 작업 진행
        try:
            sftp = ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            logging.info(f"파일 전송 성공: {local_path} -> {self._target.ip}:{remote_path}")
            return True
        except Exception as e:
            logging.error(f"연결 후 SFTP 작업에 실패했습니다: {e}")
            ensure_debugged_verbose(traceback, e)
            return False
        finally:
            ssh.close()

    def get_f_local_ssh_public_key(self):
        pass

    def set_wired_target(self, config: dict = None):
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        from pk_internal_tools.pk_objects.pk_target import PkTarget
        from pk_internal_tools.pk_objects.pk_directories import D_USERPROFILE
        from pk_internal_tools.pk_objects.pk_device_registry import device_registry

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
            key_name = 'target_identifier_for_debug' if QC_MODE else 'target_identifier'
            pk_devices_enum = [PkDevice.jetson_agx_xavier, PkDevice.jetson_nano, PkDevice.arduino_nano, PkDevice.arduino_nano_esp32]
            pk_devices = [item.value for item in pk_devices_enum]
            if QC_MODE:
                pk_device = PkDevice.jetson_agx_xavier.value
            else:
                pk_device = ensure_env_var_completed(
                    key_name=key_name,
                    func_n=func_n,
                    options=pk_devices
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
                'user_name': "remote_target_user_id",
                'ip': "remote_target_ip",
                'pw': "remote_target_pw",
            })
            if QC_MODE:
                config['f_local_ssh_public_key'] = config.get('f_local_ssh_public_key') or F_LOCAL_SSH_PUBLIC_KEY
                config['f_local_ssh_private_key'] = config.get('f_local_ssh_private_key') or F_LOCAL_SSH_PRIVATE_KEY
                config['nick_name'] = config.get('nick_name') or "pk jetson remote_target"
                config['distro_name'] = config.get('distro_name') or "Ubuntu 20.04 LTS"
                config['hostname'] = config.get('hostname') or 'pk-remote_target'
                config['port'] = config.get('port') or 22

        # Get any remaining None values from the user
        for key in ['ip', 'pw', 'hostname', 'port', 'user_name', 'f_local_ssh_public_key', 'f_local_ssh_private_key', 'nick_name', 'distro_name']:
            if config.get(key) is None:
                input_key = user_input_keys.get(key)
                if key == 'distro_name':
                    pk_devices = ["windows", "linux", "macos", "android"] + self.get_wsl_distro_names_installed()
                    config[key] = ensure_env_var_completed(key_name=input_key, func_n=func_n, options=pk_devices)
                else:
                    config[key] = ensure_env_var_completed(key_name=input_key, func_n=func_n)

        self._wired_target = PkTarget(**config)

        # 레지스트리에 등록/업데이트 (identifier로 저장된 정보 유지)
        device_registry.register(identifier, self, target_config=config)

    @ensure_seconds_measured
    def ensure_wired_target_flashed(self):
        try:
            from pk_internal_tools.pk_objects.pk_identifier import PkDevice
            import logging

            # === Pre-flight check 1: Disk Space (MOVED) ===
            logging.info("WSL 배포판의 디스크 여유 공간을 확인합니다...")
            distro_name = self._wsl.distro_name
            user_name = self._wsl.user_name
            df_cmd = "df --output=avail -B1 / | tail -n 1"
            try:
                result = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, df_cmd)
                available_space_gb = int(result.stdout.strip()) / (1024 ** 3)
                logging.info(f"사용 가능한 공간: {available_space_gb:.2f}GB")
                if available_space_gb < 60:
                    logging.error(f"WSL 배포판의 여유 공간({available_space_gb:.2f}GB)이 60GB보다 적습니다. 공간을 확보한 후 다시 시도해주세요.")
                    return False
                else:
                    logging.info("디스크 여유 공간이 60GB 이상임을 확인했습니다.")
            except (ValueError, IndexError, subprocess.CalledProcessError) as e:
                logging.warning(f"WSL 여유 공간을 확인하는 중 오류 발생: {e}. 수동으로 60GB 이상을 확인해주세요.")
                ok = ensure_value_completed(key_name=f"WSL 여유 공간 확인에 실패했습니다. 계속 진행하시겠습니까?", options=[PkTexts.YES, PkTexts.NO])
                if ok == PkTexts.NO:
                    return False
            # === End of Disk Space Check ===

            connected = is_internet_connected()
            if not connected:
                ensure_spoken("network is not connected")
                return False

            # 바인딩 하지 않을 wsl distro 해제, 다른 wsl distro 에서 USB_ID 점유 예방
            # ensure_command_executed(cmd=f"wsl --shutdown")

            # self.ensure_target_info_printed()
            self.ensure_self_effective_info_printed()
            self.ensure_target_effective_info_printed()
            self.ensure_wsl_effective_info_printed()

            ensure_windows_killed_like_human_by_window_title(window_title="wsl")
            ensure_windows_killed_like_human_by_window_title(window_title="SDK Manager CLI 2.3.0.12626")
            ensure_windows_killed_like_human_by_window_title(window_title=get_window_title_temp())
            ensure_windows_killed_like_human_by_window_title(window_title=get_window_title_temp_for_cmd_exe())
            ensure_windows_killed_like_human_by_window_title(window_title=self.window_title_temp)

            # ensure_spoken(rf"{get_easy_speakable_text(self.target.identifier.value)} 플래시 작업을 시작합니다")
            if self._wired_target.identifier == PkDevice.jetson_agx_xavier:

                # === Pre-flight cleanup logic (disk check was moved) ===
                logging.info("sdkmanager 실행 전, 정리 작업을 시작합니다.")
                distro_name = self._wsl.distro_name
                user_name = self._wsl.user_name

                # n. Clear SDKM download cache
                logging.info("SDK Manager 다운로드 캐시를 정리합니다 (~/.nvsdkm/sdkm_downloads/*)...")
                rm_cache_cmd = "rm -rf ~/.nvsdkm/sdkm_downloads/*"
                self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, rm_cache_cmd)
                logging.info("다운로드 캐시 정리 완료.")

                # 3. Clear old JetPack working directories
                logging.info("이전 JetPack 작업 디렉토리를 정리합니다 (~/nvidia/nvidia_sdk/JetPack_*)...")
                rm_jetpack_cmd = "rm -rf ~/nvidia/nvidia_sdk/JetPack_*"
                self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, rm_jetpack_cmd)
                logging.info("이전 JetPack 디렉토리 정리 완료.")
                # === End of pre-flight cleanup ===

                if self._wsl.distro_name == "Ubuntu-24.04":
                    logging.warning("Ubuntu-24.04 is not supported on Jetson AGX")
                    return False
                elif self._wsl.distro_name == "Ubuntu-20.04":
                    pass
                elif self._wsl.distro_name == "Ubuntu-18.04":
                    pass
                # user_name added
                # TODO : add user_name

                # no password
                self.ensure_wsl_distro_apps_without_user_pw_access_advanced(
                    self._wsl.distro_name,
                    self._wsl.user_name,
                )

                # usb bridge
                if not self.ensure_usb_bridge_between_windows_and_wsl_established():
                    logging.warning("usb_bridge not established")
                    return False

                # (A) 현재 작업 디렉토리: 반드시 Ext4(/home/사용자명)에서 실행 확인 및 이동
                logging.info("플래시 작업을 위해 현재 사용자의 홈 디렉토리로 이동합니다.")
                distro_name = self._wsl.distro_name
                target_user_name = self._wsl.user_name

                try:
                    # 'cd ~'는 실행 사용자 홈으로 이동하므로, 명시적으로 /home/user_name으로 이동
                    if target_user_name == "root":
                        cd_cmd = "cd /root"
                        expected_pwd_prefix = "/root"
                    else:
                        cd_cmd = f"cd /home/{target_user_name}"
                        expected_pwd_prefix = f"/home/{target_user_name}"

                    # 'cd ~'는 실행 사용자 홈으로 이동하므로, 명시적으로 /home/user_name으로 이동
                    # cd 명령과 pwd 명령을 한 번에 실행하여 정확한 현재 작업 디렉토리를 얻습니다.
                    combined_cmd = f"{cd_cmd} && pwd"
                    result_pwd = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, target_user_name, combined_cmd)

                    # combined_cmd의 출력에서 마지막 줄이 pwd 결과입니다.
                    current_wsl_pwd = result_pwd.stdout.strip().splitlines()[-1]

                    if not current_wsl_pwd.startswith(expected_pwd_prefix):
                        logging.error(f"현재 작업 디렉토리가 예상된 홈 디렉토리({expected_pwd_prefix})가 아닙니다. 현재: {current_wsl_pwd}")
                        logging.error("플래시 작업은 반드시 사용자의 홈 디렉토리(Ext4)에서 실행되어야 합니다. 프로세스를 중단합니다.")
                        return False
                    logging.info(f"현재 작업 디렉토리 ({current_wsl_pwd})가 사용자의 홈 디렉토리 (Ext4)에 있습니다. 확인 완료.")
                except Exception as e:
                    logging.error(f"WSL 작업 디렉토리 설정 및 확인 중 오류 발생: {e}")
                    return False

                # === Robust environment preparation v2 (version-specific) ===
                logging.info("플래시 환경 준비를 시작합니다 (버전 명시적 확인).")
                distro_name = self._wsl.distro_name
                user_name = self._wsl.user_name

                def find_path_in_wsl(find_cmd):
                    result = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, find_cmd)
                    path = result.stdout.strip() if result.stdout and result.stdout.strip() else ""
                    return path

                # n. Define version-specific paths
                work_base = f"/home/{user_name}/nvidia/nvidia_sdk/JetPack_5.1.5_Linux_JETSON_AGX_XAVIER_TARGETS"
                l4t_dir = f"{work_base}/Linux_for_Tegra"

                logging.info(f"목표 L4T 경로: {l4t_dir}")

                # n. Check if the correct, version-specific L4T directory exists
                check_dir_cmd = f"test -d {self.get_sh_quote(l4t_dir)} && echo EXISTS"
                result = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, check_dir_cmd)
                l4t_dir_exists = result.stdout and "EXISTS" in result.stdout.strip()

                # 3. If the specific L4T directory does not exist, find the tarball and extract it
                if not l4t_dir_exists:
                    logging.info(f"'{l4t_dir}'를 찾을 수 없습니다. Jetson Linux 압축 파일 존재 여부를 확인합니다.")

                    find_jetson_linux_cmd = "find ~/nvidia/nvidia_sdk ~/Downloads/nvidia/sdkm_downloads ~/.nvsdkm/sdkm_downloads -maxdepth 4 -type f -name 'Jetson_Linux_R35.6.1_aarch64.tbz2' 2>/dev/null | head -n1"
                    jetson_linux_tbz = find_path_in_wsl(find_jetson_linux_cmd)

                    if jetson_linux_tbz:
                        logging.info(f"Jetson Linux 압축 파일 발견: {jetson_linux_tbz}")
                        logging.info(f"[ACTION] '{work_base}' 경로에 압축을 해제하여 Linux_for_Tegra를 생성합니다...")
                        self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, f"mkdir -p {self.get_sh_quote(work_base)}")
                        self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, f"tar -xpf {self.get_sh_quote(jetson_linux_tbz)} -C {self.get_sh_quote(work_base)}")

                        # Verify again after extraction
                        result_after_extract = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, check_dir_cmd)
                        if not (result_after_extract.stdout and "EXISTS" in result_after_extract.stdout.strip()):
                            logging.error(f"압축 해제 후에도 '{l4t_dir}'를 찾을 수 없습니다. 압축 파일에 문제가 있을 수 있습니다.")
                            return False
                        logging.info(f"압축 해제 후 L4T 디렉토리 확인 완료: {l4t_dir}")
                    else:
                        logging.error("Jetson Linux 압축 파일(Jetson_Linux_R35.6.1_aarch64.tbz2)을 찾을 수 없어 L4T 디렉토리를 생성할 수 없습니다.")
                        return False
                else:
                    logging.info(f"올바른 버전의 L4T 디렉토리를 이미 확인했습니다: {l4t_dir}")

                # 4. Final checks and cleanup (This is the key fix for the 'mknod' error)
                logging.info("rootfs 디렉토리를 확인하고 이전 내용을 정리합니다.")
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"mkdir -p {self.get_sh_quote(l4t_dir + '/rootfs')}")
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"rm -rf {self.get_sh_quote(l4t_dir + '/rootfs/*')}")
                logging.info("rootfs 디렉토리 정리 완료.")
                # === End of robust preparation v2 ===

                # sdkmanager_dependencies
                sdkmanager_dependencies = [
                    UbuntuPakageName.qemu_user_static,
                    UbuntuPakageName.binfmt_support,
                    UbuntuPakageName.bzip2,
                    UbuntuPakageName.xz_utils,
                    UbuntuPakageName.gzip,
                    UbuntuPakageName.tar,
                    UbuntuPakageName.pv,
                    UbuntuPakageName.expect,
                    UbuntuPakageName.curl,
                    UbuntuPakageName.zip,
                    UbuntuPakageName.unzip,
                    UbuntuPakageName.parted,
                    UbuntuPakageName.gdisk,
                    UbuntuPakageName.dosfstools,
                    UbuntuPakageName.e2fsprogs,
                    UbuntuPakageName.util_linux,
                    UbuntuPakageName.uuid_runtime,
                    UbuntuPakageName.kmod,
                    UbuntuPakageName.udev,
                    UbuntuPakageName.python3,
                    UbuntuPakageName.ca_certificates,
                    UbuntuPakageName.binutils,
                    UbuntuPakageName.build_essential,
                    UbuntuPakageName.libxml2_utils,
                    UbuntuPakageName.android_sdk_libsparse_utils,
                    UbuntuPakageName.abootimg,
                    UbuntuPakageName.liblz4_tool,
                    UbuntuPakageName.python3_apt,
                    UbuntuPakageName.rsync,
                    UbuntuPakageName.cpio,
                    UbuntuPakageName.multipath_tools,
                    UbuntuPakageName.device_tree_compiler,
                    UbuntuPakageName.lzop,
                    UbuntuPakageName.zstd,
                    UbuntuPakageName.lsb_release,
                    UbuntuPakageName.kpartx,
                    UbuntuPakageName.lz4,
                    UbuntuPakageName.pigz,
                    UbuntuPakageName.python3_dev,
                    UbuntuPakageName.python3_distutils,
                    UbuntuPakageName.python3_venv,
                    UbuntuPakageName.sshpass,
                ]
                for pkg in sdkmanager_dependencies:
                    if not self.ensure_wsl_distro_ubuntu_pkg_installed(pkg):
                        logging.error(f"sdkmanager 의존성 패키지 {pkg.value}를 설치하는 데 실패했습니다. 프로세스를 중단합니다.")
                        return False
                logging.info("sdkmanager 의존성 패키지 설치를 완료했습니다.")

                # binfmt_misc 런타임 설정 (WSL 직접 실행)
                logging.info("binfmt_misc 런타임 설정을 확인 및 적용합니다 (WSL 직접 실행)...")
                distro_name = self._wsl.distro_name

                self.ensure_binfmt_qemu_aarch64_enabled(distro_name)
                logging.info("binfmt_misc(qemu-aarch64) 설정 완료.")

                # --- Rootfs /dev/random fix automation ---
                logging.info("Rootfs /dev/random 오류 방지를 위한 자동화된 복구 절차를 시작합니다.")
                distro_name = self._wsl.distro_name

                # n. Linux_for_Tegra 디렉토리 동적 탐색
                logging.info("Linux_for_Tegra 디렉토리를 탐색합니다...")
                wsl_temp_script = textwrap.dedent(r"""
                    set -euo pipefail
                    _s="$(mktemp /tmp/find_l4t.XXXXXX.sh)"
                    cat >"$_s"<<'EOF'
                    #!/usr/bin/env bash
                    set -euo pipefail

                    # n. WSL ext4 기본 위치
                    for base in "$HOME/nvidia/nvidia_sdk" "/root/nvidia/nvidia_sdk"; do
                      [ -d "$base" ] || continue
                      found="$(find "$base" -type d -name 'Linux_for_Tegra' -print -quit 2>/dev/null || true)"
                      if [ -n "$found" ]; then echo "$found"; exit 0; fi
                    done

                    # 2) 다른 사용자 홈(/home/*)
                    for base in /home/*/nvidia/nvidia_sdk; do
                      [ -d "$base" ] || continue
                      found="$(find "$base" -type d -name 'Linux_for_Tegra' -print -quit 2>/dev/null || true)"
                      if [ -n "$found" ]; then echo "$found"; exit 0; fi
                    done

                    # 3) Windows 경로(/mnt/c)
                    for base in \
                      /mnt/c/Users/*/nvidia/nvidia_sdk \
                      /mnt/c/Users/*/Downloads/nvidia/nvidia_sdk \
                      /mnt/c/Users/*/Documents/nvidia/nvidia_sdk \
                      /mnt/c/Users/*/Desktop/nvidia/nvidia_sdk
                    do
                      [ -d "$base" ] || continue
                      found="$(find "$base" -type d -name 'Linux_for_Tegra' -print -quit 2>/dev/null || true)"
                      if [ -n "$found" ]; then echo "$found"; exit 0; fi
                    done

                    # 4) 얕은 범위 fallback
                    found="$(find "$HOME" -maxdepth 4 -type d -name 'Linux_for_Tegra' -print -quit 2>/dev/null || true)"
                    if [ -n "$found" ]; then echo "$found"; exit 0; fi

                    found="$(find /mnt/c/Users -maxdepth 5 -type d -name 'Linux_for_Tegra' -print -quit 2>/dev/null || true)"
                    if [ -n "$found" ]; then echo "$found"; exit 0; fi

                    exit 1
                    EOF
                    chmod 0755 "$_s"
                    bash "$_s"; rc=$?; rm -f "$_s"; exit $rc
                """).strip()

                # n. Linux_for_Tegra 디렉토리 동적 탐색
                logging.info("Linux_for_Tegra 디렉토리를 탐색합니다...")
                distro_name = self._wsl.distro_name
                target_user_name = self._wsl.user_name if self._wsl.user_name != "root" else "pk"
                l4t_path = self.ensure_l4t_path_located(distro_name, target_user_name)
                if not l4t_path:
                    logging.warning("Linux_for_Tegra 디렉토리가 아직 없습니다. SDK Manager CLI를 먼저 실행해 내려받도록 합니다.")
                    self.ensure_sdkmanager_executed_on_wsl(setup_op=PkModesForSdkManager.CLI)
                    l4t_path = self.ensure_l4t_path_located(distro_name, target_user_name)
                    if not l4t_path:
                        logging.error("SDK Manager 실행 후에도 Linux_for_Tegra 디렉토리를 찾지 못했습니다. 다운로드/전개 완료 후 다시 시도해주세요.")
                        return False
                logging.info(f"Linux_for_Tegra 디렉토리 발견: {l4t_path}")

                # /dev/random/urandom 잔여물 정리
                self.ensure_rootfs_dev_random_fix(distro_name, l4t_path)

                user_to_search = self._wsl.user_name if self._wsl.user_name and self._wsl.user_name != 'root' else 'pk'
                l4t_path_result = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_to_search, wsl_temp_script)
                l4t_path = (l4t_path_result.stdout or "").strip()
                if not l4t_path:
                    logging.error("Linux_for_Tegra 디렉토리를 찾지 못했습니다. (일반 사용자 홈 포함 탐색)")
                    return False
                logging.info(f"Linux_for_Tegra 디렉토리 발견: {l4t_path}")
                if not l4t_path:
                    logging.error("Linux_for_Tegra 디렉토리를 찾을 수 없습니다. 플래시 작업을 중단합니다.")
                    return False
                logging.info(f"Linux_for_Tegra 디렉토리 발견: {l4t_path}")

                # n. Tegra_Linux_Sample-Root-Filesystem_*.tbz2 파일 동적 탐색
                logging.info("Tegra_Linux_Sample-Root-Filesystem_*.tbz2 파일을 탐색합니다...")
                find_tbz2_cmd = "find ~/Downloads/nvidia/sdkm_downloads -type f -name \"Tegra_Linux_Sample-Root-Filesystem_*.tbz2\" -print -quit"
                tbz2_path_result = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, target_user_name, find_tbz2_cmd)
                tbz2_path = tbz2_path_result.stdout.strip()
                if not tbz2_path:
                    logging.error("Tegra_Linux_Sample-Root-Filesystem_*.tbz2 파일을 찾을 수 없습니다. 플래시 작업을 중단합니다.")
                    return False
                logging.info(f"Rootfs .tbz2 파일 발견: {tbz2_path}")

                # 3. Linux_for_Tegra 디렉토리로 이동
                logging.info(f"작업 디렉토리를 {l4t_path}로 변경합니다.")
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"cd {l4t_path}")

                # 4. rootfs 디렉토리 정리
                logging.info("rootfs 디렉토리를 정리합니다...")
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, "rm -rf rootfs/*")

                # 5. rootfs 재전개
                logging.info("rootfs 파일을 재전개합니다...")
                tar_cmd = f"tar --xattrs --numeric-owner -xpf {tbz2_path} -C rootfs"
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, tar_cmd)

                # 6. l4t_flash_prerequisites.sh 실행
                logging.info("l4t_flash_prerequisites.sh 스크립트를 실행합니다...")
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, "./tools/l4t_flash_prerequisites.sh")

                # 7. apply_binaries.sh 실행
                logging.info("apply_binaries.sh 스크립트를 실행합니다...")
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, "./apply_binaries.sh")

                logging.info("Rootfs 복구 절차 완료.")
                # --- End of Rootfs /dev/random fix automation ---

                # --- SDKM Execution Mode Selection ---
                func_n = get_caller_name()
                sdk_mode_options = ["대화형 모드 (기존 --cli 방식)", "자동 스크립트 모드 (전체 자동 플래시)"]
                sdk_mode = ensure_value_completed(
                    key_name="sdk_execution_mode",
                    func_n=func_n,
                    options=sdk_mode_options,
                    guide_text="SDK Manager 실행 모드를 선택하세요:"
                )

                if sdk_mode == sdk_mode_options[0]:  # Interactive Mode
                    logging.info("대화형 모드로 SDK Manager를 실행합니다.")
                    self.ensure_sdkmanager_executed_on_wsl(setup_op=PkModesForSdkManager.CLI)

                elif sdk_mode == sdk_mode_options[1]:  # Automatic Script Mode
                    logging.info("자동 스크립트 모드로 플래시를 시작합니다.")

                    # Helper function to find paths
                    def find_path_in_wsl(find_cmd):
                        result = self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, find_cmd)
                        path = result.stdout.strip() if result.stdout and result.stdout.strip() else ""
                        return path

                    # n. Download only
                    logging.info("auto mode: 1. 파일 다운로드를 시작합니다 (downloadonly)...")
                    download_cmd = "sdkmanager --cli --action downloadonly --login-type devzone --product Jetson --target-os Linux --version 5.1.5 --show-all-versions --host --target JETSON_AGX_XAVIER_TARGETS --license accept"
                    self.ensure_command_executed_to_wsl_distro_as_user_account(distro_name, user_name, download_cmd)
                    logging.info("auto mode: 1. 파일 다운로드 완료.")

                    # Re-locate paths for safety
                    work_base = f"/home/{user_name}/nvidia/nvidia_sdk/JetPack_5.1.5_Linux_JETSON_AGX_XAVIER_TARGETS"
                    l4t_dir = f"{work_base}/Linux_for_Tegra"
                    find_sample_rootfs_cmd = "find ~/nvidia/nvidia_sdk ~/Downloads/nvidia/sdkm_downloads ~/.nvsdkm/sdkm_downloads -maxdepth 4 -type f -name 'Tegra_Linux_Sample-Root-Filesystem_R35.6.1_aarch64.tbz2' 2>/dev/null | head -n1"
                    sample_rootfs_tbz = find_path_in_wsl(find_sample_rootfs_cmd)

                    if not sample_rootfs_tbz:
                        logging.error("auto mode 오류: Sample RootFS 파일(Tegra_Linux_Sample-Root-Filesystem_R35.6.1_aarch64.tbz2)을 찾을 수 없습니다.")
                        return False

                    # n. Extract Sample RootFS
                    logging.info(f"auto mode: 2. Sample RootFS를 {l4t_dir}/rootfs에 압축 해제합니다...")
                    extract_rootfs_cmd = f"tar -xpf {self.get_sh_quote(sample_rootfs_tbz)} -C {self.get_sh_quote(l4t_dir + '/rootfs')}"
                    self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, extract_rootfs_cmd)
                    logging.info("auto mode: 2. Sample RootFS 압축 해제 완료.")

                    # 3. Apply Binaries (with fallback)
                    logging.info("auto mode: 3. 바이너리를 적용합니다 (apply_binaries.sh)...")
                    apply_cmd = f"cd {self.get_sh_quote(l4t_dir)} && ./apply_binaries.sh"
                    try:
                        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, apply_cmd)
                    except subprocess.CalledProcessError:
                        logging.warning("apply_binaries.sh 1차 실패. binfmt-support를 재시작하고 다시 시도합니다.")
                        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, "update-binfmts --enable qemu-aarch64 || true")
                        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, "service binfmt-support restart || true")
                        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, apply_cmd)  # Retry
                    logging.info("auto mode: 3. 바이너리 적용 완료.")

                    # 4. Flash
                    logging.info("auto mode: 4. 플래시를 시작합니다 (flash.sh)...")
                    flash_cmd = f"cd {self.get_sh_quote(l4t_dir)} && ./flash.sh jetson-agx-remote_target-devkit mmcblk0p1"
                    self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, flash_cmd)

                    logging.info("자동 플래시 스크립트가 완료되었습니다.")

                # pk_development_history :
                # -> Ubuntu-18.04 LTS install -> Microsoft Store -> Ubuntu-18.04 -> 설치 -> 열기 -> type id -> type pw -> retype pw
                # -> attach fail -> reattach -> attach fail ->reboot  -> reattach -> attach fail -> persist 에서 APX 가 사라지지 않음 -> usbipd remove  -> reattach -> attach success
                # -> sdkmanager execution fail -> sdkmanager 로그인-> sdkmanager 종료 -> sdkmanager 재접속 -> sdkmanager execution success
                # -> flash fail -> usb bridge timing issue  -> usbipd bind 단계 --force 옵션` 지우기 -> reflash -> flash succeeded
                # -> flash fail -> uninstall 5.1.5 of HOST Machine and Target H/W
                # -> flash fail ->  sdkmanager--cli/install -> default 옵션 설치
                # -> flash fail ->  DeepStream not installed
                # -> flash fail ->  Jetson SDK Component not installed
                # -> flash fail ->  warm reset -> reflash -> flash success
                # -> flash fail -> debug -> usb bridge timing issue discovered -> Warm Reset -> reflash -> flash success
                # -> 5.1.5 flash fail -> Warm Reset -> 5.1.5 reflash -> flash succeeded -> but, terminal not opened -> tty terminal(ctrl alt f2~f6 ?) 로 접속 -> 중도포기
                # -> 5.1.5 flash success -> login ok -> terminal not open -> AGX Xavier old revision problem 으로 판단-> 5.1.5 사용 forgive
                # -> 4.6.6 flash -> not tried yet
                # -> target hardware ssh 접속허용 -> not tried yet
                # -> 5.1.5 flash fail -> wsl distro reinstall -> not tried yet
                # -> 5.1.5 flash fail -> dependency fail ->

                # dependency check and install
                # pkgs="qemu-user-static binfmt-support bzip2 xz-utils gzip tar pv expect curl zip unzip parted gdisk dosfstools e2fsprogs util-linux uuid-runtime kmod udev python3 ca-certificates"
                # pkgs="qemu-user-static binfmt-support bzip2 xz-utils gzip tar pv expect curl zip unzip parted gdisk dosfstools e2fsprogs uuid-runtime kmod udev python3 ca-certificates"
                # for p in $pkgs; do dpkg -s $p >/dev/null 2>&1 && echo "[OK] $p" || echo "[MISSING] $p"; done
                # [OK] qemu-user-static
                # [OK] binfmt-support
                # [OK] bzip2
                # [OK] xz-utils
                # [OK] gzip
                # [OK] tar
                # [MISSING] pv
                # [MISSING] expect
                # [OK] curl
                # [MISSING] zip
                # [MISSING] unzip
                # [OK] parted
                # [OK] gdisk
                # [OK] dosfstools
                # [OK] e2fsprogs
                # [OK] uuid-runtime
                # [OK] kmod
                # [OK] udev
                # [OK] python3
                # [OK] ca-certificates
                # sudo apt update && sudo apt install -y $pkgs

                # usb bridge timing issue debugging routine:

                # mkr..
                # flash 로그 검증
                # wsl -d Ubuntu-18.04
                # ls -al ~/.nvsdkm/
                # find ~ -type f \( -name "*.log" -o -name "*.txt" \) -iname "*flash*" 2>/dev/null | head -50
                # find ~/.nvsdkm/replays -type f \( -name "*.log" -o -name "*.txt" \) 2>/dev/null | head -50
                # less ~/.nvsdkm/sdkm.log # 전체로그확인
                # grep -nEi 'fail|error|dependency|filesystem|kernel_flash|tegraflash|loop|no space|permission|udev|usb' ~/.nvsdkm/sdkm-*.log | tail -n 80
                # 다운로드 검증단계 로그
                # ls -lt ~/.nvsdkm/downloadLogs | head -n 20
                # less "$(ls -t ~/.nvsdkm/downloadLogs/* | head -n1)"
                # tail -n 100 ~/.nvsdkm/sdkm.log   # 마지막 100줄
                # tail -n 100 "$(ls -t ~/.nvsdkm/sdkm-*.log | head -n1)" | clip.exe   # 마지막 100줄
                # LOG="$(ls -t ~/.nvsdkm/sdkm-*.log | head -n1)"

                # echo "LOG => $LOG"
                # sed -n '/NV_L4T_FILE_SYSTEM_AND_OS_COMP@JETSON_AGX_XAVIER_TARGETS/,/install ended/p' "$LOG" | sed -n '1,400p'
                # sed -n '/NV_L4T_FILE_SYSTEM_AND_OS_COMP@JETSON_AGX_XAVIER_TARGETS/,/install ended/p' "$LOG" | grep -nEi 'fail|error|denied|permission|space|no space|tar|chroot|dpkg|qemu|binfmt|mount|mkfs|losetup|loop|udev' | clip.exe

                # Cold Boot :
                # RECOVERY + PWR 버튼조합 기반 RCM 진입 (Cold Boot) -> 5.1.5 flash fail
                # → 전원 켜질 때 BootROM이 RECOVERY 핀을 HIGH로 감지하면 RCM 모드 진입.
                # (RESET 안 쓰고도 가능하지만, 완전히 전원이 꺼진 상태에서만 유효)

                # Warm Reset :
                # RECOVERY + RESET 버튼조합 기반 RCM 진입 (Warm Reset) -> 5.1.5 flash success -> login ok -> terminal not open
                # → 이미 전원이 들어온 상태에서 강제로 다시 시작하면서 Recovery 핀 상태를 읽게 함.
                # → '전원 전체 OFF/ON 하지 않고도 RCM 모드 진입' 가능.
                # → 개발자가 보통 플래싱할 때 이 방식을 많이 씀.
                # reflash fail ->  (usbipd 재설치/reboot /target jetpack reinstall/host jetpack reinstall) -> reflash fail -> warm reset -> reflash success

                # def ensure_nvidia_developer_login():
                #     smart phone 에서 QR 촬영을 해서 smart phone web 열리면 로그인
                #     다른거 치라는데 패스워드 치면 됨.
                #     로그인 되면서 device type select 창이 나옴.
                #     Jetson AGX Xavier
                #     OK
                #     Later
                #     while True:
                #     튜토리얼 로그인웹이 자동으로 안열리는 경우, reboot 부터 해보자, QR code 로 시도

                # ensure_sdkmanager_success_history_routine_followed()
                #     Install
                #     Jetson
                #     Target Hardware
                #     Jetson AGX Xavier modules
                #     y
                #     5.1.5 # Jetpack Version
                #     OEM Configuration/pre-config : default # 10% 대에서 fail, reboot 후 재시도는 시도해볼 필요 있음.
                #     Storage Device: EMMC (Default)
                #     OEM Configuration/Runtime 는 진행하지 않음.
                #     OEM Configuration/Runtime
                #     ensure ubuntu OEM
                #     evm
                #     EVM terminal x
                #     accept blah lisence
                #     display on
                #     agree
                #     english
                #     english(US)
                #     english(US)
                #     seoul
                #     nvidia
                #     nvidia
                #     nvidia
                #     nvidia
                #     nvidia

                # todo : flash fail 시에 자동로깅   clip.exe 로 마지막줄은 2번 실행
                # LOG="$(ls -t ~/.nvsdkm/sdkm-*.log | head -n1)"
                # COMP='NV_L4T_FILE_SYSTEM_AND_OS_COMP@JETSON_AGX_XAVIER_TARGETS'
                # {
                #   echo "==== $LOG ($COMP) ===="
                #   sed -n "/$COMP/,/install ended/p" "$LOG" | sed -n '1,400p'
                #   echo "---- tail errors ----"
                #   grep -nEi 'fail|error|denied|permission|space|tar|chroot|dpkg|qemu|binfmt|mount|mkfs|losetup|loop|udev' "$LOG" | tail -n 200
                # } | sed -e 's/\r//g'

                # LOG="$(ls -t ~/.nvsdkm/sdkm-*.log | head -n1)"
                # COMP='NV_L4T_FILE_SYSTEM_AND_OS_COMP@JETSON_AGX_XAVIER_TARGETS'
                # {
                #   echo "==== $LOG ($COMP) ===="
                #   sed -n "/$COMP/,/install ended/p" "$LOG" | sed -n '1,400p'
                #   echo "---- tail errors ----"
                #   grep -nEi 'fail|error|denied|permission|space|tar|chroot|dpkg|qemu|binfmt|mount|mkfs|losetup|loop|udev' "$LOG" | tail -n 200
                # } | sed -e 's/\r//g' | clip.exe

                # def ensure_target_hardware_customized_for_jung_hoon_park()
                # set evm network wired connection 1 as 192.168.2.124 22 192.168.1.1 8.8.8.8 manualy in evm
                # sudo apt update
                # ensure MAXN
                # ensure log in automatically
                # ensure passwd set  target Hardware pw 는 필요.

                # ensure stack size 10240 #MEMORY LEAK 예방 #10240로 합의
                # sudo vi /etc/security/limits.conf
                # #End of file
                # nvidia hard stack 10240
                # nvidia soft stack 10240
                # ubuntu hard stack 10240
                # ubuntu soft stack 10240
                # root hard stack 10240
                # root soft stack 10240
                # :wq
                # cat /etc/security/limits.conf

                # ensure ntp available
                # sudo vi /etc/systemd/timesyncd.conf
                # [Time]
                # NTP=192.168.10.10 #server ip(control PC)
                # FallbackNTP=ntp.ubuntu.com
                # RootDistanceMaxSec=15 #5→15
                # PollIntervalMinSec=32
                # PollIntervalMaxSec=2048
                # # timedatectl set-ntp no #자동 시간동기화 해제
                # # date
                # # timedatectl set-time "2024-10-28 13:26:00" #수동 시간 SETTING

                # if not ensure_remote_target_auto_rebootable:
                #     ssh command -> restart
                #     wait ssh connection success
                #     while True:
                #         enure_guide_auto_power_pin_connected_performed():

                pass
            #         ensure_remote_os_connection(wsl)  # test_ip
            #         ensure_os_locked()
            #         ensure_screen_black_never()
            #         ensure_maxn()
            #         reboot_vpc()
            #             gen_target_flash_image()
            #
            #         elif not self.is_target_flash_image_exists():
            #             # cd
            #             # cmd = "cd ~/Downloads/flash/xc_flash/Linux_for_Tegra/"
            #             # ensure_command_to_wsl_distro_like_human_deprecated(cmd=cmd, distro_name=target_device_data_os_n, wsl_window_title_seg=wsl_window_title_seg, exit_mode=exit_mode)
            #
            #             # ensure system.img* and system.img.raw
            #             ensure_location_about_system_img_and_system_img_raw(wsl)
            #
            #             # flash
            #             cmd = rf"echo {wsl_pw} | sudo -S ./flash.sh -r jetson-remote_target mmcblk0p1"
            #             ensure_command_to_wsl_distro_like_human_deprecated(cmd=cmd, distro_name=wsl.selected,
            #                                                 wsl_window_title_seg=wsl_window_title_seg)
            #
            #             # sudo mv /home/pk_system/Downloads/flash/xc_flash/Linux_for_Tegra/system.img* /home/pk_system/Downloads/flash/xc_flash/Linux_for_Tegra/rootfs/bin/
            #
            #             # cmd = rf'sudo find -type f -name "system.img*"'
            #             # cmd_to_wsl_like_human(cmd=cmd, distro_name=distro_name, wsl_window_title_seg=wsl_window_title_seg)
            #             #
            #             # cmd_to_wsl_like_human(cmd = rf'df -h', distro_name=distro_name, wsl_window_title_seg=wsl_window_title_seg)
            #             # ensure_command_executed(cmd = rf'explorer \\wsl$')
            #
            #             logging.debug(rf'''FLASH : This function took {elapsed_minutes} minutes  ''')
            #             # todo : elapsed_minutes 이걸 f에 매번 기록, 공정시간 자동통계
            #             # 해당공정이 통계시간보다 느리거나 빠르게 종료되었다는 것을 출력 하도록
            #
            #         check_manual_task_iteractively(question=rf'''DID YOU EXIT WSL ATTACH PROGRAM AT LOCAL?  %%%FOO%%%''')
            #         # todo : 플래시이미지 재생성 후 해당 내용 네트워크 설정 자동화 후 추후삭제예정
            #         check_manual_task_iteractively(question=rf'''DID YOU SET WIRED CONNECTION 3 AS {target_device_wired_connection_3_new} ?  %%%FOO%%%''')
            #         ensure_target_side_mode(target_device_data=self, wsl)
            #         if not ensure_target_accessable(self, wsl):
            #             # history : ensure_target_accessable() 수행 -> target_device 접속안됨 -> Wired Connection 활성화 실패->gui 통해서 2.76 으로 ssh 접속 시도->fail->flash 재수행->success
            #             # flash 재수행해야 하는 경우로 판단
            #             continue

            return True
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
        finally:
            ensure_spoken(read_finished_wait_mode=True)

    def ensure_self_info_printed(self):
        """Prints all fields of the PkWirelessTargetManager (self) in pretty JSON format."""
        import logging
        import json

        self_dict = {
            "identifier": self.identifier.value if self.identifier else None,
            "nick_name": self.nick_name,
            "state": self.state.name if self.state else None,
            "ip": getattr(self, 'ip', None),
            "hostname": getattr(self, 'hostname', None),
            "port": getattr(self, 'port', None),
            "user_n": getattr(self, 'user_n', None),
            "f_local_ssh_public_key": str(getattr(self, 'f_local_ssh_public_key', None)),
            "f_local_ssh_private_key": str(getattr(self, 'f_local_ssh_private_key', None)),
            # Password ('pw') is intentionally omitted for security.
        }

        pretty_json = json.dumps(self_dict, indent=4, ensure_ascii=False)
        logging.debug(f"PkWirelessTargetManager (self) info:\n{pretty_json}")
        return pretty_json

    def ensure_target_recovery_mode_entered(self):
        # RCM MODE
        import logging
        import re
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        func_n = get_caller_name()
        if self._wired_target.identifier == PkDevice.jetson_agx_xavier:
            bus_id = None
            # ensure_spoken(get_easy_speakable_text(question))
            while True:
                if is_os_windows():
                    cmd = "usbipd.exe list"
                    souts, _ = ensure_command_executed(cmd=cmd, encoding='utf-8')
                    device_signature = "APX"
                    # 정규표현식을 사용하여 BUSID, VID:PID, DEVICE, STATE를 정확히 파싱
                    line_pattern = re.compile(r"^\s*([0-9\-]+)\s+([0-9a-fA-F]{4}:[0-9a-fA-F]{4})\s+(.*?)\s{2,}(.*)$")
                    logging.debug("--- 'usbipd list' 출력 파싱 시작 ---")
                    if not souts:
                        logging.warning("'usbipd list' 명령어의 출력이 없습니다.")
                    for line in souts:
                        if not line.strip():
                            continue
                        logging.debug(f"target line to parse='{line}'")
                        match = line_pattern.match(line)
                        if match:
                            logging.debug(f"line is matched with expected pattern")
                            parsed_bus_id = match.group(1)
                            parsed_vid_pid = match.group(2)
                            parsed_device = match.group(3).strip()
                            parsed_state = match.group(4).strip()

                            logging.debug(f"파싱 결과: BUSID={parsed_bus_id}, VID:PID={parsed_vid_pid}, DEVICE='{parsed_device}', STATE='{parsed_state}'")

                            if device_signature in parsed_device:
                                bus_id = parsed_bus_id
                                logging.info(f"타겟 장치 '{device_signature}' 발견. BUSID: {bus_id}")
                                return bus_id
                        else:
                            logging.debug(f"line is not matched with expected pattern")
                    if bus_id is None:
                        # pk_* -> monitor
                        # ensure_command_executed(cmd=rf'start "{self.window_title_temp}" wsl watch -n 0.3 usbipd.exe list', mode='a')
                        # while True:
                        #     if is_window_opened(window_title_seg=self.window_title_temp):
                        #         break
                        #     ensure_slept(milliseconds=77)

                        # pk_* -> monitor advanced

                        target_file = D_PK_WRAPPERS / "pk_ensure_stand_output_streams_watched.py"
                        ensure_pk_python_file_executed_in_uv_venv_windows(target_file)
                        while True:
                            if is_window_opened(window_title_seg=get_nx(target_file)):
                                break
                            ensure_slept(milliseconds=77)

                        # pk_* -> 튜토리얼
                        guide_title = "리커버리 모드 진입"
                        logging.warning("Could not find a device with the required signature (APX) from 'usbipd list' output.")
                        logging.warning(get_text_yellow("타겟 장치(APX)를 찾을 수 없습니다."))
                        ensure_window_to_front(window_title_seg=get_current_console_title())
                        guide_text = textwrap.dedent(rf'''
                            # {guide_title} 수동튜토리얼
    
                            ## RECOVERY MODE ENTRY ROUTINE WITH SAFE FOR JETSON AGX XAVIER 
                            n. If possible, please power off Xavier using the "poweroff" command.
                            n. press power button. if device turn off, release power button 
                            n. remove power (Xavier/carrier board/배럴 잭)
                            n. remove auto power selector pin
                            n. connect power cable (Xavier/carrier board/배럴 잭)
                            n. connect data cable (PC/USB PORT, Xavier/carrier board/WHITE LED INDICATOR SIDE USB PORT(C))
                            n. hold the RECOVERY button  # ccw button (center button)
                            n. press power button. if device turn on, release buttons
                            n. reinstall auto power mode selector pin
    
                        ''')
                        logging.warning(get_text_yellow(guide_text))
                        question = f'{guide_title} 수동튜토리얼를 완료하셨나요'
                        ok = ensure_value_completed(key_name=question, func_n=func_n, options=[PkTexts.YES, PkTexts.NO, PkTexts.FAILED], guide_text=guide_text)
                        if ok == PkTexts.YES:
                            continue
                        elif ok == PkTexts.NO:
                            ensure_spoken(get_easy_speakable_text(f'{guide_title}를 반드시 수행해야 다음으로 진행할 수 있습니다'))
                            continue
                        elif ok == PkTexts.FAILED:
                            guide_title = f'{guide_title} 트러블슈팅'
                            guide_text = textwrap.dedent(rf'''
                                # {guide_title} 수동튜토리얼
                                n. 플래시 케이블 연결안함
                                n. 네트워크 케이블 remove 후 재시도
                            ''')
                            logging.debug(get_text_yellow(guide_text))
                            ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                            if ok != PkTexts.YES:
                                ensure_spoken(get_easy_speakable_text(f'{guide_title}를 반드시 수행해야 다음으로 진행할 수 있습니다'))
                                continue
        else:
            # 다른 디바이스
            ensure_not_prepared_yet_guided()
            # TODO jetpack update" via sdkmanager #원격으로 jetpack 업데이트 가능#usb방식 가능?

    def ensure_target_info_printed(self):
        logging.debug(f'self.target.to_json()={self._wired_target.to_json()}')
        return

    def ensure_target_effective_info_printed(self):
        """
        Print only non-None fields of target in pretty JSON format.
        """
        import logging
        import json

        # target 객체 → dict
        target_dict = self._wired_target.to_dict()

        # None 값 제거
        effective_dict = {k: v for k, v in target_dict.items() if v is not None}

        # JSON 문자열 변환
        pretty_json = json.dumps(effective_dict, indent=4, ensure_ascii=False)

        logging.debug(pretty_json)
        return pretty_json

    def ensure_self_effective_info_printed(self):
        """
        Print only non-None fields of the PkWirelessTargetManager (self) in pretty JSON format.
        """
        import logging
        import json

        # Manually construct a dictionary from self's attributes
        self_dict = {
            "identifier": self.identifier.value if self.identifier else None,
            "nick_name": self.nick_name,
            "state": self.state.name if self.state else None,
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

        logging.debug(f"PkWirelessTargetManager (self) effective info:\n{pretty_json}")
        return pretty_json

    def ensure_usbipd_installed(self):
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

        if F_USBPIPD_MSI.exists():
            ensure_command_executed(rf'start "" {F_USBPIPD_MSI}')
            # pk_* -> seconds_limited loop
            is_found = ensure_signature_found_in_souts_for_milliseconds_limited(
                cmd=rf"usbipd --version",
                signature=".master.",
                milliseconds_limited=get_milliseconds_from_seconds(seconds=30),
            )
            if is_found:
                return True

        guide_title = "usbipd-win 설치"
        question = f"'{guide_title}' 튜토리얼를 모두 완료하고 uspipd가 준비되었습니까?"
        ensure_spoken(get_easy_speakable_text(f"{guide_title}를 시작합니다. 웹페이지를 확인해주세요."))

        # Open the download page once at the beginning
        ensure_command_executed("explorer https://github.com/dorssel/usbipd-win/releases")
        while True:
            guide = textwrap.dedent(f'''
                        # {guide_title} 수동 튜토리얼 (usbipd-win_5.2.0_x64.msi 파일사용 가정)
                        n. 방금 열린 웹페이지/Assets/usbipd-win_5.2.0_x64.msi 클릭
                        n. 다운로드된 usbipd-win_5.2.0_x64.msi 클릭 후 설치창의 절차진행
                        n. cmd.exe 또는 PowerShell 터미널에서  `usbipd --version`  5.2.0-45+Branch.master.Sha.e37737bfa2c8bafbe33674fc32eda3857dab6893.e37737bfa2c8bafbe33674fc32eda3857dab6893 이런 해시 형태의 버전이 나오면 정상설치완료
                    ''')
            logging.info(get_text_cyan(guide))

            ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO])

            if ok == PkTexts.YES:
                logging.info("사용자가 설치 완료를 확인했습니다. uspipd 상태를 다시 확인합니다...")
                if self.get_uspipd_version():
                    logging.info("usbipd가 성공적으로 확인되었습니다.")
                    ensure_spoken(get_easy_speakable_text("usbipd가 성공적으로 확인되었습니다."), read_finished_wait_mode=True)
                    return True
                else:
                    logging.error("오류: 사용자가 완료를 확인했지만, 여전히 uspipd를 사용할 수 없습니다.")
                    troubleshooting_guide = textwrap.dedent(f'''
                                # {guide_title} 트러블슈팅
                                n. PC를 reboot 한 후 `usbipd` 명령어 시도.
                                n. PowerShell 세션을 닫고 `usbipd` 명령어 시도.
                                n. PowerShell(관리자)에서 `usbipd` 명령어 시도.
                                n. target이 PC에 올바르게 연결되어 있는지 확인해주세요.(wsl 의 경우는 상관없어요) 
                            ''')
                    logging.warning(get_text_yellow(troubleshooting_guide))
                    ensure_spoken(get_easy_speakable_text("설치 확인에 실패했습니다. 트러블슈팅 튜토리얼를 확인하고 재시도해주세요."), read_finished_wait_mode=True)
                    continue
            else:  # PkTexts.NO or other
                ensure_spoken(get_easy_speakable_text(f'{guide_title}를 반드시 수행해야 다음으로 진행할 수 있습니다.'))
                # Loop will continue

    def is_usbipd_enabled(self):
        import subprocess
        import logging
        try:
            command = ["usbipd", "list"]
            logging.debug(f"Executing command: {' '.join(command)}")

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8',
                errors='ignore'
            )

            if result.returncode == 0:
                logging.info("usbipd-win is enabled and accessible.")
                return True
            else:
                logging.warning(f"'usbipd wsl list' command failed with return code {result.returncode}.")
                if result.stderr:
                    logging.debug(f"usbipd stderr: {result.stderr.strip()}")

                # Automatically check the service status for better diagnostics
                try:
                    sc_command = ["sc", "query", "usbipd"]
                    sc_result = subprocess.run(sc_command, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore')
                    service_status = sc_result.stdout.strip()
                    logging.debug(f"Checking service status for 'usbipd':\n{service_status}")

                    if "STOPPED" in service_status:
                        logging.error("The 'usbipd' service is stopped. Please start it by running 'sc start usbipd' in a terminal with administrator privileges.")
                    elif "RUNNING" in service_status:
                        logging.warning("The 'usbipd' service is running, but the command failed. This might be a permissions issue or a problem with the WSL integration.")
                    else:
                        logging.warning("Could not determine the state of the 'usbipd' service, but the command failed.")

                except FileNotFoundError:
                    logging.error("'sc.exe' not found. Cannot automatically check the service status.")
                except Exception as sc_e:
                    logging.error(f"An unexpected error occurred while checking the usbipd service status: {sc_e}")
                return False

        except FileNotFoundError:
            logging.error(
                "The 'usbipd' command was not found. "
                "Please ensure usbipd-win is installed and its location is included in the system's PATH environment variable."
            )
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred while checking usbipd-win status: {e}")
            return False

    def get_uspipd_version(self):
        """
        Checks for usbipd-win version on Windows by running 'usbipd --version'.
        Returns the version string if found, otherwise None.
        """
        import subprocess
        import logging
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

        if not is_os_windows():
            logging.debug("get_uspipd_version is only supported on Windows.")
            return None

        try:
            # Execute the command to get the version
            result = subprocess.run(
                ["usbipd", "--version"],
                capture_output=True,
                text=True,
                check=True,  # Raises CalledProcessError for non-zero exit codes
                encoding='utf-8',
                errors='ignore'
            )
            # The output is typically just the version string
            version = result.stdout.strip()
            if version:
                logging.debug(f"Found usbipd-win version: {version}")
                return version
            else:
                logging.warning("'usbipd --version' command ran but returned empty output.")
                return None

        except FileNotFoundError:
            # This means the 'usbipd' command was not found in the system's PATH
            logging.warning("'usbipd' command not found. usbipd-win may not be installed or not in PATH.")
            return None
        except subprocess.CalledProcessError as e:
            # This means the command executed but returned an error
            logging.error(f"The 'usbipd --version' command failed: {e.stderr}")
            return None
        except Exception as e:
            # Catch any other unexpected errors
            logging.error(f"An unexpected error occurred while checking usbipd version: {e}")
            return None

    def ensure_sdkmanager_installed(self):
        """
        Ensures NVIDIA SDK Manager is installed in the WSL distro.
        Checks for existing file before guiding the user to download it, then copies and installs it.
        """
        import logging
        import os
        from pathlib import Path
        import glob
        from pk_internal_tools.pk_objects.pk_directories import D_PK_LINUX_TOOLS, D_PK_EXTERNAL_TOOLS

        distro_name = self._wsl.distro_name
        wsl_user_n = self._wsl.user_name if self._wsl.user_name != "root" else "pk"  # pk_option
        wsl_user_home = f"/home/{wsl_user_n}"

        # Define the correct check command once
        check_cmd = f'wsl -d {distro_name} -- sdkmanager --ver'

        # n. Check if sdkmanager command is already installed
        stdout, stderr = ensure_command_executed(check_cmd)
        # If the command produces any output on stdout and no errors, consider it successful.
        if stdout and not stderr:
            logging.info(f"sdkmanager is already installed in {distro_name}. Version: {' '.join(stdout)}")
            return True

        # n. Define search paths and perform an initial search for the .deb file
        downloads_path = Path(os.path.expanduser("~")) / "Downloads"
        fallback_paths = [D_PK_LINUX_TOOLS, D_PK_EXTERNAL_TOOLS]
        search_paths = [downloads_path] + fallback_paths

        sdkmanager_debs = []
        for path in search_paths:
            logging.info(f"Searching for sdkmanager_*.deb in {path}...")
            found_debs = glob.glob(str(path / "sdkmanager_*.deb"))
            if found_debs:
                sdkmanager_debs.extend(found_debs)
                logging.info(f"Found {len(found_debs)} .deb file(s) in {path}.")
                break

        # n. If not found, guide user to download
        if not sdkmanager_debs:
            guide_title = "NVIDIA SDK Manager 다운로드"
            question = f"'{guide_title}'를 완료했습니까? (sdkmanager_*.deb 파일)"
            download_url = "https://developer.nvidia.com/nvidia-sdk-manager"
            ensure_spoken(get_easy_speakable_text(f"{guide_title}를 시작합니다. 웹페이지를 열고 로그인 후 DEB 파일을 다운로드하세요."))
            ensure_command_executed(f"explorer {download_url}")

            while True:
                guide = textwrap.dedent(f'''
                    # {guide_title} 수동 튜토리얼
                    1. 방금 열린 웹페이지({download_url})에서 로그인하세요.
                    2. 'SDK Manager'를 찾아 DEB 패키지(.deb)를 다운로드하세요.
                    3. 다운로드가 완료되면 터미널로 돌아와 질문에 답변해주세요.
                ''')
                logging.info(get_text_cyan(guide))
                ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                if ok != PkTexts.YES:
                    ensure_spoken(get_easy_speakable_text(f'{guide_title}를 반드시 수행해야 다음으로 진행할 수 있습니다.'))
                    continue

                # Search again after user confirmation
                for path in search_paths:
                    found_debs = glob.glob(str(path / "sdkmanager_*.deb"))
                    if found_debs:
                        sdkmanager_debs.extend(found_debs)
                        break

                if sdkmanager_debs:
                    break  # Exit download loop if file is found
                else:
                    logging.error(f"다음 경로들에서 sdkmanager 데비안 파일을 찾을 수 없습니다: {[str(p) for p in search_paths]}")
                    ensure_spoken("SDK Manager 파일을 찾지 못했습니다. 다시 시도해주세요.")
                    continue

        # n. Proceed with copy and installation if the file was found
        latest_deb_path = max(sdkmanager_debs, key=os.path.getmtime)
        latest_deb_file_name = Path(latest_deb_path).name
        logging.info(f"Using SDK Manager DEB file: {latest_deb_path}")

        wsl_downloads_dir_host_path = Path(f"//wsl.localhost/{distro_name}{wsl_user_home.replace('/', '//')}/Downloads")
        ensure_command_executed(f"wsl -d {distro_name} -- mkdir -p {wsl_user_home}/Downloads")

        logging.info(f"Copying {latest_deb_file_name} to WSL ({wsl_downloads_dir_host_path})...")
        copy_cmd = f'copy "{latest_deb_path}" "{wsl_downloads_dir_host_path}"'
        stdout, stderr = ensure_command_executed(copy_cmd)
        if stderr and "지정된 파일을 찾을 수 없습니다" not in " ".join(stderr):
            logging.error(f"Failed to copy file to WSL: {stderr}")
            ensure_spoken("파일을 WSL로 복사하는 데 실패했습니다.")
            return False

        wsl_deb_path = f"{wsl_user_home}/Downloads/{latest_deb_file_name}"
        logging.info(f"Installing {latest_deb_file_name} in WSL...")
        install_cmd = f'wsl -d {distro_name} --user {wsl_user_n} -- sudo apt install -y {wsl_deb_path}'
        stdout, stderr = ensure_command_executed(install_cmd)

        if stderr and ("Err:" in " ".join(stderr) or "E:" in " ".join(stderr)):
            logging.error(f"Failed to install sdkmanager in WSL: {stderr}")
            logging.info("`apt install` failed, falling back to `dpkg -i`...")
            install_cmd_dpkg = f'wsl -d {distro_name} --user {wsl_user_n} -- sudo dpkg -i {wsl_deb_path}'
            stdout_dpkg, stderr_dpkg = ensure_command_executed(install_cmd_dpkg)
            if stderr_dpkg:
                logging.error(f"dpkg installation also failed: {stderr_dpkg}")
                ensure_spoken("SDK Manager 설치에 최종 실패했습니다.")
                return False

            logging.info("Fixing broken dependencies after dpkg...")
            ensure_command_executed(f'wsl -d {distro_name} --user {wsl_user_n} -- sudo apt-get install -f -y')

        # n. Final verification
        logging.info("Verifying sdkmanager installation...")
        stdout, stderr = ensure_command_executed(check_cmd)
        if stdout and not stderr:
            logging.info(f"Successfully installed sdkmanager in {distro_name}. Version: {' '.join(stdout)}")
            ensure_spoken("SDK Manager 설치를 완료했습니다.")
            return True
        else:
            logging.error("Verification failed after installation attempt.")
            logging.error(f"Stdout: {stdout}")
            logging.error(f"Stderr: {stderr}")
            ensure_spoken("SDK Manager 설치 후 확인에 실패했습니다.")
            return False

    def get_sh_quote(self, s: str) -> str:
        # TODO renaming
        return "'" + s.replace("'", "'\"'\"'") + "'"

    def ensure_binfmt_qemu_aarch64_enabled(self, distro_name: str) -> bool:
        """
        WSL 내부에서 aarch64 ELF를 qemu-aarch64-static로 자동 실행되도록 binfmt_misc를 보장한다.
        1) qemu-user-static, binfmt-support 설치
        2) binfmt_misc 마운트
        3) (우선) update-binfmts --install → --import → --enable 로 DB 등록/활성화 시도
        4) 실패 시 커널 인터페이스(/proc/sys/fs/binfmt_misc/register)에 직접 등록(printf | tee)
        5) /proc/sys/fs/binfmt_misc/qemu-aarch64 존재로 최종 검증
        """
        import logging
        import subprocess

        MAGIC = r'\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\xb7\x00'
        MASK = r'\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xff'
        ENTRY = f":qemu-aarch64:M::{MAGIC}:{MASK}:/usr/bin/qemu-aarch64-static:CF"

        def _run_root(cmd: str):
            # 공통 실행 (root로 sh -lc); 내부에서 로깅/체크까지 수행
            return self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, cmd)

        logging.info("binfmt_misc 런타임 설정을 확인 및 적용합니다 (WSL 내부).")

        # 0) 필수 바이너리 존재 확인 및 패키지 설치
        try:
            # qemu-user-static, binfmt-support 설치 (이미 설치되어 있으면 내부 함수가 True 반환)
            self.ensure_wsl_distro_ubuntu_pkg_installed(UbuntuPakageName.qemu_user_static)
            self.ensure_wsl_distro_ubuntu_pkg_installed(UbuntuPakageName.binfmt_support)

            # 실행 파일 확인
            rc = _run_root("test -x /usr/bin/qemu-aarch64-static || echo NOBIN")
            if "NOBIN" in (rc.stdout or ""):
                logging.error("/usr/bin/qemu-aarch64-static 를 찾지 못했습니다. qemu-user-static 설치를 확인하세요.")
                raise RuntimeError("qemu-aarch64-static not found")
        except Exception as e:
            # 상위에서 에러 로그를 이미 남기므로 그대로 전파
            raise

        # n. binfmt_misc 지원/마운트 보장
        #    - WSL1 등에서 binfmt_misc 미지원이면 여기서 차단
        try:
            rc = _run_root("grep -qw binfmt_misc /proc/filesystems || echo NOSUP")
            if "NOSUP" in (rc.stdout or ""):
                logging.error("커널이 binfmt_misc를 지원하지 않습니다. (WSL2 필요 가능성).")
                raise RuntimeError("binfmt_misc not supported by kernel")

            # 이미 마운트되어 있지 않으면 마운트
            _run_root("mountpoint -q /proc/sys/fs/binfmt_misc || mount -t binfmt_misc binfmt_misc /proc/sys/fs/binfmt_misc || true")
        except subprocess.CalledProcessError as e:
            logging.error(f"binfmt_misc 마운트 보장 중 오류: {e.stderr}")
            raise

        # 2) 이미 등록되어 있으면 그대로 성공 처리
        try:
            rc = _run_root("test -e /proc/sys/fs/binfmt_misc/qemu-aarch64 && echo READY || echo MISSING")
            if "READY" in (rc.stdout or ""):
                logging.info("qemu-aarch64 binfmt가 이미 활성화되어 있습니다.")
                return True
        except subprocess.CalledProcessError:
            # 계속 진행 (재등록 시도)
            pass

        # 3) 방법 A: update-binfmts DB 경로로 등록/활성화
        try:
            # Ubuntu 18.04의 구버전 update-binfmts는 --flags 옵션을 지원하지 않음
            flags_option = "--flags CF"
            if distro_name == "Ubuntu-18.04":
                logging.warning(f"'{distro_name}'에서는 update-binfmts의 '--flags' 옵션을 지원하지 않아 제외합니다.")
                flags_option = ""

            install_cmd = (
                "/usr/sbin/update-binfmts --install qemu-aarch64 /usr/bin/qemu-aarch64-static "
                f"--magic {self.get_sh_quote(MAGIC)} --mask {self.get_sh_quote(MASK)} {flags_option}"
            )
            _run_root(install_cmd)

            _run_root("/usr/sbin/update-binfmts --import || true")
            _run_root("/usr/sbin/update-binfmts --enable qemu-aarch64")

            # 확인
            rc = _run_root("test -e /proc/sys/fs/binfmt_misc/qemu-aarch64 && echo READY || echo MISSING")
            if "READY" in (rc.stdout or ""):
                logging.info("qemu-aarch64 binfmt가 update-binfmts 경로로 활성화되었습니다.")
                return True
            else:
                logging.warning("update-binfmts 경로로 활성화 확인 실패. 커널 직접 등록을 시도합니다.")
        except subprocess.CalledProcessError as e:
            # 흔한 케이스: "not in database" / exit code 2 등
            msg = (e.stderr or "").strip()
            logging.warning(f"update-binfmts 경로 실패, 커널 직접 등록으로 진행합니다. stderr: {msg}")

        # 4) 방법 B: 커널 인터페이스에 직접 등록 (printf | tee) — 모든 프로세스 root로 실행되므로 sudo 불필요
        try:
            # 기존 엔트리 비활성화(-1) 후 재등록
            _run_root("test -e /proc/sys/fs/binfmt_misc/qemu-aarch64 && echo -1 > /proc/sys/fs/binfmt_misc/qemu-aarch64 || true")

            # printf 가 \x 이스케이프를 해석하도록 그대로 사용 (dash의 printf도 동작)
            register_line_quoted = self.get_sh_quote(ENTRY)
            direct_register_cmd = f"printf %b {register_line_quoted} | tee /proc/sys/fs/binfmt_misc/register >/dev/null"
            _run_root(direct_register_cmd)

            # 최종 확인
            rc = _run_root("test -e /proc/sys/fs/binfmt_misc/qemu-aarch64 && echo READY || echo MISSING")
            if "READY" in (rc.stdout or ""):
                logging.info("qemu-aarch64 binfmt가 커널 인터페이스를 통해 활성화되었습니다.")
                return True
        except subprocess.CalledProcessError as e:
            logging.error(f"커널 직접 등록 실패: {e.stderr}")

        # 5) 마지막으로도 실패하면 예외
        try:
            _run_root("cat /proc/sys/fs/binfmt_misc/status >/dev/null")
        except subprocess.CalledProcessError:
            logging.error("binfmt_misc 상태 확인 실패 (마운트/커널지원 문제일 수 있음).")

        raise RuntimeError("qemu-aarch64 binfmt가 최종 등록/활성화되지 않았습니다.")

    def ensure_l4t_path_located(self, distro_name: str, user_name: str) -> str | None:
        """
        JetPack이 전개한 Linux_for_Tegra 디렉토리 경로를 찾아서 반환.
        - 우선 WSL ext4 경로($HOME, /home/*, /root)에서 검색
        - 없으면 Windows 경로(/mnt/c/Users/*/nvidia/nvidia_sdk, /mnt/c/Users/*/Downloads/nvidia/nvidia_sdk)도 검색
        - Windows 쪽에서만 발견 시, WSL 홈 아래로 rsync 복사 후 그 경로를 반환
        - 끝까지 못 찾으면 None
        """
        import posixpath

        # n. 후보군을 한 번에 찾아서 첫 결과만 출력
        find_inline = r"""
    set -euo pipefail
    out=""
    _try_find () {
      local base="$1"
      [ -d "$base" ] || return 0
      local f
      f="$(find "$base" -type d -name 'Linux_for_Tegra' -print -quit 2>/dev/null || true)"
      [ -n "${f:-}" ] && echo "$f"
    }

    # 우선 WSL ext4(사용자 홈들 + root)에서 탐색
    _try_find "$HOME/nvidia/nvidia_sdk" && exit 0
    for d in /home/*/nvidia/nvidia_sdk; do
      [ -d "$d" ] || continue
      _try_find "$d" && exit 0
    done
    _try_find "/root/nvidia/nvidia_sdk" && exit 0

    # Windows 경로(다운로드 위치 다양성 고려)
    for d in \
      /mnt/c/Users/*/nvidia/nvidia_sdk \
      /mnt/c/Users/*/Downloads/nvidia/nvidia_sdk \
      /mnt/c/Users/*/Documents/nvidia/nvidia_sdk \
      /mnt/c/Users/*/Desktop/nvidia/nvidia_sdk
    do
      [ -d "$d" ] || continue
      _try_find "$d" && exit 0
    done

    exit 1
    """.strip()

        # 사용자 셸에서 한 번에 검색
        res = self.ensure_command_executed_to_wsl_distro_as_user_account(
            distro_name, user_name, f"bash -lc {self.get_sh_quote(find_inline)}"
        )
        found = (res.stdout or "").strip()

        if found:
            # /mnt/c/... 에 있으면 WSL 홈으로 복사 (Ext4에서 작업하기 위해)
            if found.startswith("/mnt/"):
                # 원본과 대상 경로 구성
                # 예) found=/mnt/c/Users/xxx/nvidia/nvidia_sdk/JetPack_5.1.2/Linux_for_Tegra
                parent = posixpath.dirname(found)  # .../JetPack_xxx
                jetpack_name = posixpath.basename(parent)  # JetPack_xxx
                dest_root = f"/home/{user_name}/nvidia/nvidia_sdk/{jetpack_name}"
                dest_l4t = f"{dest_root}/Linux_for_Tegra"

                # 대상 디렉토리 생성 + rsync 복사 + 권한 정리
                self.ensure_command_executed_to_wsl_distro_as_root_account(
                    distro_name, f"mkdir -p {self.get_sh_quote(dest_l4t)}"
                )
                rsync_cmd = (
                    f"rsync -aH --info=progress2 --delete "
                    f"{self.get_sh_quote(found)}/ {self.get_sh_quote(dest_l4t)}/"
                )
                self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, rsync_cmd)
                self.ensure_command_executed_to_wsl_distro_as_root_account(
                    distro_name, f"chown -R {self.get_sh_quote(user_name)}:{self.get_sh_quote(user_name)} {self.get_sh_quote(dest_root)}"
                )
                return dest_l4t

            # 이미 WSL ext4라면 그대로 사용
            return found

        return None

    def ensure_rootfs_dev_random_fix(self, distro_name: str, l4t_path: str) -> None:
        """
        SDKM의 'File System and OS' 단계가 rootfs/dev/random(또는 urandom) 잔여물로
        mknod 'File exists'에 실패하는 걸 예방/복구한다.
        """
        import logging, textwrap
        sh = textwrap.dedent(f"""
            set -e
            cd {self.get_sh_quote(l4t_path)}
            mkdir -p rootfs/dev
            rm -f rootfs/dev/random || true
            rm -f rootfs/dev/urandom || true
        """).strip()
        logging.info("rootfs/dev 잔여 device node 정리( random/urandom )...")
        # TODO ensure_command_executed_to_wsl_distro_as_root_account()
