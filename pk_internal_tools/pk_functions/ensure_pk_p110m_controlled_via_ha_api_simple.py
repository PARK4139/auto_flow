#!/usr/bin/env python3

"""
Xavier에서 Home Assistant REST API를 통해 P110M을 간단히 제어하는 함수.

이 함수는 Xavier에서 직접 실행할 수 있는 간단한 인터페이스를 제공합니다.
"""
import logging
import os
import sys
from typing import Optional

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def control_p110m_simple(action: str, entity_id: Optional[str] = None) -> bool:
    """
    Xavier에서 Home Assistant REST API를 통해 P110M을 간단히 제어합니다.
    
    사용법:
        python ensure_pk_p110m_controlled_via_ha_api_simple.py on
        python ensure_pk_p110m_controlled_via_ha_api_simple.py off
        python ensure_pk_p110m_controlled_via_ha_api_simple.py toggle
    
    환경변수:
        HA_URL: Home Assistant URL (예: http://119.207.161.56:8123)
        HA_TOKEN: Home Assistant Long-Lived Access Token
        HA_ENTITY: Entity ID (예: switch.tapo_p110m_plug)
    
    :param action: 제어 액션 ("on", "off", "toggle")
    :param entity_id: Entity ID (None인 경우 환경변수 HA_ENTITY 사용)
    :return: 제어 성공 여부
    """
    if action not in ("on", "off", "toggle"):
        logger.error("지원하지 않는 액션입니다: %s (지원: on, off, toggle)", action)
        return False
    
    # 환경변수에서 설정값 가져오기
    ha_url = os.getenv("HA_URL", "http://localhost:8123")
    ha_token = os.getenv("HA_TOKEN")
    entity_id = entity_id or os.getenv("HA_ENTITY", "switch.tapo_p110m_plug")
    
    if not ha_token:
        logger.error("HA_TOKEN 환경변수가 설정되어 있지 않습니다.")
        logger.error("사용법: export HA_TOKEN='your_token_here'")
        return False
    
    logger.info("P110M 제어 시작: action=%s, entity=%s, ha_url=%s", action, entity_id, ha_url)
    
    # toggle 액션의 경우 현재 상태를 먼저 조회
    if action == "toggle":
        current_state = _get_entity_state(ha_url, entity_id, ha_token)
        if current_state is None:
            logger.error("현재 상태를 조회할 수 없어 toggle을 수행할 수 없습니다.")
            return False
        
        next_action = "off" if current_state == "on" else "on"
        logger.info("현재 상태: %s -> %s로 전환", current_state, next_action)
        action = next_action
    
    # Home Assistant 서비스 호출
    success = _call_switch_service(ha_url, entity_id, action, ha_token)
    
    if success:
        logger.info("P110M 제어 성공: %s", action)
    else:
        logger.error("P110M 제어 실패: %s", action)
    
    return success


def _get_entity_state(ha_url: str, entity_id: str, ha_token: str) -> Optional[str]:
    """Entity의 현재 상태를 조회합니다."""
    state_url = ha_url.rstrip("/") + f"/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.get(state_url, headers=headers, timeout=5)
        if resp.status_code // 100 == 2:
            state_data = resp.json()
            current_state = state_data.get("state")
            logger.debug("Entity %s 현재 상태: %s", entity_id, current_state)
            return current_state
        else:
            logger.error("상태 조회 실패: %s %s", resp.status_code, resp.text)
            return None
    except Exception as e:
        logger.error("상태 조회 중 예외 발생: %s", e)
        return None


def _call_switch_service(ha_url: str, entity_id: str, action: str, ha_token: str) -> bool:
    """Home Assistant switch 서비스를 호출합니다."""
    service_url = ha_url.rstrip("/") + f"/api/services/switch/turn_{action}"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    payload = {"entity_id": entity_id}
    
    try:
        resp = requests.post(service_url, headers=headers, json=payload, timeout=5)
        if resp.status_code // 100 == 2:
            logger.info("서비스 호출 성공: %s %s", action, entity_id)
            return True
        else:
            logger.error("서비스 호출 실패: %s %s -> %s %s", action, entity_id, resp.status_code, resp.text)
            return False
    except Exception as e:
        logger.error("서비스 호출 중 예외 발생: %s", e)
        return False


def main():
    """CLI 진입점"""
    if len(sys.argv) < 2:
        print("사용법: python ensure_pk_p110m_controlled_via_ha_api_simple.py <action> [entity_id]")
        print("action: on, off, toggle")
        print("entity_id: 선택사항 (기본값: 환경변수 HA_ENTITY 또는 switch.tapo_p110m_plug)")
        print("\n환경변수:")
        print("HA_URL: Home Assistant URL (예: http://119.207.161.56:8123)")
        print("HA_TOKEN: Home Assistant Long-Lived Access Token")
        print("HA_ENTITY: Entity ID (예: switch.tapo_p110m_plug)")
        sys.exit(1)
    
    action = sys.argv[1]
    entity_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = control_p110m_simple(action, entity_id)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

