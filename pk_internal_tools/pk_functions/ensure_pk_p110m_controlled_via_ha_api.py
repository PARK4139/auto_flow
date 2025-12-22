#!/usr/bin/env python3

"""
Home Assistant REST API를 통해 P110M 스마트 플러그를 제어하는 함수.

이 함수는 로컬에서 직접 Home Assistant REST API를 호출하여
P110M 장치를 제어합니다.
"""
import logging
import os
from typing import List, Optional, Dict, Any

import requests

from pk_internal_tools.pk_functions.ensure_env_var_completed import (
    ensure_env_var_completed,
)
from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)
from pk_internal_tools.pk_functions.ensure_values_completed import (
    ensure_values_completed,
)


@ensure_seconds_measured
def ensure_pk_p110m_controlled_via_ha_api(
        action: str,
        *,
        entity_id: Optional[str] = None,
        ha_url: Optional[str] = None,
        ha_token: Optional[str] = None,
) -> bool:
    """
    Home Assistant REST API를 통해 P110M 스마트 플러그를 제어합니다.

    :param action: 제어 액션 ("on", "off", "toggle")
    :param entity_id: Home Assistant switch entity ID (예: "switch.tapo_p110m_plug")
                      None인 경우 환경변수 HA_ENTITY 또는 기본값 사용
    :param ha_url: Home Assistant 기본 URL (예: "http://localhost:8123")
                   None인 경우 환경변수 HA_URL 또는 기본값 사용
    :param ha_token: Home Assistant Long-Lived Access Token
                     None인 경우 환경변수 HA_TOKEN 사용
    :return: 제어 성공 여부
    """
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if action not in ("on", "off", "toggle"):
        logging.error("지원하지 않는 액션입니다: %s (지원: on, off, toggle)", action)
        return False

    # fzf를 사용해서 설정값 가져오기
    if not ha_url:
        ha_url = _select_ha_url_via_fzf()
        if not ha_url:
            # HA IP 기반으로 기본값 설정
            try:
                ha_ip = ensure_env_var_completed(
                    key_name="HA_IP",
                    func_n=func_n,
                    guide_text="Home Assistant IP 주소를 입력하세요 (예: 119.207.161.56):",
                )
                default_url = f"http://{ha_ip}:8123" if ha_ip else "http://localhost:8123"
            except Exception as e:
                default_url = "http://localhost:8123"

            ha_url = ensure_env_var_completed(
                key_name="HA_URL",
                func_n="ensure_pk_p110m_controlled_via_ha_api",
                guide_text=f"Home Assistant 기본 URL을 입력하세요 (예: {default_url}):",
                default_value=default_url,
            )

    if not ha_token:
        # 토큰은 민감한 정보이므로 getpass 사용
        import getpass
        from pk_internal_tools.pk_functions.get_pk_env_var_id import get_pk_env_var_id
        from pk_internal_tools.pk_functions.ensure_pk_env_file_setup import (
            ensure_pk_env_file_setup,
        )
        from dotenv import set_key, get_key
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

        # 먼저 환경변수에서 확인
        env_path = ensure_pk_env_file_setup()
        env_var_id = get_pk_env_var_id("HA_TOKEN", "ensure_pk_p110m_controlled_via_ha_api")

        try:
            ha_token = get_key(env_path, env_var_id)
        except Exception as e:
            ha_token = None

        # 환경변수에도 없으면 토큰 생성 안내 후 입력받기
        if not ha_token:
            from pk_internal_tools.pk_functions.ensure_ha_token_obtained import (
                ensure_ha_token_obtained_via_fzf,
            )

            # fzf로 HA URL 선택 후 토큰 생성 안내
            ha_token = ensure_ha_token_obtained_via_fzf(ha_url=ha_url)

            # 토큰 생성 안내를 취소한 경우 직접 입력 요청
            if not ha_token:
                logging.info("Home Assistant Long-Lived Access Token을 입력하세요.")
                logging.info("(입력 내용은 화면에 표시되지 않습니다)")
                ha_token = getpass.getpass("HA_TOKEN: ").strip()

            if ha_token:
                # .env 파일에 저장할지 물어보기
                if not QC_MODE:
                    save_choice = input("이 토큰을 .env 파일에 저장하시겠습니까? (y/n): ").strip().lower()
                else:
                    save_choice = "y"

                if save_choice == "y":
                    try:
                        set_key(env_path, env_var_id, ha_token)
                        logging.info(f"HA_TOKEN이 {env_path}에 저장되었습니다.")
                    except Exception as e:
                        logging.error(f"HA_TOKEN 저장 실패: {e}")

    if not ha_token:
        logging.error("HA_TOKEN이 설정되어 있지 않습니다.")
        return False

    # fzf를 사용해서 Entity ID 선택
    if not entity_id:
        entity_id = _select_ha_entity_via_fzf(ha_url, ha_token)
        if not entity_id:
            entity_id = ensure_env_var_completed(
                key_name="HA_ENTITY",
                func_n="ensure_pk_p110m_controlled_via_ha_api",
                guide_text="Home Assistant switch entity ID를 입력하세요 (예: switch.tapo_p110m_plug):",
                default_value="switch.tapo_p110m_plug",
            )

    # Entity 존재 여부 및 접근 가능 여부 확인
    entity_exists = False
    if entity_id:
        current_state = _get_ha_entity_state(ha_url, entity_id, ha_token)
        if current_state is not None:
            entity_exists = True
            logging.debug("Entity %s 확인됨 (현재 상태: %s)", entity_id, current_state)
        else:
            logging.warning("Entity %s를 찾을 수 없거나 접근할 수 없습니다.", entity_id)

    # Entity가 없거나 접근할 수 없는 경우 Matter 커미션 시도
    if not entity_exists:
        logging.info("P110M이 Home Assistant에 등록되지 않은 것으로 보입니다.")
        logging.info("Matter 커미션을 시도합니다...")

        # Matter Commission Code 입력받기
        commission_code = ensure_env_var_completed(
            key_name="P110M_MATTER_COMMISSION_CODE",
            func_n="ensure_pk_p110m_controlled_via_ha_api",
            guide_text="P110M Matter Commission Code를 입력하세요 (11자리 숫자 또는 QR 코드):",
        )

        if commission_code:
            # Matter 커미션 진행
            commission_success = _try_matter_commission(commission_code)

            if commission_success:
                logging.info("Matter 커미션 성공. 잠시 후 Entity를 다시 확인합니다...")
                import time
                time.sleep(5)  # Matter 서버가 장치를 인식할 시간 확보

                # Entity ID 다시 확인 (Matter 통합으로 생성된 Entity 찾기)
                entity_id = _find_matter_entity_id(ha_url, ha_token, entity_id)

                if not entity_id:
                    logging.warning("커미션 후에도 Entity를 찾을 수 없습니다. 수동으로 확인해주세요.")
                    logging.info("Home Assistant UI에서 Matter 통합을 확인하세요.")
                    return False
            else:
                logging.error("Matter 커미션이 실패했습니다.")
                logging.info("다음을 확인하세요:")
                logging.info("1. P110M과 Xavier가 같은 Wi-Fi 네트워크에 있는지")
                logging.info("2. Commission Code가 올바른지")
                logging.info("3. Home Assistant에서 Matter 통합이 활성화되어 있는지")
                return False
        else:
            logging.error("Matter Commission Code가 입력되지 않았습니다.")
            logging.info("TP-Link 통합을 사용하거나 Matter Commission Code를 입력해주세요.")
            return False

    # toggle 액션의 경우 현재 상태를 먼저 조회
    if action == "toggle":
        current_state = _get_ha_entity_state(ha_url, entity_id, ha_token)
        if current_state is None:
            logging.error("현재 상태를 조회할 수 없어 toggle을 수행할 수 없습니다.")
            return False

        next_action = "off" if current_state == "on" else "on"
        logging.info("현재 상태: %s -> %s로 전환", current_state, next_action)
        action = next_action

    # Home Assistant 서비스 호출
    return _call_ha_switch_service(ha_url, entity_id, action, ha_token)


