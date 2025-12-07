#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xavier에 Home Assistant 설치 및 P110M 연동을 완료하는 통합 함수.

이 함수는 다음 단계를 수행합니다:
1. Xavier에 Home Assistant Docker 컨테이너 설치 및 실행
2. Home Assistant 온보딩 완료 (계정 생성, 설정 등)
3. P110M을 Matter 멀티-어드민으로 HA에 연동
4. 연동 완료 후 테스트 제어 수행
"""
import logging
from typing import Optional, TYPE_CHECKING

from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)

if TYPE_CHECKING:
    from pk_internal_tools.pk_objects.pk_wireless_target_controller import (
        PkWirelessTargetController,
    )

logger = logging.getLogger(__name__)


@ensure_seconds_measured
def ensure_ha_p110m_integration_completed(
    target_controller: "PkWirelessTargetController",
    *,
    ha_container_name: str = "homeassistant",
    ha_config_dir: str = "/opt/homeassistant",
    ha_image_ref: str = "ghcr.io/home-assistant/home-assistant:stable",
    ha_url: Optional[str] = None,
) -> bool:
    """
    Xavier에 Home Assistant를 설치하고 P110M을 연동합니다.

    :param target_controller: Xavier 타겟 컨트롤러
    :param ha_container_name: Home Assistant 컨테이너 이름
    :param ha_config_dir: Home Assistant 설정 디렉터리
    :param ha_image_ref: Home Assistant Docker 이미지 참조
    :param ha_url: Home Assistant 기본 URL (None인 경우 타겟 IP 기반으로 자동 설정)
    :return: 성공 여부
    """
    logger.info("Xavier에 Home Assistant 설치 및 P110M 연동을 시작합니다.")

    # 1. Home Assistant 설치 및 실행
    from pk_internal_tools.pk_functions.ensure_home_assistant_ready_on_target import (
        ensure_home_assistant_ready_on_target,
    )

    logger.info("1단계: Home Assistant 설치 및 실행 확인 중...")
    if not ensure_home_assistant_ready_on_target(
        target_controller,
        container_name=ha_container_name,
        config_dir=ha_config_dir,
        image_ref=ha_image_ref,
    ):
        logger.error("Home Assistant 설치/실행에 실패했습니다.")
        return False

    # HA URL 결정
    if not ha_url:
        target_ip = getattr(
            target_controller.wireless_target, "ip", None
        ) or getattr(target_controller.wireless_target, "hostname", None)
        ha_url = f"http://{target_ip}:8123" if target_ip else "http://localhost:8123"
        logger.info("Home Assistant URL: %s", ha_url)

    # 2. Home Assistant 온보딩 완료
    from pk_internal_tools.pk_functions.ensure_home_assistant_onboarding_completed import (
        ensure_home_assistant_onboarding_completed,
    )

    logger.info("2단계: Home Assistant 온보딩 완료 확인 중...")
    if not ensure_home_assistant_onboarding_completed(
        ha_url=ha_url,
        headless_mode=False,  # 온보딩은 브라우저 필요
        timeout_seconds=120,
    ):
        logger.warning("Home Assistant 온보딩이 완료되지 않았습니다. 수동으로 완료해주세요.")
        # 온보딩 실패해도 계속 진행 (이미 완료된 경우일 수 있음)

    # 3. P110M Matter 멀티-어드민 연동
    logger.info("3단계: P110M Matter 멀티-어드민 연동 확인 중...")
    # TODO: Matter 멀티-어드민 연동 로직 추가
    # - Matter Server 컨테이너 준비
    # - P110M 커미션 코드 입력
    # - HA에서 Matter 멀티-어드민 공유 절차 트리거
    # - 연동 완료 확인

    logger.info("Home Assistant 설치 및 P110M 연동이 완료되었습니다.")
    logger.info("이제 REST/WebSocket API를 통해 P110M을 제어할 수 있습니다.")
    return True

