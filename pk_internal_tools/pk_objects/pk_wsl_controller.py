import logging
import subprocess
import textwrap
import traceback
from enum import Enum
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_command_executed_advanced import ensure_command_executed_advanced
from pk_internal_tools.pk_functions.ensure_command_executed_as_admin import ensure_command_executed_as_admin
from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
from pk_internal_tools.pk_functions.ensure_pk_python_file_executed_in_uv_venv_windows import ensure_pk_python_file_executed_in_uv_venv_windows
from pk_internal_tools.pk_functions.ensure_signature_found_in_lines import ensure_signature_found_in_lines
from pk_internal_tools.pk_functions.ensure_signature_found_in_souts_for_milliseconds_limited import ensure_signature_found_in_souts_for_milliseconds_limited
from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForEnsureSlept, SetupOpsForGetListFromClass, SetupOpsForSdkManager, SetupOpsForPkWirelessTargetController
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
from pk_internal_tools.pk_functions.get_env_var_name_id import get_env_var_id
from pk_internal_tools.pk_functions.get_list_from_class import get_list_from_class
from pk_internal_tools.pk_functions.get_milliseconds_from_seconds import get_milliseconds_from_seconds
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
from pk_internal_tools.pk_functions.get_window_title_temp_for_cmd_exe import get_window_title_temp_for_cmd_exe
from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified
from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21
from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
from pk_internal_tools.pk_objects.pk_identifier import PkIdentifier, PkDevice
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers
from pk_internal_tools.pk_objects.pk_files import F_WSL_SSHD_CONFIG, F_USBPIPD_MSI
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_target import PkTarget
from pk_internal_tools.pk_objects.pk_ubuntu_package_name import UbuntuPakageName
from pk_internal_tools.pk_objects.pk_directories import D_USERPROFILE
from pathlib import Path

# 기본 SSH 키 경로 정의
F_LOCAL_SSH_PUBLIC_KEY = D_USERPROFILE / ".ssh" / "id_ed25519.pub"
F_LOCAL_SSH_PRIVATE_KEY = D_USERPROFILE / ".ssh" / "id_ed25519"


class WslDistrosNotSupportedOfficiallyAnymore(Enum):
    ubuntu_18_04 = "Ubuntu-18.04"


