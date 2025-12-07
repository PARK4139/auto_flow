#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P110M Matter 장치 완전 자동화 제어
- Wi-Fi 연결 감지 → 네트워크 범위 계산 → P110M 발견 → 커미셔닝 → 제어
- 관리자 권한 확인 및 효율적인 실행 순서 최적화
"""

import logging
from typing import Optional, Tuple

FINAL_TOGGLE: Optional[bool] = True  # pk_option: True=ON, False=OFF, None=상태만 확인


# -------------------------- HELPER FUNCTIONS ------------------------------
async def check_wifi_connection_status() -> Tuple[bool, Optional[str]]:
    import asyncio
    import logging
    from pk_internal_tools.pk_functions.ensure_wifi_pw_printed_fixed import ensure_wifi_pw_printed_fixed
    """Wi-Fi 연결 상태 확인"""
    logging.debug("➡️ check_wifi_connection_status 함수 시작")
    try:
        wifi_name, _ = await asyncio.to_thread(ensure_wifi_pw_printed_fixed)

        if wifi_name:
            logging.debug(f"⬅️ check_wifi_connection_status 함수 종료 (Wi-Fi 연결됨: {wifi_name})")
            return True, wifi_name
        else:
            logging.debug("⬅️ check_wifi_connection_status 함수 종료 (Wi-Fi 연결 안됨)")
            return False, None
    except Exception as e:
        logging.debug(f"Wi-Fi 상태 확인 중 오류: {e}")
        logging.debug("⬅️ check_wifi_connection_status 함수 종료 (오류 발생)")
        return False, None


async def detect_local_network_range() -> str:
    import asyncio
    import logging
    import ipaddress
    """로컬 네트워크 범위 자동 감지"""
    logging.debug("➡️ detect_local_network_range 함수 시작")
    try:
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

        # Windows ipconfig로 현재 IP와 서브넷 마스크 확인
        # ipconfig 출력은 CP949 인코딩일 수 있으므로 명시적으로 지정
        result_lines = await asyncio.to_thread(ensure_command_executed, 'ipconfig', encoding='cp949')

        if result_lines:
            current_ip = None
            subnet_mask = None

            for line in result_lines:
                if 'IPv4 Address' in line and '192.168.' in line:
                    current_ip = line.split(':')[-1].strip()
                elif 'Subnet Mask' in line and current_ip:
                    subnet_mask = line.split(':')[-1].strip()
                    break

            if current_ip and subnet_mask:
                # 네트워크 범위 계산
                network = ipaddress.IPv4Network(f"{current_ip}/{subnet_mask}", strict=False)
                network_addr = str(network.network_address)

                # 192.168.0.1-254 형태로 반환
                start_ip = network_addr.rsplit('.', 1)[0] + '.1'
                logging.debug(f"⬅️ detect_local_network_range 함수 종료 (감지된 범위: {start_ip}-254)")
                return f"{start_ip}-254"

        # 기본값 반환
        logging.debug("⬅️ detect_local_network_range 함수 종료 (기본값 반환: 192.168.1.1-254)")
        return "192.168.1.1-254"

    except Exception as e:
        logging.debug(f"네트워크 범위 감지 중 오류: {e}")
        logging.debug("⬅️ detect_local_network_range 함수 종료 (오류 발생, 기본값 반환)")
        return "192.168.1.1-254"


# ------------------------------ MAIN FUNCTION -----------------------------------
async def ensure_matter_smart_plug_on() -> bool:
    from pk_internal_tools.pk_functions.ensure_sensitive_info_masked import ensure_sensitive_info_masked

    import asyncio
    import logging
    import platform
    """
    P110M 완전 자동화 제어 함수
    Wi-Fi 연결 감지 → 네트워크 범위 자동 계산 → P110M 발견 → 커미셔닝 → 제어
    """
    logging.debug("➡️ ensure_matter_smart_plug_on 함수 시작")
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed

        # Get COMMISSION_CODE using the generalized helper function
        commission_code = ensure_env_var_completed_2025_11_23(
            "P110M_MATTER_COMMISSION_CODE",
            "Please enter the Matter Commission Code: ",
        )
        if not commission_code:
            logging.error("Commission Code is not set. Cannot proceed.")
            return False

        logging.debug("🚀 === P110M 완전 자동화 제어 시작")
        # Get DEVICE_MAC using the generalized helper function
        device_mac = ensure_env_var_completed_2025_11_23(
            "P110M_NETWORK_INTERFACE_MAC_ADDRESS",
            "Please enter the Matter Device MAC: ",
        )
        if not device_mac:
            logging.error("Device MAC is not set. Cannot proceed.")
            return False

        logging.debug(f"📋 Commission Code: {ensure_sensitive_info_masked(commission_code)} | MAC: {ensure_sensitive_info_masked(device_mac)}")
        logging.debug(f"🎯 Target action: {FINAL_TOGGLE}")
        logging.debug(f"💻 Platform: {platform.system()}")

        # 0. 관리자 권한 확인 및 자동 상승
        try:
            from pk_internal_tools.pk_functions.ensure_admin_privilege_elevated import ensure_admin_privilege_or_exit
            ensure_admin_privilege_or_exit(auto_elevate=True)
        except Exception as e:
            logging.error(f"관리자 권한 처리 중 심각한 오류 발생: {e}")
            return False

        # n. Wi-Fi 연결 상태 확인
        wifi_connected, current_network = await check_wifi_connection_status()
        if not wifi_connected:
            logging.debug("⚠️ Wi-Fi가 연결되지 않았습니다. Wi-Fi 연결 후 다시 시도하세요.")
            logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (Wi-Fi 연결 실패)")
            return False

        logging.debug(f"📶 Wi-Fi 연결됨: {current_network}")

        # n. 로컬 네트워크 범위 자동 감지
        local_ip_range = await detect_local_network_range()
        logging.debug(f"🔍 감지된 네트워크 범위: {local_ip_range}")

        # n. P110M 자동 발견 및 제어 (Windows 실용적 방법 우선)
        if platform.system().lower() == "windows":
            try:
                from pk_internal_tools.pk_functions.ensure_pk_p110m_practical_control import P110MPracticalController

                logging.debug("🔎 P110M 장치 자동 검색 중...")
                controller = P110MPracticalController()

                # 올바른 네트워크 범위 설정
                controller.target_network_range = local_ip_range
                devices = await controller.discover_p110m_devices()

                if devices:
                    device_ip = devices[0]["ip"]
                    device_mac = devices[0].get("mac", "unknown")
                    logging.debug(f"✅ P110M 장치 발견: {device_ip} (MAC: {device_mac})")

                    # 제어 실행
                    if FINAL_TOGGLE is not None:
                        success = await controller.control_via_kasa_protocol(device_ip, FINAL_TOGGLE)
                        if success:
                            action = "켜기" if FINAL_TOGGLE else "끄기"
                            logging.debug(f"🎉 P110M {action} 성공! ({device_ip})")
                            logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (Kasa 제어 성공)")
                            return True
                        else:
                            logging.debug(f"❌ P110M Kasa 제어 실패 ({device_ip})")
                    else:
                        logging.debug(f"📋 P110M 장치 상태 확인 완료 ({device_ip})")
                        logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (장치 상태 확인 완료)")
                        return True
                else:
                    # 장치가 없으면 즉시 커미셔닝 시도 (효율적)
                    logging.debug("🔍 P110M 장치를 찾을 수 없습니다.")
                    logging.debug("💡 P110M LED 상태 확인: 주황+초록 점멸 = 커미셔닝 필요")

                    # 즉시 커미셔닝 시도 (시간 낭비 방지)
                    logging.debug("🔧 P110M 자동 커미셔닝 시작...")
                    try:
                        from pk_internal_tools.pk_functions.ensure_matter_commissioning import commission_p110m_auto

                        commission_success = await commission_p110m_auto(commission_code)

                        if commission_success:
                            logging.debug("✅ P110M 커미셔닝 성공! 장치 재검색...")

                            # 커미셔닝 후 장치 재검색
                            await asyncio.sleep(10)  # 장치 부팅 대기
                            devices = await controller.discover_p110m_devices()

                            if devices:
                                device_ip = devices[0]["ip"]
                                logging.debug(f"🎉 커미셔닝된 P110M 발견: {device_ip}")

                                if FINAL_TOGGLE is not None:
                                    success = await controller.control_via_kasa_protocol(device_ip, FINAL_TOGGLE)
                                    if success:
                                        action = "켜기" if FINAL_TOGGLE else "끄기"
                                        logging.debug(f"🎉 P110M {action} 성공! ({device_ip})")
                                        logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (커미셔닝 후 Kasa 제어 성공)")
                                    return True
                                logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (커미셔닝 후 장치 재발견)")
                                return True
                            else:
                                logging.debug("커미셔닝 후에도 장치를 찾을 수 없습니다.")
                        else:
                            logging.debug("⚠️ 자동 커미셔닝 실패 - 수동 설정 필요")
                            logging.debug("📱 TP-Link Tapo 앱으로 수동 설정하세요:")
                            logging.debug(f"Commission Code: {ensure_sensitive_info_masked(commission_code)}")
                            logging.debug(f"Wi-Fi: {current_network}")

                    except Exception as ce:
                        logging.debug(f"커미셔닝 중 오류: {ce}")
                        logging.debug("📱 수동 해결: TP-Link Tapo 앱 사용 권장")

                    # 커미셔닝 시도 후에는 다른 방법들은 건너뛰기
                    logging.debug("커미셔닝 단계이므로 다른 제어 방법은 건너뜁니다.")
                    logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (자동 커미셔닝 실패)")
                    return False

            except Exception as e:
                logging.debug(f"실용적 제어 중 오류: {e}")

        # n. Docker 기반 Matter 제어 시도 (백업)
        try:
            logging.debug("🐳 Docker 기반 Matter 제어 시도...")
            from pk_internal_tools.pk_functions.ensure_matter_docker_control import control_p110m_via_docker_matter

            action = "on" if FINAL_TOGGLE else "off" if FINAL_TOGGLE is False else "toggle"
            result = await control_p110m_via_docker_matter(
                commission_code=commission_code,
                action=action
            )

            if result:
                logging.debug("✅ Docker Matter 제어 성공!")
                logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (Docker Matter 제어 성공)")
                return True

        except Exception as e:
            logging.debug(f"Docker Matter 제어 중 오류: {e}")

        # n. 최종 실패
        logging.debug("❌ 모든 제어 방법이 실패했습니다.")
        logging.debug("💡 해결 방법:")
        logging.debug("  1. 관리자 PowerShell에서 실행")
        logging.debug("  2. TP-Link Tapo 앱으로 수동 커미셔닝")
        logging.debug(f"3. Commission Code: {commission_code}")
        logging.debug("⬅️ ensure_matter_smart_plug_on 함수 종료 (최종 실패)")
        return False

    except Exception as e:
        logging.debug(f"❌ P110M 완전 자동화 제어 중 오류: {e}")
        import traceback
        traceback.print_exc()
        return False


# ------------------------------ COMPATIBILITY WRAPPER -----------------------------------
async def ensure_matter_smart_plug_on_async() -> bool:
    """Compatibility wrapper (async). Run and print result directly."""
    result = await ensure_matter_smart_plug_on()
    if result:
        logging.debug("✅ P110M 제어 성공!")
    else:
        logging.debug("❌ P110M 제어 실패")
    return result
