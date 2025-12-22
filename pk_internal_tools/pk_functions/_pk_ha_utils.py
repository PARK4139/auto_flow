import logging
import os
from typing import List, Optional, Dict, Any, Tuple
import requests
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# --- Helper Functions ---
def _get_ha_config() -> Tuple[Optional[str], Optional[str]]:
    """환경변수에서 HA 설정을 가져옵니다."""
    ha_url = os.environ.get("HA_URL")
    ha_token = os.environ.get("HA_TOKEN")
    return ha_url, ha_token


def _list_ha_switch_entities(ha_url: str, ha_token: str) -> List[Dict[str, Any]]:
    """Home Assistant에서 모든 switch entity 목록을 가져옵니다."""
    states_url = ha_url.rstrip("/") + "/api/states"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.get(states_url, headers=headers, timeout=10)
        if resp.status_code // 100 != 2:
            logger.error("Entity 목록 조회 실패: %s %s", resp.status_code, resp.text)
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
                    "attributes": state.get("attributes", {}),
                })
        
        return switch_entities
    except Exception as e:
        logger.error("Entity 목록 조회 중 예외 발생: %s", e, exc_info=True)
        return []


def _list_ha_media_player_entities(ha_url: str, ha_token: str) -> List[Dict[str, Any]]:
    """Home Assistant에서 모든 media_player entity 목록을 가져옵니다."""
    states_url = ha_url.rstrip("/") + "/api/states"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.get(states_url, headers=headers, timeout=10)
        if resp.status_code // 100 != 2:
            logger.error("Entity 목록 조회 실패: %s %s", resp.status_code, resp.text)
            return []
        
        all_states = resp.json()
        media_player_entities = []
        
        for state in all_states:
            entity_id = state.get("entity_id", "")
            if entity_id.startswith("media_player."):
                media_player_entities.append({
                    "entity_id": entity_id,
                    "friendly_name": state.get("attributes", {}).get("friendly_name", ""),
                    "state": state.get("state", "unknown"),
                    "attributes": state.get("attributes", {}),
                })
        
        return media_player_entities
    except Exception as e:
        logger.error("Entity 목록 조회 중 예외 발생: %s", e, exc_info=True)
        return []


def _get_ha_entity_state(ha_url: str, entity_id: str, ha_token: str) -> Optional[Dict[str, Any]]:
    """Home Assistant에서 entity의 현재 상태를 조회합니다."""
    state_url = ha_url.rstrip("/") + f"/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.get(state_url, headers=headers, timeout=10)
        if resp.status_code // 100 == 2:
            return resp.json()
        else:
            logger.error("상태 조회 실패: %s %s", resp.status_code, resp.text)
            return None
    except Exception as e:
        logger.error("상태 조회 중 예외 발생: %s", e, exc_info=True)
        return None


# --- Home Assistant Control Logic ---
def call_ha_switch(action: str, entity_id: str, ha_url: str, ha_token: str) -> bool:
    """
    Calls the Home Assistant 'switch' service to control a device.
    """
    service_domain = "switch"
    service_name = f"turn_{action}"
    url = f"{ha_url.rstrip('/')}/api/services/{service_domain}/{service_name}"
    
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    
    payload = {"entity_id": entity_id}

    logger.info(f"Calling HA Service: POST {url} with payload: {payload}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if 200 <= response.status_code < 300:
            logger.info(f"HA service call successful for entity '{entity_id}'. Status: {response.status_code}")
            return True
        else:
            logger.error(f"HA service call failed for entity '{entity_id}'. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to Home Assistant failed: {e}")
        return False


def call_ha_media_player(action: str, entity_id: str, ha_url: str, ha_token: str) -> bool:
    """
    Calls the Home Assistant 'media_player' service to control a TV or media device.
    Supports "on", "off", and "toggle" actions.
    For "off" action, if media_player.turn_off fails, tries remote.send_command as fallback.
    """
    if action not in ("on", "off", "toggle"):
        logger.error(f"Unsupported action: {action}")
        return False

    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }

    # Handle toggle by reading current state first
    if action == "toggle":
        state_url = ha_url.rstrip("/") + f"/api/states/{entity_id}"
        try:
            resp = requests.get(state_url, headers=headers, timeout=5)
        except Exception as e:
            logger.error(f"Exception while getting current state: {e}")
            return False

        if resp.status_code // 100 != 2:
            logger.error(f"Failed to get current state: {resp.status_code} {resp.text}")
            return False

        cur_state = resp.json().get("state")
        # For media_player, "on" means on, "off" or "standby" means off
        if cur_state in ("on", "playing", "paused"):
            next_action = "off"
        else:
            next_action = "on"
        logger.info(f"Current state: {cur_state} -> switching to {next_action}")
        action = next_action

    # Call media_player service
    if action == "on":
        service_name = "turn_on"
        service_domain = "media_player"
    elif action == "off":
        service_name = "turn_off"
        service_domain = "media_player"
    else:
        logger.error(f"Unsupported action: {action}")
        return False

    service_url = ha_url.rstrip("/") + f"/api/services/{service_domain}/{service_name}"

    try:
        resp = requests.post(
            service_url,
            headers=headers,
            json={"entity_id": entity_id},
            timeout=10,  # TV control may take longer
        )
    except Exception as e:
        logger.error(f"Exception while calling Home Assistant service: {e}")
        return False

    if resp.status_code // 100 == 2:
        logger.info(f"Home Assistant service call successful: {action} {entity_id}")
        return True

    # OFF 액션 실패 시 remote.send_command로 재시도 (LG TV용)
    if action == "off" and service_domain == "media_player":
        logger.warning("media_player.turn_off 실패, remote.send_command로 재시도합니다.")
        # remote 엔티티 찾기 (media_player.lg_tv -> remote.lg_tv)
        remote_entity_id = entity_id.replace("media_player.", "remote.")
        remote_service_url = ha_url.rstrip("/") + "/api/services/remote/send_command"
        
        try:
            # LG TV 전원 끄기 명령 (일반적인 IR 코드)
            remote_resp = requests.post(
                remote_service_url,
                headers=headers,
                json={
                    "entity_id": remote_entity_id,
                    "command": "KEY_POWER"
                },
                timeout=10,
            )
            if remote_resp.status_code // 100 == 2:
                logger.info(f"remote.send_command로 TV OFF 성공: {remote_entity_id}")
                return True
            else:
                logger.warning(f"remote.send_command도 실패: {remote_resp.status_code} {remote_resp.text}")
        except Exception as e:
            logger.warning(f"remote.send_command 시도 중 예외: {e}")

    logger.error(
        f"Home Assistant service call failed: {action} {entity_id} -> {resp.status_code} {resp.text}"
    )
    return False