def get_ha_entity_state(
        entity_id: Optional[str] = None,
        ha_url: Optional[str] = None,
        ha_token: Optional[str] = None,
) -> Optional[str]:
    """
    Home Assistant에서 entity의 현재 상태를 조회합니다 (public API).

    :param entity_id: Entity ID (None인 경우 환경변수 또는 기본값 사용)
    :param ha_url: Home Assistant 기본 URL (None인 경우 환경변수 또는 기본값 사용)
    :param ha_token: Home Assistant Access Token (None인 경우 환경변수 사용)
    :return: 현재 상태 ("on", "off" 등) 또는 None (실패 시)
    """
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 환경변수 또는 인자에서 설정값 가져오기
    if not entity_id:
        entity_id = ensure_env_var_completed(
            key_name="HA_ENTITY",
            func_n="get_ha_entity_state",
            guide_text="Home Assistant switch entity ID를 입력하세요 (예: switch.tapo_p110m_plug):",
            default_value="switch.tapo_p110m_plug",
        )

    if not ha_url:
        # HA IP 기반으로 기본값 설정
        try:

            ha_ip = ensure_env_var_completed(
                key_name="HA_IP",
                func_n=func_n,
                guide_text="Home Assistant IP 주소를 입력하세요 (예: 119.207.161.56):",
            )
            default_url = f"http://{ha_ip}:8123" if ha_ip else "http://localhost:8123"
        except Exception as e:
            default_url = "http://localhost:8123"

        ha_url = ensure_env_var_completed(
            key_name="HA_URL",
            func_n="get_ha_entity_state",
            guide_text=f"Home Assistant 기본 URL을 입력하세요 (예: {default_url}):",
            default_value=default_url,
        )

    if not ha_token:
        ha_token = ensure_env_var_completed(
            key_name="HA_TOKEN",
            func_n="get_ha_entity_state",
            guide_text="Home Assistant Long-Lived Access Token을 입력하세요:",
        )

    if not ha_token:
        logging.error("HA_TOKEN이 설정되어 있지 않습니다.")
        return None

    return _get_ha_entity_state(ha_url, entity_id, ha_token)


