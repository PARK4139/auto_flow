#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xavier에서 사용 가능한 Wi-Fi 네트워크 목록을 조회하는 함수.
"""
import logging
from typing import List, Dict, Any, Optional

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

logger = logging.getLogger(__name__)


@ensure_seconds_measured
def ensure_pk_xavier_wifi_listed() -> List[Dict[str, Any]]:
    """
    Xavier에서 사용 가능한 Wi-Fi 네트워크 목록을 조회합니다.
    
    :return: Wi-Fi 네트워크 목록
        형식: [
            {
                "ssid": str,
                "signal": int,
                "security": str,
                "in_use": bool,
            },
            ...
        ]
    """
    # Xavier 연결
    try:
        controller = PkWirelessTargetController(
            identifier=PkDevice.jetson_agx_xavier,
            setup_op=SetupOpsForPkWirelessTargetController.TARGET,
        )
    except Exception as e:
        logger.error("Xavier 연결 실패: %s", e, exc_info=True)
        return []
    
    # Wi-Fi 네트워크 스캔 (rescan으로 최신 목록 가져오기)
    logger.info("Xavier에서 사용 가능한 Wi-Fi 네트워크 스캔 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd="sudo nmcli device wifi list --rescan yes",
        timeout_seconds=30,
        use_sudo=True,
    )
    
    if exit_code != 0:
        logger.error("Wi-Fi 네트워크 스캔 실패")
        if stderr:
            for line in stderr:
                logger.error("  %s", line)
        return []
    
    # 결과 파싱
    wifi_networks = []
    
    if stdout:
        # 헤더 라인 건너뛰기 (첫 번째 라인)
        for line in stdout[1:]:
            line = line.strip()
            if not line:
                continue
            
            # nmcli 출력 파싱
            # 형식: "IN-USE  BSSID              SSID                  MODE   CHAN  RATE        SIGNAL  BARS  SECURITY"
            # 예: "        00:07:89:41:E0:42  olleh_WiFi_E03F       Infra  7     130 Mbit/s  100     ▂▄▆█  WPA1 WPA2"
            # 예: "*       58:86:94:72:B2:E6  skyiptimeB2E5         Infra  1     270 Mbit/s  65      ▂▄▆_  WPA2"
            
            # IN-USE 컬럼 확인 (* 표시 여부)
            in_use = line.strip().startswith("*")
            
            # 공백으로 분리
            parts = line.split()
            
            if len(parts) >= 3:
                # IN-USE가 "*"인 경우: parts[0] = "*", parts[1] = BSSID, parts[2] = SSID
                # IN-USE가 비어있는 경우: parts[0] = BSSID, parts[1] = SSID
                ssid_index = 2 if in_use else 1
                
                if ssid_index < len(parts):
                    ssid = parts[ssid_index]
                    
                    # SSID가 따옴표로 감싸져 있을 수 있음
                    if ssid.startswith('"') and ssid.endswith('"'):
                        ssid = ssid[1:-1]
                    
                    # SSID가 "--"인 경우 (숨겨진 네트워크) 건너뛰기
                    if ssid == "--":
                        continue
                    
                    # Signal 강도 찾기 (숫자로만 구성된 부분, 0-100 범위)
                    signal = None
                    security = "Unknown"
                    
                    for part in parts:
                        # Signal은 보통 숫자로만 구성 (0-100)
                        if part.isdigit() and 0 <= int(part) <= 100:
                            signal = int(part)
                        # Security는 WPA, WPA2, WEP, Open 등 (여러 개일 수 있음: "WPA1 WPA2")
                        if part.startswith("WPA") or part in ["WEP", "Open"]:
                            if security == "Unknown":
                                security = part
                            else:
                                security += " " + part
                    
                    wifi_networks.append({
                        "ssid": ssid,
                        "signal": signal or 0,
                        "security": security,
                        "in_use": in_use,
                    })
    
    logger.info("발견된 Wi-Fi 네트워크: %d개", len(wifi_networks))
    for network in wifi_networks:
        status = " [현재 연결됨]" if network["in_use"] else ""
        logger.info("  - %s (신호: %s%%, 보안: %s)%s", 
                   network["ssid"], 
                   network["signal"], 
                   network["security"],
                   status)
    
    return wifi_networks


@ensure_seconds_measured
def ensure_pk_xavier_wifi_status() -> Optional[Dict[str, Any]]:
    """
    Xavier의 현재 Wi-Fi 연결 상태를 조회합니다.
    
    :return: Wi-Fi 연결 상태 정보 또는 None
        형식: {
            "interface": str,
            "ssid": str,
            "ip_address": str,
            "connected": bool,
        }
    """
    # Xavier 연결
    try:
        controller = PkWirelessTargetController(
            identifier=PkDevice.jetson_agx_xavier,
            setup_op=SetupOpsForPkWirelessTargetController.TARGET,
        )
    except Exception as e:
        logger.error("Xavier 연결 실패: %s", e, exc_info=True)
        return None
    
    # Wi-Fi 인터페이스 확인
    logger.info("Xavier Wi-Fi 연결 상태 확인 중...")
    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
        cmd="nmcli device status | grep wifi",
        timeout_seconds=10,
        use_sudo=False,
    )
    
    if exit_code != 0 or not stdout:
        logger.warning("Wi-Fi 인터페이스를 찾을 수 없습니다.")
        return None
    
    # Wi-Fi 인터페이스 찾기
    wifi_interface = None
    wifi_connected = False
    wifi_ssid = None
    
    for line in stdout:
        parts = line.split()
        if len(parts) >= 4:
            interface = parts[0]
            if "wlan" in interface.lower() or "wlp" in interface.lower():
                wifi_interface = interface
                wifi_connected = parts[2] == "connected"
                if wifi_connected and len(parts) >= 4:
                    wifi_ssid = parts[3]
                break
    
    if not wifi_interface:
        logger.warning("Wi-Fi 인터페이스를 찾을 수 없습니다.")
        return None
    
    # IP 주소 확인
    ip_address = None
    if wifi_connected:
        stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
            cmd=f"ip addr show {wifi_interface} | grep 'inet ' | awk '{{print $2}}' | cut -d'/' -f1",
            timeout_seconds=10,
            use_sudo=False,
        )
        
        if exit_code == 0 and stdout:
            ip_address = stdout[0].strip() if stdout else None
    
    status = {
        "interface": wifi_interface,
        "ssid": wifi_ssid,
        "ip_address": ip_address,
        "connected": wifi_connected,
    }
    
    if wifi_connected:
        logger.info("Wi-Fi 연결 상태:")
        logger.info("  인터페이스: %s", wifi_interface)
        logger.info("  SSID: %s", wifi_ssid)
        logger.info("  IP 주소: %s", ip_address)
    else:
        logger.info("Wi-Fi가 연결되어 있지 않습니다. (인터페이스: %s)", wifi_interface)
    
    return status

