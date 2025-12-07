#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xavier에서 Wi-Fi 네트워크에 연결하는 함수.

Wi-Fi USB가 연결된 Xavier를 무선 네트워크에 연결합니다.
"""
import logging
from typing import Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)
from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
    PkWirelessTargetController,
)
from pk_internal_tools.pk_objects.pk_identifier import PkDevice
from pk_internal_tools.pk_objects.pk_operation_options import (
    SetupOpsForPkWirelessTargetController,
)
from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
    ensure_env_var_completed_2025_11_24,
)
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

logger = logging.getLogger(__name__)


@ensure_seconds_measured
def ensure_xavier_wifi_connected(
    wifi_ssid: Optional[str] = None,
    wifi_password: Optional[str] = None,
    wifi_interface: Optional[str] = None,
) -> bool:
    """
    Xavier에서 Wi-Fi 네트워크에 연결합니다.
    
    :param wifi_ssid: Wi-Fi 네트워크 이름 (SSID)
    :param wifi_password: Wi-Fi 비밀번호
    :param wifi_interface: Wi-Fi 인터페이스 이름 (예: wlan0, 기본값: 자동 감지)
    :return: 연결 성공 여부
    """
    func_n = get_caller_name()
    
    # Xavier 연결
    try:
        controller = PkWirelessTargetController(
            identifier=PkDevice.jetson_agx_xavier,
            setup_op=SetupOpsForPkWirelessTargetController.TARGET,
        )
    except Exception as e:
        logger.error("Xavier 연결 실패: %s", e, exc_info=True)
        return False
    
    # Wi-Fi 인터페이스 확인
    if not wifi_interface:
        logger.info("Wi-Fi 인터페이스 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
            cmd="nmcli device status | grep wifi",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        wifi_interfaces = []
        if exit_code == 0 and stdout:
            # 모든 Wi-Fi 인터페이스 찾기
            for line in stdout:
                if "wlan" in line.lower() or "wlp" in line.lower():
                    parts = line.split()
                    if parts:
                        interface_name = parts[0]
                        wifi_interfaces.append(interface_name)
        
        if wifi_interfaces:
            # 여러 인터페이스가 있으면 wlan1 우선, 없으면 첫 번째 사용
            if "wlan1" in wifi_interfaces:
                wifi_interface = "wlan1"
                logger.info("wlan1 인터페이스를 사용합니다.")
            else:
                wifi_interface = wifi_interfaces[0]
                logger.info("Wi-Fi 인터페이스 '%s'를 사용합니다. (발견된 인터페이스: %s)", wifi_interface, ", ".join(wifi_interfaces))
        else:
            logger.warning("Wi-Fi 인터페이스를 찾을 수 없습니다. 'wlan0'을 기본값으로 사용합니다.")
            wifi_interface = "wlan0"
    
    logger.info("Wi-Fi 인터페이스: %s", wifi_interface)
    
    # Wi-Fi 네트워크 스캔 (인터페이스 지정)
    logger.info("사용 가능한 Wi-Fi 네트워크 스캔 중... (인터페이스: %s)", wifi_interface)
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd=f"sudo nmcli device wifi list ifname {wifi_interface} --rescan yes",
        timeout_seconds=30,
        use_sudo=True,
    )
    
    if exit_code == 0 and stdout:
        logger.info("사용 가능한 Wi-Fi 네트워크:")
        for line in stdout:
            logger.info("  %s", line)
    
    # SSID 입력받기
    if not wifi_ssid:
        wifi_ssid = ensure_env_var_completed_2025_11_24(
            key_name="XAVIER_WIFI_SSID",
            func_n=func_n,
            guide_text="연결할 Wi-Fi 네트워크 이름(SSID)을 입력하세요:",
        )
    
    if not wifi_ssid:
        logger.error("Wi-Fi SSID가 입력되지 않았습니다.")
        return False
    
    # 비밀번호 입력받기 (WPA/WPA2 네트워크인 경우)
    if not wifi_password:
        import getpass
        from pk_internal_tools.pk_functions.get_env_var_name_id import get_env_var_id
        from pk_internal_tools.pk_functions.ensure_pk_env_file_setup import (
            ensure_pk_env_file_setup,
        )
        from dotenv import get_key
        
        env_path = ensure_pk_env_file_setup()
        env_var_id = get_env_var_id("WIFI_PASSWORD", func_n)
        
        try:
            wifi_password = get_key(env_path, env_var_id)
        except Exception:
            wifi_password = None
        
        if not wifi_password:
            logger.info("연결할 Wi-Fi 네트워크 '%s'의 비밀번호를 입력하세요:", wifi_ssid)
            # 마스킹된 패스워드 입력 함수
            import sys
            import platform
            
            def get_password_masked(prompt: str) -> str:
                """마스킹된 패스워드 입력 (Windows/Linux 지원)"""
                password = ""
                sys.stdout.write(prompt)
                sys.stdout.flush()
                
                if platform.system() == "Windows":
                    import msvcrt
                    while True:
                        char = msvcrt.getch()
                        if char == b'\r':  # Enter
                            sys.stdout.write('\n')
                            break
                        elif char == b'\x08':  # Backspace
                            if len(password) > 0:
                                password = password[:-1]
                                sys.stdout.write('\b \b')
                                sys.stdout.flush()
                        else:
                            password += char.decode('utf-8', errors='ignore')
                            sys.stdout.write('*')
                            sys.stdout.flush()
                else:
                    # Linux/Mac
                    import termios
                    import tty
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(sys.stdin.fileno())
                        while True:
                            char = sys.stdin.read(1)
                            if char == '\r' or char == '\n':  # Enter
                                sys.stdout.write('\n')
                                break
                            elif char == '\x7f' or char == '\b':  # Backspace
                                if len(password) > 0:
                                    password = password[:-1]
                                    sys.stdout.write('\b \b')
                                    sys.stdout.flush()
                            else:
                                password += char
                                sys.stdout.write('*')
                                sys.stdout.flush()
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
                return password
            
            wifi_password = get_password_masked(f"Wi-Fi 네트워크 '{wifi_ssid}' 비밀번호: ").strip()
    
    # 연결 전 네트워크 존재 확인
    logger.info("연결 전 네트워크 '%s' 존재 여부 확인 중... (인터페이스: %s)", wifi_ssid, wifi_interface)
    check_stdout, check_stderr, check_exit = controller.ensure_command_to_wireless_target(
        cmd=f"sudo nmcli device wifi list ifname {wifi_interface} | grep -i '{wifi_ssid}'",
        timeout_seconds=10,
        use_sudo=True,
    )
    
    if check_exit != 0 or not check_stdout:
        logger.warning("네트워크 '%s'를 현재 스캔 결과에서 찾을 수 없습니다. 재스캔을 시도합니다...", wifi_ssid)
        # 재스캔
        controller.ensure_command_to_wireless_target(
            cmd=f"sudo nmcli device wifi rescan ifname {wifi_interface}",
            timeout_seconds=10,
            use_sudo=True,
        )
        import time
        time.sleep(2)  # 스캔 완료 대기
    
    # Wi-Fi 연결
    logger.info("Wi-Fi 네트워크 '%s'에 연결 시도 중... (인터페이스: %s)", wifi_ssid, wifi_interface)
    
    if wifi_password:
        cmd = f'sudo nmcli device wifi connect "{wifi_ssid}" password "{wifi_password}" ifname {wifi_interface}'
    else:
        cmd = f'sudo nmcli device wifi connect "{wifi_ssid}" ifname {wifi_interface}'
    
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd=cmd,
        timeout_seconds=30,
        use_sudo=True,
    )
    
    if exit_code == 0:
        logger.info("Wi-Fi 연결 성공!")
        
        # 연결 확인
        logger.info("연결 상태 확인 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
            cmd=f"ip addr show {wifi_interface} | grep 'inet '",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code == 0 and stdout:
            for line in stdout:
                logger.info("Wi-Fi IP 주소: %s", line.strip())
        
        # P110M과 같은 네트워크인지 확인
        logger.info("P110M 연결 테스트 중...")
        stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
            cmd="ping -c 2 192.168.0.15",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code == 0:
            logger.info("✅ P110M과 같은 네트워크에 연결되었습니다!")
        else:
            logger.warning("⚠️ P110M으로 ping 테스트 실패. IP 주소를 확인하세요.")
        
        return True
    else:
        logger.error("Wi-Fi 연결 실패:")
        if stderr:
            for line in stderr:
                logger.error("  %s", line)
        return False

