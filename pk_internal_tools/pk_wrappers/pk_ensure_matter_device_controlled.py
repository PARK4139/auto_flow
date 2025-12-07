#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import asyncio
import sys
from pathlib import Path

import logging

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from pk_internal_tools.pk_functions.ensure_matter_device_controlled import (
    ensure_matter_device_controlled,
    list_matter_devices,
    ensure_matter_smart_plug_on,
    ensure_pk_p110m_off,
    ensure_pk_p110m_toggle
)


async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(description="Matter 장치 제어 도구")
    parser.add_argument("device", nargs="?", help="장치 식별자 (node_id 또는 이름)")
    parser.add_argument("action", nargs="?", default="toggle",
                        choices=["on", "off", "toggle", "status"],
                        help="수행할 액션 (기본값: toggle)")
    parser.add_argument("--list", "-l", action="store_true", help="연결된 장치 목록 표시")
    parser.add_argument("--commission", "-c", help="새 장치 커미션 코드")
    parser.add_argument("--wifi-ssid", help="Wi-Fi SSID (커미션 시)")
    parser.add_argument("--wifi-password", help="Wi-Fi 비밀번호 (커미션 시)")
    parser.add_argument("--p110m", action="store_true", help="P110M 전용 모드 (node_id=1)")

    args = parser.parse_args()

    logging.info(f"PK Matter 장치 제어 도구")

    # 장치 목록 표시
    if args.list:
        logging.info("연결된 Matter 장치 목록:")
        devices = await list_matter_devices()

        if not devices:
            logging.info("연결된 Matter 장치가 없습니다.")
        else:
            for device in devices:
                logging.info(f"ID: {device['node_id']}, 이름: {device['name']}")
                logging.info(f"제조사: {device['vendor']}, 제품: {device['product']}")
                logging.info(f"타입: {device['type']}, 상태: {device['current_state']}")
                logging.info("")  # Add an empty line for formatting
        return

    # P110M 전용 모드
    if args.p110m:
        logging.info(f"P110M 제어: {args.action}")

        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        commission_code = args.commission or ensure_env_var_completed_2025_11_23(
            "P110M_MATTER_COMMISSION_CODE",
            "Please enter the Matter Commission Code: ",
        )  # Use ensure_env_var_completed as fallback

        if not commission_code:  # Ensure we got a valid code
            logging.error("오류: 커미션 코드를 얻을 수 없습니다. 환경 변수를 설정하거나 --commission 옵션을 사용하세요.")
            sys.exit(1)

        if args.action == "on":
            success = await ensure_matter_smart_plug_on(commission_code)
        elif args.action == "off":
            success = await ensure_pk_p110m_off(commission_code)
        else:  # toggle
            success = await ensure_pk_p110m_toggle(commission_code)

        if success:
            logging.info("P110M 제어 성공")
        else:
            logging.error("❌ P110M 제어 실패")
        return

    # 일반 장치 제어
    if not args.device:
        logging.error("오류: 장치 식별자를 지정해주세요.")
        logging.info("사용법: python {} <device_id> <action>".format(sys.argv[0]))
        logging.info("또는 --list 옵션으로 사용 가능한 장치를 확인하세요.")
        sys.exit(1)

    logging.info(f"장치 제어: {args.device} -> {args.action}")

    success = await ensure_matter_device_controlled(
        device_identifier=args.device,
        action=args.action,
        commission_code=args.commission,
        wifi_ssid=args.wifi_ssid,
        wifi_password=args.wifi_password
    )

    if success:
        logging.info("장치 제어 성공")
    else:
        logging.error("❌ 장치 제어 실패")
        sys.exit(1)


if __name__ == "__main__":
    # Add logging setup for wrapper script
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logging.error(f"# pk_error\n{e}")
        sys.exit(1)
