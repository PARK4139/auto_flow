from __future__ import annotations

import logging
import re
import traceback
from typing import Optional

import rich
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import \
    ensure_pk_wrapper_exception_routine_done
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_colors import PkColors
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine


@ensure_seconds_measured
def ensure_wifi_printed_of_remote_target(
        target_device: Optional[PkDevice] = None,
        target_ip: Optional[str] = None,
        target_user: Optional[str] = None,
        target_pw: Optional[str] = None,
) -> bool:
    """
    원격 대상 장치의 Wi-Fi 정보를 가져와 출력합니다.

    Args:
        target_device: 원격 대상 장치 (예: PkDevice.jetson_agx_xavier). None인 경우 사용자에게 선택을 요청합니다.
        target_ip: 원격 대상의 IP 주소.
        target_user: 원격 대상의 사용자 이름.
        target_pw: 원격 대상의 비밀번호.

    Returns:
        Wi-Fi 정보를 성공적으로 가져와 출력했으면 True, 아니면 False.
    """
    func_n = get_caller_name()

    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}원격 대상 Wi-Fi 정보 출력 시작{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    try:
        if target_device is None:
            pk_devices_enum = [PkDevice.jetson_agx_xavier, PkDevice.jetson_nano]  # TODO: 다른 디바이스 추가 필요
            pk_device_names = [item.value for item in pk_devices_enum]

            selected_device_name = ensure_value_completed(
                key_name="remote_target_device_selection",
                func_n=func_n,
                guide_text="Wi-Fi 정보를 확인할 원격 대상 장치를 선택해주세요:",
                options=pk_device_names,
            )
            target_device = next((item for item in pk_devices_enum if item.value == selected_device_name), None)

            if target_device is None:
                logging.error("원격 대상 장치가 선택되지 않았습니다. 작업을 중단합니다.")
                return False

        # --- Get Target Connection Info ---
        target_device_upper_name = target_device.name.upper()
        if not target_ip:
            target_ip = ensure_env_var_completed(
                key_name=f"{target_device_upper_name}_IP",
                guide_text=f"{target_device.value}의 IP 주소를 입력해주세요:",
            )
        if not target_user:
            target_user = ensure_env_var_completed(
                key_name=f"{target_device_upper_name}_USER",
                guide_text=f"{target_device.value}의 사용자 이름을 입력해주세요:",
            )
        if not target_pw:
            target_pw = ensure_env_var_completed(
                key_name=f"{target_device_upper_name}_PW",
                guide_text=f"{target_device.value}의 비밀번호를 입력해주세요:",
            )

        if not all([target_ip, target_user, target_pw]):
            logging.error(f"{target_device.value} 연결 정보를 가져올 수 없습니다. 작업을 중단합니다.")
            return False

        # --- Initialize Controller ---
        controller = PkRemoteTargetEngine(
            identifier=target_device,
            
            ip=target_ip,
            user_n=target_user,
            pw=target_pw
        )
        logging.info(f"Initialized controller for target: {target_device.value}")

        # --- Fetch Wi-Fi Info ---
        # OS별로 Wi-Fi 정보 가져오는 명령어가 다를 수 있음.
        # 여기서는 Linux (Ubuntu/Debian 계열) 기준으로 nmcli 사용.
        # TODO: Windows나 다른 OS 지원 추가

        # nmcli가 설치되어 있는지 확인
        stdout_check, stderr_check, exit_code_check = controller.ensure_command_to_remote_target(
            cmd="which nmcli", use_sudo=False, timeout_seconds=5
        )
        if exit_code_check != 0:
            logging.warning(f"원격 대상 ({target_device.value})에 nmcli가 설치되어 있지 않거나 경로에 없습니다.")
            # 다른 명령어로 시도 (예: iwconfig, ip a)
            logging.info("iwconfig 명령어로 Wi-Fi 정보 가져오기를 시도합니다.")
            wifi_command = "iwconfig"
        else:
            wifi_command = "nmcli device wifi list"

        stdout, stderr, exit_code = controller.ensure_command_to_remote_target(
            cmd=wifi_command, use_sudo=False
        )

        if exit_code == 0 and stdout:
            if "nmcli" in wifi_command:
                try:
                    console = Console()

                    # Columns for nmcli are fixed
                    columns = ["IN-USE", "BSSID", "SSID", "MODE", "CHAN", "RATE", "SIGNAL", "BARS", "SECURITY"]

                    table = Table(
                        show_header=True,
                        header_style="bold dark_orange",
                        border_style="dim",
                        box=rich.box.SQUARE
                    )

                    col_configs = {
                        "IN-USE": {"justify": "center"},
                        "BSSID": {"min_width": 17, "no_wrap": True},
                        "SSID": {"min_width": 20},
                        "RATE": {"min_width": 12, "no_wrap": True},
                        "SIGNAL": {"no_wrap": True},
                        "SECURITY": {"min_width": 10, "no_wrap": True},
                    }

                    for col_name in columns:
                        config = col_configs.get(col_name, {})
                        table.add_column(col_name, **config)

                    # Find data lines (not empty and not headers)
                    data_lines = [
                        line.strip() for line in stdout
                        if line.strip() and "BSSID" not in line
                    ]

                    for line in data_lines:
                        # Split by 2 or more spaces
                        row_items = re.split(r'\s{2,}', line)

                        # Handle the IN-USE column, which is only present if '*'
                        if not line.startswith('*'):
                            row_items.insert(0, '')  # Add empty IN-USE field

                        # Ensure row has correct number of columns
                        if len(row_items) == len(columns):
                            table.add_row(*row_items)
                        else:
                            # Log a warning if parsing seems to have failed for a line
                            logging.warning(f"Skipping malformed wifi list line: {line}")

                    panel = Panel(
                        table,
                        title=f"[bold dark_orange]✅ 원격 대상 ({target_device.value}) Wi-Fi 정보[/bold dark_orange]",
                        border_style="dark_orange",
                    )
                    console.print(panel)

                except Exception as e:
                    # Add exception details to the log for better debugging
                    logging.error(f"rich 테이블 생성 중 오류 발생: {e}", exc_info=True)
                    logging.warning("rich 라이브러리로 테이블을 만드는 데 실패했습니다. 원본 출력을 표시합니다.")
                    logging.info(f"✅ 원격 대상 ({target_device.value}) Wi-Fi 정보 (raw):")
                    for line in stdout:
                        logging.info(f" {line}")

            else:  # Fallback for other commands like iwconfig
                logging.info(f"✅ 원격 대상 ({target_device.value}) Wi-Fi 정보:")
                for line in stdout:
                    logging.info(f" {line}")
            return True
        else:
            logging.error(f"원격 대상 ({target_device.value})에서 Wi-Fi 정보를 가져오는 데 실패했습니다.")
            if stderr:
                for line in stderr:
                    logging.error(f"  STDERR: {line}")
            return False

    except Exception as e:
        logging.error(f"원격 대상 Wi-Fi 정보 출력 중 오류 발생: {e}", exc_info=True)
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
        return False
    except BaseException:
        ensure_debugged_verbose(traceback, e)
        return False