def _get_ha_entity_state(ha_url: str, entity_id: str, ha_token: str) -> Optional[str]:
    """
    Home Assistant에서 entity의 현재 상태를 조회합니다 (내부 함수).

    :param ha_url: Home Assistant 기본 URL
    :param entity_id: Entity ID
    :param ha_token: Home Assistant Access Token
    :return: 현재 상태 ("on", "off" 등) 또는 None (실패 시)
    """
    state_url = ha_url.rstrip("/") + f"/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.get(state_url, headers=headers, timeout=10)
        if resp.status_code // 100 == 2:
            state_data = resp.json()
            current_state = state_data.get("state")
            logging.debug("Entity %s 현재 상태: %s", entity_id, current_state)
            return current_state
        else:
            logging.error(
                "상태 조회 실패: %s %s -> %s %s",
                entity_id,
                resp.status_code,
                resp.text,
            )
            return None
    except Exception as e:
        logging.error("상태 조회 중 예외 발생: %s", e, exc_info=True)
        return None


def _select_ha_url_via_fzf() -> Optional[str]:
    """
    fzf를 사용해서 HA URL을 선택합니다.
    HA_IP를 우선적으로 사용합니다.
    """
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # HA IP 가져오기
    ha_ip = None
    try:
        from pk_internal_tools.pk_functions.ensure_env_var_completed import (
            ensure_env_var_completed,
        )

        ha_ip = ensure_env_var_completed(
            key_name="HA_IP",
            func_n=func_n,
            guide_text="Home Assistant IP 주소를 입력하세요 (예: 119.207.161.56):",
        )
    except Exception as e:
        logging.debug("HA IP를 가져오는 중 오류 발생: %s", e)

    # URL 옵션들 (HA IP 우선)
    url_options = []

    # 1. HA IP 기반 URL (가장 우선)
    if ha_ip:
        ha_url_from_ip = f"http://{ha_ip}:8123"
        url_options.append(ha_url_from_ip)
    else:
        ha_url_from_ip = f"http://localhost:8123"
    url_options.extend([
        ha_url_from_ip,
    ])

    # 3. 환경변수에서 저장된 URL들
    env_url = os.getenv("HA_URL")
    if env_url and env_url not in url_options:
        url_options.append(env_url)

    # 중복 제거
    all_urls = list(dict.fromkeys(url_options))

    selected = ensure_values_completed(
        key_name="HA_URL",
        options=all_urls,
        multi_select=False,
        func_n=func_n
    )

    return selected[0] if selected else None


def _select_ha_entity_via_fzf(ha_url: str, ha_token: str) -> Optional[str]:
    """
    fzf를 사용해서 HA switch entity를 선택합니다.
    """
    try:
        entities = _list_ha_switch_entities(ha_url, ha_token)
        if not entities:
            logging.warning("Home Assistant에서 switch entity를 찾을 수 없습니다.")
            return None

        # fzf 옵션 포맷: "entity_id | friendly_name | state"
        options = [
            f"{e['entity_id']} | {e.get('friendly_name', 'N/A')} | {e.get('state', 'unknown')}"
            for e in entities
        ]

        selected = ensure_values_completed(
            key_name="HA_ENTITY",
            options=options,
            multi_select=False,
        )

        if selected:
            # "entity_id | ..." 형식에서 entity_id만 추출
            entity_id = selected[0].split(" | ")[0].strip()
            return entity_id

        return None
    except Exception as e:
        logging.error("fzf를 통한 entity 선택 중 오류 발생: %s", e, exc_info=True)
        return None