class PkWslController(PkIdentifier):
    from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
    from pathlib import Path
    from typing import Optional

    from pk_internal_tools.pk_objects.pk_target import PkTarget

    """
        # remote device == target 을 제어하기 위한 목적
        self : host machine is working for control target device
        wsl : wsl hardware device
    """
    _wsl: PkTarget = None

    from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

    def __init__(self, identifier: "PkDevice" = PkDevice.undefined, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None, setup_op: "SetupOpsForPkWirelessTargetController" = SetupOpsForPkWirelessTargetController.INITIALIZE_NONE):
        super().__init__(identifier)

        self.window_title_temp = get_window_title_temp_identified(__file__)
        self._setup_op = setup_op
        self._init_kwargs = dict(ip=ip, pw=pw, hostname=hostname, port=port, user_n=user_n, f_local_ssh_public_key=f_local_ssh_public_key, f_local_ssh_private_key=f_local_ssh_private_key, nick_name=nick_name)
        self.ensure_executed_by_setup_op(setup_op, **self._init_kwargs)
        logging.debug(f'{get_caller_name()} is initialized')

    def ensure_executed_by_setup_op(self, setup_ops: "SetupOpsForPkWirelessTargetController", *, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None) -> None:
        import logging
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice

        if setup_ops & SetupOpsForPkWirelessTargetController.INITIALIZE_NONE:
            return

        if setup_ops & SetupOpsForPkWirelessTargetController.SELF:
            self.set_self(
                ip=ip, pw=pw, hostname=hostname, port=port, user_n=user_n,
                f_local_ssh_public_key=f_local_ssh_public_key,
                f_local_ssh_private_key=f_local_ssh_private_key,
                nick_name=nick_name,
            )
            logging.debug("set_self() done")

        if setup_ops & SetupOpsForPkWirelessTargetController.WSL_DISTRO:
            self.setup_wsl_distro()
            logging.debug("setup_wsl() done")
            if self._wsl is None:
                logging.error("WSL setup failed. Cannot proceed with WSL-dependent operations.")
                return  # Exit _run_setups if WSL setup failed

    def set_self(self, ip=None, pw=None, hostname=None, port=None, user_n=None, f_local_ssh_public_key=None, f_local_ssh_private_key=None, nick_name=None):
        self.ip = ip
        self.pw = pw
        self.hostname = hostname
        self.port = port
        self.user_n = user_n
        self.f_local_ssh_public_key = f_local_ssh_public_key
        self.f_local_ssh_private_key = f_local_ssh_private_key
        self.nick_name = nick_name



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
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed

        # pk_* -> 명시적 초기화, ⚠️ 수동 초기화
        # env_var_name = "selected"
        # selected = ensure_value_completed_2025_10_13_0000(env_var_name=env_var_name, prompt_message=f"{env_var_name}", options=get_wsl_distro_names_installed())

        # pk_* -> 자동 초기화, ⚠️ 환경변수 selected 를 수정하기 위해서는 selected 수동 수정 필요
        env_var_name = "wsl_distro_name_debug"
        selected = ensure_env_var_completed_2025_11_23(env_var_name=env_var_name, prompt_message=f"{env_var_name}", options=self.get_wsl_distro_names_installed())
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
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
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
            ensure_debug_loged_verbose(traceback)
            return []

    def ensure_wsl_distro_installed_by_user_selection(self):
        import logging
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
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
        selected_distro = ensure_value_completed_2025_10_13_0000(
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
            selected = ensure_env_var_completed_2025_11_24(key_name=key_name, func_n=func_n)
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
                        except:
                            ensure_debug_loged_verbose(traceback)
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
        except:
            ensure_debug_loged_verbose(traceback)
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
                selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
                if selected == another_option:
                    question = f'do you want to install another wsl distro and use it'
                    ok = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
                    if ok == PkTexts.YES:
                        self.ensure_wsl_distro_installed_by_user_selection()
                        continue
                wsl_distro_name = selected
                break
        else:
            while True:
                key_name = 'wsl_distro_name'
                options = self.get_wsl_distro_names_installed() + [another_option]
                selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
                if selected == another_option:
                    question = f'do you want to install another wsl distro and use it'
                    ok = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
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
        selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n)
        wsl_distro_user_n = selected

        key_name = 'wsl_distro_f_local_ssh_public_key'
        selected = ensure_env_var_completed_2025_11_24(key_name=key_name, func_n=func_n)
        wsl_distro_f_local_ssh_public_key = selected

        key_name = 'wsl_distro_f_local_ssh_private_key'
        selected = ensure_env_var_completed_2025_11_24(key_name=key_name, func_n=func_n)
        wsl_distro_f_local_ssh_private_key = selected

        key_name = 'wsl_distro_nick_name'
        selected = ensure_env_var_completed_2025_11_24(key_name=key_name, func_n=func_n)
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
        except:
            logging.error("Failed to get installed WSL distro names.")
            return []

    def get_distro_names(self, distro_name) -> list[str]:
        import subprocess

        try:
            if not self.is_wsl_distro_installed(distro_name): return []
            result = subprocess.run(['wsl', '--list', '--quiet'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode != 0: return []

            output = result.stdout.replace('\x00', '').strip()
            return [line.strip() for line in output.splitlines() if line.strip()]
        except:
            ensure_debug_loged_verbose(traceback)
            return []

    @ensure_seconds_measured
    def ensure_wsl_distros_enabled_with_persistent_session(self):
        import logging
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        try:
            for distro_name in self.get_wsl_distro_names_executable():
                if self.ensure_wsl_distro_executed_with_persistent_session(distro_name):
                    logging.debug("WSL distros enabled with persistent sessions")
                else:
                    logging.debug("Failed to start WSL distros with persistent sessions")
                    return False
            return True
        except:
            ensure_debug_loged_verbose(traceback)
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
                        except:
                            logging.warning(f"sshd_config: Could not parse Port line: {line}")
                    if line.strip().startswith("ListenAddress"):  # Check for ListenAddress
                        try:
                            address_value = line.strip().split()[1]
                            if address_value not in ["0.0.0.0", "::"]:
                                logging.warning(f"sshd_config: ListenAddress is set to {address_value}, expected 0.0.0.0 or ::.")
                            listen_address_found = True
                        except:
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
        from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21

        if not is_internet_connected_2025_10_21():
            logging.debug(f'''can not install ubuntu pakage ({distro_package_name}) for internet not connected  ''')
            raise
        if distro_package_name == 'docker':
            std_outs, std_errs = self.ensure_command_to_wireless_target_with_pubkey(cmd='docker --version')
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
            std_outs, std_errs = self.ensure_command_to_wireless_target_with_pubkey(cmd=f'sudo apt list --installed | grep {distro_package_name}')
            if std_outs is None:
                logging.error(f"Failed to list installed packages for {distro_package_name} from remote OS. SSH connection might be down.")
                return False
            if ensure_signature_found_in_lines(signature='installed', lines=std_outs):
                logging.debug(f"{distro_package_name} is installed in {self._target.distro_name}")
                ensure_general_ubuntu_pkg(ubuntu_pkg_n=distro_package_name)
        return True

    def ensure_target_distro_docker_installed(self):
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(cmd='sudo usermod -aG docker $USER')
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(cmd='sudo apt update')
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(
            cmd='curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg')  # GPG 키 추가
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(
            cmd='sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release')  # wsl docker dependency
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(
            cmd='echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')  # Docker 리포지토리 추가
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(cmd='sudo apt update')
        std_outs, std_err_list = self.ensure_command_to_wireless_target_with_pubkey(
            cmd='sudo apt install -y docker-ce docker-ce-cli containerd.io')

    def ensure_command_to_wireless_target(self, cmd):
        return self.ensure_command_to_wireless_target_with_pubkey(cmd=cmd)

    def ensure_file_transferred_to_target(self, local_path: str, remote_path: str) -> bool:
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
            f"  - Host: {self._target.ip}:{self._target.port}\n"
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
                key_private = paramiko.Ed25519Key(filename=self._target.f_local_ssh_private_key)
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
            ensure_debug_loged_verbose(traceback)
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
            ensure_debug_loged_verbose(traceback)
            return False
        finally:
            ssh.close()

    def ensure_command_to_wireless_target_with_pubkey(self, cmd):
        import logging
        import paramiko
        import traceback
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

        if not self._target or not self._target.ip:
            logging.error("Target is not properly configured. IP address is missing.")
            return None, ["Target not configured"]

        logging.debug(
            f"Attempting to execute command on target:\n"
            f"  - Host: {self._target.ip}:{self._target.port}\n"
            f"  - User: {self._target.user_name}\n"
            f"  - Command: {cmd}"
        )

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False

        # n. 공개 키 인증 시도
        try:
            if self._target.f_local_ssh_private_key:
                logging.info("SSH 공개 키로 연결을 시도합니다...")
                key_private = paramiko.Ed25519Key(filename=self._target.f_local_ssh_private_key)
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
            if self._target.pw:
                stdin.write(self._target.pw + '\n')
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

    def get_f_local_ssh_public_key(self):
        pass

    def get_f_wsl_sshd_config_path(self, distro_name: str) -> Optional[Path]:
        """
        지정된 WSL distro의 sshd_config 파일에 대한 Windows 호스트 접근 경로를 반환합니다.

        Args:
            distro_name: 대상 WSL distro의 이름입니다.

        Returns:
            Windows에서 접근 가능한 sshd_config 파일의 Path 객체.
            distro_name이 제공되지 않으면 None을 반환합니다.
        """
        import logging
        from pathlib import Path

        from pk_internal_tools.pk_objects.pk_files import F_WSL_SSHD_CONFIG

        if not distro_name:
            logging.error("distro_name이 제공되지 않았습니다.")
            return None

        # Windows에서 WSL 파일 시스템에 접근하기 위한 UNC 경로
        # \wsl.localhost\Ubuntu\etc\ssh\sshd_config 형식
        wsl_path = Path(f"//wsl.localhost/{distro_name}{F_WSL_SSHD_CONFIG}")

        logging.debug(f"생성된 WSL sshd_config 경로: {wsl_path}")

        return wsl_path

    def ensure_wsl_effective_info_printed(self):
        """
        Print only non-None fields of wsl in pretty JSON format.
        """
        import logging
        import json

        if not hasattr(self, 'wsl') or self._wsl is None:
            logging.warning("self._wsl is not initialized. Cannot print effective info.")
            return None

        # wsl 객체 → dict
        wsl_dict = self._wsl.to_dict()

        # None 값 제거
        effective_dict = {k: v for k, v in wsl_dict.items() if v is not None}

        # JSON 문자열 변환
        pretty_json = json.dumps(effective_dict, indent=4, ensure_ascii=False)

        logging.debug(f"WSL effective info:\n{pretty_json}")
        return pretty_json

    def ensure_sdkmanager_executed_on_wsl_distro(self, setup_op: "SetupOpsForSdkManager" = SetupOpsForSdkManager.GUI):
        if not self.ensure_sdkmanager_installed_on_wsl_distro():
            logging.warning("sdkmanager is not installed")
            return False
        logging.info("Attempting to launch NVIDIA SDK Manager")

        ensure_spoken("NVIDIA SDK Manager를 실행합니다. 창을 확인해주세요.")

        distro_name = self._wsl.distro_name
        wsl_user_n = self._wsl.user_name if self._wsl.user_name != "root" else "pk"  # pk_option
        sdk_cmd = None
        if setup_op == SetupOpsForSdkManager.GUI:
            sdk_cmd = f"start wsl -d {distro_name} -u {wsl_user_n} -- sdkmanager"
        elif setup_op == SetupOpsForSdkManager.CLI:
            # sdk_cmd = f'start "" wsl -d {distro_name} sdkmanager --cli' # -> Debugging is uncomfortable because I cannot see the error when the window is not kept open
            # sdk_cmd = f'start cmd /K "wsl -d {distro_name} sdkmanager --cli"'  # -> title name not defined -> can control title to close
            sdk_cmd = f'start "{self.window_title_temp}" cmd /K "wsl -d {distro_name} sdkmanager --cli"'  # -> can not see detail failure log

        stdout, stderr = ensure_command_executed(sdk_cmd)

        if stderr:
            logging.error(f"Failed to launch SDK Manager: {stderr}")
            logging.warning("SDK Manager를 시작하지 못했습니다. WSL에 지원이 설정되어 있는지 확인하세요 (예: WSLg).")
            ensure_spoken("SDK Manager를 시작하지 못했습니다.")
            return False

        logging.info("SDK Manager launched. Please proceed with the installation steps in the GUI.")
        logging.info("GUI에서의 작업이 완료되면 다음 단계를 진행하세요.")
        return True

    def ensure_sdkmanager_installed_on_wsl_distro(self):
        """
        Ensures NVIDIA SDK Manager is installed in the WSL distro.
        Checks for existing file before guiding the user to download it, then copies and installs it.
        """
        import logging
        import os
        from pathlib import Path
        import glob
        from pk_internal_tools.pk_objects.pk_directories import d_pk_linux_tools, d_pk_external_tools

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
        fallback_paths = [d_pk_linux_tools, d_pk_external_tools]
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
                ok = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
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
        latest_deb_filename = Path(latest_deb_path).name
        logging.info(f"Using SDK Manager DEB file: {latest_deb_path}")

        wsl_downloads_dir_host_path = Path(f"//wsl.localhost/{distro_name}{wsl_user_home.replace('/', '//')}/Downloads")
        ensure_command_executed(f"wsl -d {distro_name} -- mkdir -p {wsl_user_home}/Downloads")

        logging.info(f"Copying {latest_deb_filename} to WSL ({wsl_downloads_dir_host_path})...")
        copy_cmd = f'copy "{latest_deb_path}" "{wsl_downloads_dir_host_path}"'
        stdout, stderr = ensure_command_executed(copy_cmd)
        if stderr and "지정된 파일을 찾을 수 없습니다" not in " ".join(stderr):
            logging.error(f"Failed to copy file to WSL: {stderr}")
            ensure_spoken("파일을 WSL로 복사하는 데 실패했습니다.")
            return False

        wsl_deb_path = f"{wsl_user_home}/Downloads/{latest_deb_filename}"
        logging.info(f"Installing {latest_deb_filename} in WSL...")
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

    @ensure_seconds_measured
    @ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=128)  # pk_option
    def ensure_wsl_packages_installed(self, distro_name, packages):
        import logging

        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

        """Checks if a list of packages are installed in a WSL distribution and installs them if not."""
        for package in packages:
            logging.debug(f"Checking if '{package}' is installed in WSL distro '{distro_name}'...")
            # Using 'dpkg -s' is more reliable for checking installation status of Debian packages.
            check_cmd = f"wsl -d {distro_name} -- dpkg -s {package}"
            outs, errs = ensure_command_executed(check_cmd)

            # 'dpkg -s' outputs to stdout and has a zero exit code if the package is installed.
            # If not installed, it outputs to stderr and has a non-zero exit code.
            if not errs:
                logging.info(f"Package '{package}' is already installed in '{distro_name}'.")
                continue

            # Package is not installed or check failed, proceed with installation.
            logging.warning(f"Package '{package}' not found or check failed in '{distro_name}'. Attempting to install...")

            # Update package list first
            update_cmd = f"wsl -d {distro_name} -- sudo apt-get update"
            logging.debug(f"Running package list update in '{distro_name}'...")
            update_outs, update_errs = ensure_command_executed(update_cmd)
            if update_errs:
                # This might not be a fatal error, so just log a warning.
                logging.warning(f"Error updating package lists in '{distro_name}': {update_errs}")

            # Install the package
            install_cmd = f"wsl -d {distro_name} -- sudo apt-get install -y {package}"
            logging.debug(f"Running installation for '{package}' in '{distro_name}'...")
            install_outs, install_errs = ensure_command_executed(install_cmd)
            if install_errs:
                logging.error(f"Failed to install '{package}' in '{distro_name}': {install_errs}")
                raise RuntimeError(f"Failed to install '{package}' in WSL distro '{distro_name}'.")

            # Verify installation
            logging.debug(f"Verifying installation of '{package}' in '{distro_name}'...")
            verify_outs, verify_errs = ensure_command_executed(check_cmd)
            if verify_errs:
                logging.error(f"Verification failed for '{package}' in '{distro_name}' after installation attempt: {verify_errs}")
                raise RuntimeError(f"Failed to verify '{package}' installation in WSL distro '{distro_name}'.")

            logging.info(f"Successfully installed and verified '{package}' in '{distro_name}'.")

        return True

    @ensure_seconds_measured
    def get_wsl_distro_name_installed_legacy(self):
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000

        wsl_distro_names_installed = self.get_wsl_distro_names_installed()

        if len(wsl_distro_names_installed) == 1:
            return wsl_distro_names_installed[0]

        else:
            key_name = "wsl_distro_name"
            from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
            func_n = get_caller_name()
            selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=wsl_distro_names_installed)
            wsl_distro_name = selected

            return wsl_distro_name

    def get_wsl_distro_pw_legacy(self, distro_name):
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        env_var_name = get_env_var_id("PASSWORD", func_n)
        prompt_message = f"Please enter the password for WSL distro '{distro_name}': "

        wsl_pw = ensure_env_var_completed_2025_11_23(env_var_name, prompt_message)

        return wsl_pw

    def get_wsl_distro_ip_legacy(self, distro_name):
        import logging
        from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_functions.get_env_var_name_id import get_env_var_id  # New import
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        std_outs = None
        if is_os_windows():
            std_outs = ensure_command_executed(rf'wsl -d {distro_name} hostname -I')
        else:
            if is_os_wsl_linux():
                std_outs = ensure_command_executed(rf'hostname -I')
            else:
                pass

        wsl_ip = None
        if std_outs and len(std_outs) > 0:
            logging.debug(f"In get_wsl_ip, type(std_outs)={type(std_outs)}, std_outs={std_outs}")
            logging.debug(f"In get_wsl_ip, type(std_outs[0])={type(std_outs[0])}, std_outs[0]={std_outs[0]}")
            wsl_ip = std_outs[0][0].split(" ")[0]

        if not wsl_ip:
            env_var_name = get_env_var_id("IP", func_n)  # Use helper function
            prompt_message = f"Please enter the IP address for WSL distro '{distro_name}': "
            wsl_ip = ensure_env_var_completed_2025_11_23(env_var_name, prompt_message)

        return wsl_ip

    def get_wsl_distro_user_name_legacy_via_whoami(self, distro_name):
        import logging

        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed  # New import
        from pk_internal_tools.pk_functions.get_env_var_name_id import get_env_var_id  # New import
        from pk_internal_tools.pk_functions.get_list_without_none_and_duplicates import get_list_without_none_and_duplicates
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

        std_outs = None
        if is_os_windows():
            std_outs = ensure_command_executed(f'wsl -d {distro_name} whoami')
        else:
            std_outs = ensure_command_executed(rf'whoami', encoding='utf-8')

        user_n = None
        if std_outs:
            user_n_list = get_list_without_none_and_duplicates(std_outs)
            if len(user_n_list) == 1:
                user_n = user_n_list[0]
            else:
                logging.debug(f"현재 wsl에 로그인된 사용자가 한명이 아닙니다 user_n_list=[{user_n_list}]")

        if not user_n:
            from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
            func_n = get_caller_name()
            env_var_name = get_env_var_id("USERNAME", func_n)  # Use helper function
            prompt_message = f"Please enter the username for WSL distro '{distro_name}': "
            user_n = ensure_env_var_completed_2025_11_23(env_var_name, prompt_message)

        if user_n:
            logging.debug(rf'''user_n"{user_n}"  ''')
        return user_n

    def ensure_wsl_distro_user_added(self, distro: str, user_name: str):
        subprocess.run(
            ["wsl.exe", "-d", distro, "-u", "root", "--", "adduser", user_name],
            check=True
        )

    def ensure_wsl_distro_user_pw_changed(self, distro: str, user_name: str):
        subprocess.run(
            ["wsl.exe", "-d", distro, "-u", "root", "--", "passwd", user_name],
            check=True
        )

    def ensure_wsl_distro_specific_app_without_user_pw_access(self, distro_name: str, user_name: str, executable_abs_path: str):
        cmd = f'echo "{user_name} ALL=(ALL) NOPASSWD: {executable_abs_path}" | EDITOR="tee -a" visudo'
        subprocess.run(["wsl.exe", "-d", distro_name, "-u", "root", "--", "sh", "-lc", cmd], check=True)

    def ensure_wsl_distro_apps_without_user_pw_access(self, distro_name: str, user_name: str):
        cmd = f'echo "{user_name} ALL=(ALL) NOPASSWD: ALL" | EDITOR="tee -a" visudo'
        subprocess.run(["wsl.exe", "-d", distro_name, "-u", "root", "--", "sh", "-lc", cmd], check=True)

    def ensure_wsl_distro_root_account_access_permitted(self, distro_name: str, user_name: str):
        cmd = f'echo "{user_name} ALL=(ALL) NOPASSWD: /bin/su" | EDITOR="tee -a" visudo'
        subprocess.run(["wsl.exe", "-d", distro_name, "-u", "root", "--", "sh", "-lc", cmd], check=True)

    def ensure_wsl_distro_user_added_advanced(self, distro_name: str, user_name: str, password: str, create_home: bool = True, shell: str = "/bin/bash"):
        rc = self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"id -u {self.get_sh_quote(user_name)} >/dev/null 2>&1 || echo NOUSER")
        if "NOUSER" in (rc.stdout or ""):
            home_flag = "-m" if create_home else "-M"
            self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"useradd {home_flag} -s {self.get_sh_quote(shell)} {self.get_sh_quote(user_name)}")
        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"echo {self.get_sh_quote(user_name)}:{self.get_sh_quote(password)} | chpasswd")

    def ensure_wsl_distro_user_pw_changed_advanced(self, distro_name: str, user_name: str, new_password: str):
        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"echo {self.get_sh_quote(user_name)}:{self.get_sh_quote(new_password)} | chpasswd")

    def ensure_wsl_distro_specific_app_without_user_pw_access_advanced(self, distro_name: str, user_name: str, executable_abs_path: str, group_name: str | None = None, file_tag: str | None = None):
        rc = self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"test -x {self.get_sh_quote(executable_abs_path)} || echo NOEXE")
        if "NOEXE" in (rc.stdout or ""):
            raise RuntimeError(f"Executable not found: {executable_abs_path}")
        if group_name:
            self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, f"usermod -aG {self.get_sh_quote(group_name)} {self.get_sh_quote(user_name)}")
        tag = file_tag or f"{user_name}-nopasswd-{Path(executable_abs_path).name}"
        line = f"{user_name} ALL=(ALL) NOPASSWD: {executable_abs_path}\n"
        self.ensure_wsl_distro_sudoers_fragment_written(distro_name, tag, line)

    def ensure_wsl_distro_apps_without_user_pw_access_advanced(self, distro_name: str, user_name: str, file_tag: str | None = None):
        tag = file_tag or f"{user_name}-nopasswd-all"
        line = f"{user_name} ALL=(ALL) NOPASSWD: ALL\n"
        self.ensure_wsl_distro_sudoers_fragment_written(distro_name, tag, line)

    def ensure_wsl_distro_root_account_access_permitted_advanced(self, distro_name: str, user_name: str, file_tag: str | None = None):
        rc = self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, "test -x /bin/su || echo NOSU")
        if "NOSU" in (rc.stdout or ""):
            raise RuntimeError("/bin/su not found")
        tag = file_tag or f"{user_name}-nopasswd-su"
        line = f"{user_name} ALL=(ALL) NOPASSWD: /bin/su\n"
        self.ensure_wsl_distro_sudoers_fragment_written(distro_name, tag, line)

    def get_sh_quote(self, s: str) -> str:
        # TODO renaming
        return "'" + s.replace("'", "'\"'\"'") + "'"

    # 교체: ensure_command_executed_to_wsl_distro_as_root_account
    def ensure_command_executed_to_wsl_distro_as_root_account(self, distro_name: str, cmd: str):
        full_cmd = ["wsl.exe", "-d", distro_name, "-u", "root", "--", "sh", "-lc", cmd]
        logging.debug(textwrap.dedent(f"""
            cmd                      | {' '.join(full_cmd)}
            distro_name              | {distro_name}
            user_name                | root
            mode                     | sync
            encoding                 | utf-8
        """))
        result = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            logging.error(f"Command failed with exit code {result.returncode}: {cmd}")
            if result.stdout:
                logging.error(f"Stdout: {result.stdout}")
            if result.stderr:
                logging.error(f"Stderr: {result.stderr}")
            result.check_returncode()
        return result

    # 교체: ensure_command_executed_to_wsl_distro_as_user_account
    def ensure_command_executed_to_wsl_distro_as_user_account(self, distro_name: str, user_name: str, cmd: str):
        full_cmd = ["wsl.exe", "-d", distro_name, "-u", user_name, "--", "sh", "-lc", cmd]
        logging.debug(textwrap.dedent(f"""
            cmd                      | {' '.join(full_cmd)}
            distro_name              | {distro_name}
            user_name                | {user_name}
            mode                     | sync
            encoding                 | utf-8
        """))
        result = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            logging.error(f"Command failed with exit code {result.returncode}: {cmd}")
            if result.stdout:
                logging.error(f"Stdout: {result.stdout}")
            if result.stderr:
                logging.error(f"Stderr: {result.stderr}")
            result.check_returncode()
        return result

    def ensure_wsl_distro_sudoers_fragment_written(self, distro: str, filename: str, content: str):
        tmp_path = f"/tmp/.{filename}.tmp"
        remote_path = f"/etc/sudoers.d/{filename}"
        cmd = (
            f"printf %s {self.get_sh_quote(content)} > {self.get_sh_quote(tmp_path)} && "
            f"chown root:root {self.get_sh_quote(tmp_path)} && "
            f"chmod 0440 {self.get_sh_quote(tmp_path)} && "
            f"mv {self.get_sh_quote(tmp_path)} {self.get_sh_quote(remote_path)} && "
            f"visudo -cf /etc/sudoers"
        )
        self.ensure_command_executed_to_wsl_distro_as_root_account(distro, cmd)

    def ensure_wsl_distro_session_alived(self, distro_name):
        import logging
        import time  # Added import

        from pk_internal_tools.pk_functions.is_wsl_distro_started import is_wsl_distro_started
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
        from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
        import subprocess

        logging.debug(f"Attempting to ensure WSL distro session for: {distro_name}")

        if is_os_windows():
            if not is_os_wsl_linux():
                if not is_wsl_distro_started(distro_name):
                    logging.debug(f"WSL distro {distro_name} is not started. Attempting to start it.")
                    # subprocess.Popen(f"wsl -d {distro_name}", creationflags=subprocess.CREATE_NO_WINDOW)
                    subprocess.Popen(f"wsl -d {distro_name} --exit", creationflags=subprocess.CREATE_NO_WINDOW)

                    retry_cnt_limited = 10
                    retry_delay = 1  # seconds
                    started = False
                    for i in range(retry_cnt_limited):
                        self.ensure_wsl_distro_executed(self._wsl.distro_name)
                        logging.debug(f"Checking if WSL distro {distro_name} started (attempt {i + 1}/{retry_cnt_limited})...")
                        if is_wsl_distro_started(distro_name):
                            started = True
                            logging.debug(f"WSL distro {distro_name} successfully started.")
                            break
                        time.sleep(retry_delay)

                    if not started:
                        logging.error(f"Failed to start WSL distro {distro_name} after {retry_cnt_limited} attempts.")

                if is_wsl_distro_started(distro_name):  # This check is redundant after the loop, but keeping for consistency with original logic
                    logging.debug(f'''{distro_name} is started already in wsl with keeping session ''')
                else:  # This else branch should ideally not be reached if the above logic is correct
                    logging.debug(f'''{distro_name} is not started in wsl with keeping session ''')

        return True

    def ensure_wsl_distros_enabled(self):
        import logging
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        try:
            for distro_name in self.get_wsl_distro_names_executable():
                if self.ensure_wsl_distro_executed(distro_name):
                    if self.is_wsl_distro_executed(distro_name):
                        logging.debug(f"WSL distros enabled with persistent sessions '{distro_name}'")
                    else:
                        logging.debug(f"Failed to start WSL distros with persistent sessions '{distro_name}'")
                        return False
            return True
        except:
            ensure_debug_loged_verbose(traceback)

    def get_wsl_distro_names_executable(self):  # 기능 중복 같음.
        import logging
        import subprocess

        try:
            # WSL이 실제로 설치되어 있는지 먼저 확인
            if not self.is_wsl_installed():
                logging.debug("WSL is not installed")
                return []

            result = subprocess.run(['wsl', '-l', '-v'], capture_output=True, text=True)

            if result.returncode != 0:
                logging.debug(f"WSL command failed with return code: {result.returncode}")
                if result.stderr:
                    logging.debug(f"WSL error: {result.stderr}")
                return []

            output = result.stdout
            if not output.strip():
                logging.debug("WSL command returned empty output")
                return []

            # null 문자 제거 및 정리
            cleaned_output = output.replace('\x00', '').strip()
            lines = cleaned_output.splitlines()
            for line in lines:
                logging.debug(f"Raw WSL output: {line}")

            distros = []
            for line in lines:
                if line.strip():
                    # WSL 배포판 정보 파싱
                    parts = line.split()
                    logging.debug(f"Parsing line: '{line}' -> parts: {parts}")

                    # 헤더 라인 건너뛰기
                    if parts[0] in ['NAME', 'STATE', 'VERSION'] or len(parts) < 3:
                        logging.debug(f"Skipping header line: {line}")
                        continue

                    if len(parts) >= 3:
                        # * 표시가 있는 경우 처리
                        if parts[0] == '*':
                            # * Ubuntu    Running         2 형태
                            name = parts[1]
                            state = parts[2]
                            version = parts[3] if len(parts) > 3 else "?"
                        else:
                            # Ubuntu    Running         2 형태
                            name = parts[0]
                            state = parts[1]
                            version = parts[2] if len(parts) > 2 else "?"

                        # null 문자 제거
                        name = name.replace('\x00', '').strip()
                        state = state.replace('\x00', '').strip()
                        version = version.replace('\x00', '').strip()

                        if name and name not in ['NAME', 'STATE', 'VERSION']:  # 유효한 배포판 이름인지 확인
                            distro_info = {
                                'name': name,
                                'state': state,
                                'version': version
                            }
                            distros.append(distro_info)
                            logging.debug(f"Added distro: {distro_info}")

            logging.debug(f"Found {len(distros)} WSL distros")
            return distros

        except FileNotFoundError:
            logging.debug("WSL command not found")
            return []
        except Exception as e:
            logging.debug(f"Failed to get WSL distros: {e}")
            return []

    def ensure_wsl_distro_assistance_executed(self):
        import logging
        import subprocess
        from pathlib import Path
        import shutil

        from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
        logging.info(f"WSL distro 지원 기능 시작")

        func_n = get_caller_name()

        OP_ENTER = "distro 진입"
        OP_DELETE = "distro 삭제"
        OP_INSTALL = "distro 설치"
        OP_DISTROS_INFO = "distros 정보출력"

        work_type = [OP_ENTER, OP_DELETE, OP_INSTALL, OP_DISTROS_INFO]
        while True:
            operation_option = ensure_value_completed_2025_10_12_0000(key_name="작업옵션", options=work_type)

            distro_name = None
            if operation_option != OP_DISTROS_INFO:
                key_name = "distro_name"
                wsl_distros_not_supported_officially_anymore = get_list_from_class(WslDistrosNotSupportedOfficiallyAnymore, SetupOpsForGetListFromClass.ATTRIBUTE_VALUE)
                options = self.get_wsl_distro_names_installed() + self.get_wsl_distro_names_installable() + wsl_distros_not_supported_officially_anymore
                selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=options)
                distro_name = selected

            if operation_option == OP_ENTER:
                logging.info(f"WSL distro '{distro_name}'에 진입합니다.")
                try:
                    subprocess.run(f"wsl -d {distro_name}", shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    logging.error(f"WSL 진입 중 오류 발생: {e}")
                except FileNotFoundError:
                    logging.error("WSL 명령어를 찾을 수 없습니다. WSL이 설치되어 있는지 확인하세요.")

            elif operation_option == OP_DELETE:
                logging.info(f"WSL distro '{distro_name}'을(를) 삭제(unregister)합니다.")
                ok = ensure_value_completed_2025_10_12_0000(
                    key_name=f"정말로 '{distro_name}' distro을 unregister 하시겠습니까?",
                    options=[PkTexts.YES, PkTexts.NO],
                )
                if ok == PkTexts.YES:
                    try:
                        subprocess.run(f"wsl --unregister {distro_name}", shell=True, check=True)
                        logging.info(f"'{distro_name}' distro이 성공적으로 unregister 되었습니다.")

                        ok_delete_dir = ensure_value_completed_2025_10_12_0000(
                            key_name=f"'{distro_name}'의 실제 설치 디렉토리도 삭제하시겠습니까?",
                            options=[PkTexts.YES, PkTexts.NO],
                        )
                        if ok_delete_dir == PkTexts.YES:
                            import os
                            options = []
                            local_app_data = os.environ.get('LOCALAPPDATA')
                            if local_app_data:
                                packages_path = Path(local_app_data) / 'Packages'
                                if packages_path.exists():
                                    try:
                                        for package_dir in packages_path.iterdir():
                                            if distro_name.lower() in package_dir.name.lower():
                                                potential_path = package_dir / 'LocalState'
                                                if potential_path.exists():
                                                    options.append(str(potential_path))
                                                    logging.debug(f"'{distro_name}'의 예상 설치 경로를 찾았습니다 {potential_path}")
                                    except Exception as e:
                                        logging.warning(f'WSL distro 경로 검색 중 오류 발생: {e}')
                            distro_path_input = ensure_value_completed_2025_10_12_0000(
                                key_name=f"'{distro_name}'의 설치 디렉토리 경로를 입력해주세요",
                                options=options)
                            if distro_path_input:
                                distro_path = Path(distro_path_input)
                                if distro_path.exists() and distro_path.is_dir():
                                    ok_confirm_delete = ensure_value_completed_2025_10_12_0000(
                                        key_name=f"'{distro_path}' 디렉토리를 삭제하시겠습니까?, 없다면 '종료' 를 눌러주세요. ",
                                        options=[PkTexts.YES, PkTexts.NO],
                                    )
                                    if ok_confirm_delete == PkTexts.YES:
                                        try:
                                            shutil.rmtree(distro_path)
                                            logging.info(f"'{distro_path}' 디렉토리가 성공적으로 삭제되었습니다.")
                                        except Exception as e:
                                            logging.error(f"디렉토리 삭제 중 오류 발생: {e}")
                                    else:
                                        logging.info("디렉토리 삭제를 취소했습니다.")
                                else:
                                    logging.warning(
                                        f"입력된 경로 '{distro_path}'가 유효하지 않거나 존재하지 않습니다. "
                                        "디렉토리를 수동으로 삭제해주세요."
                                    )
                            else:
                                logging.info("디렉토리 경로가 입력되지 않아 삭제를 건너뛰었습니다.")
                    except subprocess.CalledProcessError as e:
                        logging.error(f"WSL unregister 중 오류 발생: {e}")
                else:
                    logging.info("WSL distro 삭제를 취소했습니다.")

            elif operation_option == OP_INSTALL:
                # 공식 지원 중단 버전인지 확인
                unsupported_distro_values = [e.value for e in WslDistrosNotSupportedOfficiallyAnymore]
                if distro_name in unsupported_distro_values:
                    logging.warning(f"`wsl --install -d {distro_name}` 사용은 공식적으로 지원되지 않습니다.")
                    logging.warning(f"Microsoft Store에서 '{distro_name}'을(를) 검색하여 수동으로 설치하는 것을 권장합니다.")
                    ensure_slept(seconds=15, setup_op=SetupOpsForEnsureSlept.SILENT)
                    continue  # 설치를 진행하지 않고 메뉴로 돌아감

                logging.info(f"WSL distro '{distro_name}'을(를) 설치합니다.")
                try:
                    subprocess.run(f"wsl --install -d {distro_name}", shell=True, check=True)
                    logging.info(f"'{distro_name}' distro 설치 명령이 실행되었습니다. 설치가 완료될 때까지 기다려주세요.")
                except subprocess.CalledProcessError as e:
                    logging.error(f"WSL 설치 중 오류 발생: {e}")

            elif operation_option == OP_DISTROS_INFO:
                logging.info("WSL distro OS/용량 정보 및 상태를 출력합니다.")
                try:
                    logging.info("--- 설치된 WSL distro 목록 ---")
                    subprocess.run("wsl -l -v", shell=True, check=True)
                    for distro_name_installed in self.get_wsl_distro_names_installed():
                        logging.info(f"--- '{distro_name_installed}' distro 내부 디스크 사용량 ---")
                        subprocess.run(f"wsl -d {distro_name_installed} df -h", shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    logging.error(f"WSL 정보 출력 중 오류 발생: {e}")
            else:
                logging.warning("유효하지 않은 옵션입니다. 다시 선택해주세요.")

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
        except Exception:
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
        self.ensure_command_executed_to_wsl_distro_as_root_account(distro_name, sh)