def _list_ha_switch_entities(ha_url: str, ha_token: str) -> List[Dict[str, Any]]:
    """
    Home Assistant에서 모든 switch entity 목록을 가져옵니다.
    
    :param ha_url: Home Assistant 기본 URL
    :param ha_token: Home Assistant Access Token
    :return: Switch entity 목록
    """
    states_url = ha_url.rstrip("/") + "/api/states"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.get(states_url, headers=headers, timeout=10)
        if resp.status_code // 100 != 2:
            logging.error(
                "Entity 목록 조회 실패: %s %s",
                resp.status_code,
                resp.text,
            )
            return []

        all_states = resp.json()
        switch_entities = []

        for state in all_states:
            entity_id = state.get("entity_id", "")
            if entity_id.startswith("switch."):
                switch_entities.append({
                    "entity_id": entity_id,
                    "friendly_name": state.get("attributes", {}).get("friendly_name", ""),
                    "state": state.get("state", "unknown"),
                })

        logging.debug("Home Assistant에서 %d개의 switch entity를 찾았습니다.", len(switch_entities))
        return switch_entities
    except Exception as e:
        logging.error("Entity 목록 조회 중 예외 발생: %s", e, exc_info=True)
        return []


def _try_matter_commission(commission_code: str) -> bool:
    """
    Matter 커미션을 시도합니다.
    
    :param commission_code: Matter Commission Code
    :return: 커미션 성공 여부
    """
    try:
        import asyncio
        from pk_internal_tools.pk_functions.ensure_matter_device_controlled import (
            ensure_matter_device_controlled,
        )

        logging.info("Matter 커미션 시작...")

        # 비동기 함수를 동기적으로 실행
        success = asyncio.run(
            ensure_matter_device_controlled(
                device_identifier="1",  # P110M node_id
                action="status",  # 상태 확인으로 커미션만 수행
                commission_code=commission_code,
            )
        )

        if success:
            logging.info("Matter 커미션 성공")
        else:
            logging.warning("Matter 커미션 실패")

        return success

    except Exception as e:
        logging.error("Matter 커미션 중 예외 발생: %s", e, exc_info=True)
        return False


def _find_matter_entity_id(
        ha_url: str, ha_token: str, fallback_entity_id: Optional[str] = None
) -> Optional[str]:
    """
    Matter 통합으로 생성된 Entity ID를 찾습니다.
    
    :param ha_url: Home Assistant URL
    :param ha_token: Home Assistant Token
    :param fallback_entity_id: 찾지 못한 경우 반환할 기본 Entity ID
    :return: Entity ID 또는 None
    """
    try:
        # 모든 switch entity 목록 조회
        entities = _list_ha_switch_entities(ha_url, ha_token)

        # Matter로 시작하는 entity 찾기
        for entity in entities:
            entity_id = entity.get("entity_id", "")
            if "matter" in entity_id.lower():
                logging.info("Matter Entity 발견: %s", entity_id)
                return entity_id

        # Matter entity를 찾지 못한 경우 fallback 사용
        if fallback_entity_id:
            logging.info("Matter Entity를 찾지 못했습니다. 기본 Entity ID 사용: %s", fallback_entity_id)
            return fallback_entity_id

        return None

    except Exception as e:
        logging.error("Entity ID 찾기 중 예외 발생: %s", e, exc_info=True)
        return fallback_entity_id


def _call_ha_switch_service(
        ha_url: str, entity_id: str, action: str, ha_token: str
) -> bool:
    """
    Home Assistant switch 서비스를 호출하여 장치를 제어합니다.

    :param ha_url: Home Assistant 기본 URL
    :param entity_id: Entity ID
    :param action: 제어 액션 ("on" 또는 "off")
    :param ha_token: Home Assistant Access Token
    :return: 성공 여부
    """
    service_url = ha_url.rstrip("/") + f"/api/services/switch/turn_{action}"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    payload = {"entity_id": entity_id}

    logging.info(
        "Home Assistant 서비스 호출: %s %s (entity: %s)",
        action,
        service_url,
        entity_id,
    )

    try:
        resp = requests.post(service_url, headers=headers, json=payload, timeout=10)
        if resp.status_code // 100 == 2:
            logging.info(
                "Home Assistant 서비스 호출 성공: %s %s",
                action,
                entity_id,
            )
            return True
        else:
            logging.error(
                "Home Assistant 서비스 호출 실패: %s %s -> %s %s",
                action,
                entity_id,
                resp.status_code,
                resp.text,
            )
            return False
    except Exception as e:
        logging.error("Home Assistant 서비스 호출 중 예외 발생: %s", e, exc_info=True)
        return False
