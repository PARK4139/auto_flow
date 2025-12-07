import logging
import os
import sys
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("XavierAPI")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="PK Xavier Control API",
    description="API to control devices connected to the Xavier, such as Home Assistant entities. "
                "웹앱에서도 사용할 수 있는 REST/WebSocket API를 제공합니다.",
    version="2.0.0",
)

# --- CORS 설정 (웹앱에서 접근 가능하도록) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for API Data Validation ---
class SwitchControlRequest(BaseModel):
    action: str  # "on", "off", or "toggle"
    entity_id: Optional[str] = None  # None인 경우 기본 entity 사용


class TvControlRequest(BaseModel):
    action: str  # "on", "off", or "toggle"
    entity_id: Optional[str] = None  # None인 경우 기본 entity 사용


class EntityStateResponse(BaseModel):
    entity_id: str
    state: str
    friendly_name: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None


class EntityListResponse(BaseModel):
    entities: List[EntityStateResponse]

# --- Helper Functions ---
def _get_ha_config() -> tuple[Optional[str], Optional[str]]:
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

# --- API Endpoints ---
@app.post("/api/v1/plug/control")
async def control_plug(request: SwitchControlRequest):
    """
    스마트 플러그(P110M 등)를 Home Assistant를 통해 제어합니다.
    웹앱에서도 사용할 수 있습니다.
    
    - action: "on", "off", "toggle"
    - entity_id: 선택사항. None인 경우 환경변수 HA_ENTITY 또는 기본값 사용
    """
    ha_url, ha_token = _get_ha_config()
    
    if not all([ha_url, ha_token]):
        logger.error("HA_URL or HA_TOKEN environment variables are not set on the server.")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Home Assistant URL or Token is not configured."
        )
    
    # entity_id가 없으면 환경변수 또는 기본값 사용
    entity_id = request.entity_id or os.environ.get("HA_ENTITY", "switch.tapo_p110m_plug")
    
    logger.info(f"Received request to '{request.action}' entity '{entity_id}'")
    
    # toggle 액션의 경우 현재 상태를 먼저 조회
    if request.action == "toggle":
        state_data = _get_ha_entity_state(ha_url, entity_id, ha_token)
        if state_data:
            current_state = state_data.get("state", "unknown")
            next_action = "off" if current_state == "on" else "on"
            logger.info(f"현재 상태: {current_state} -> {next_action}로 전환")
            action_to_use = next_action
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Failed to get current state for entity '{entity_id}'."
            )
    else:
        action_to_use = request.action
    
    success = call_ha_switch(
        action=action_to_use,
        entity_id=entity_id,
        ha_url=ha_url,
        ha_token=ha_token
    )

    if success:
        return {
            "status": "success",
            "action": request.action,
            "executed_action": action_to_use,
            "entity_id": entity_id,
        }
    else:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to control entity '{entity_id}' via Home Assistant."
        )


@app.post("/api/v1/tv/control")
async def control_tv(request: TvControlRequest):
    """
    TV(media_player)를 Home Assistant를 통해 제어합니다.
    웹앱에서도 사용할 수 있습니다.
    
    - action: "on", "off", "toggle"
    - entity_id: 선택사항. None인 경우 환경변수 HA_TV_ENTITY 또는 기본값 사용
    """
    ha_url, ha_token = _get_ha_config()
    
    if not all([ha_url, ha_token]):
        logger.error("HA_URL or HA_TOKEN environment variables are not set on the server.")
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Home Assistant URL or Token is not configured."
        )
    
    # entity_id가 없으면 환경변수 또는 기본값 사용
    entity_id = request.entity_id or os.environ.get("HA_TV_ENTITY", "media_player.lg_tv")
    
    logger.info(f"Received request to '{request.action}' TV entity '{entity_id}'")
    
    # toggle 액션의 경우 현재 상태를 먼저 조회
    if request.action == "toggle":
        state_data = _get_ha_entity_state(ha_url, entity_id, ha_token)
        if state_data:
            current_state = state_data.get("state", "unknown")
            # For media_player, "on", "playing", "paused" means on
            if current_state in ("on", "playing", "paused"):
                next_action = "off"
            else:
                next_action = "on"
            logger.info(f"현재 상태: {current_state} -> {next_action}로 전환")
            action_to_use = next_action
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Failed to get current state for entity '{entity_id}'."
            )
    else:
        action_to_use = request.action
    
    success = call_ha_media_player(
        action=action_to_use,
        entity_id=entity_id,
        ha_url=ha_url,
        ha_token=ha_token
    )

    if success:
        return {
            "status": "success",
            "action": request.action,
            "executed_action": action_to_use,
            "entity_id": entity_id,
        }
    else:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to control TV entity '{entity_id}' via Home Assistant."
        )


# --- API Endpoints ---
@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "message": "PK Xavier Control API is running.",
        "version": "2.0.0",
        "endpoints": {
            "plug_control": "/api/v1/plug/control",
            "tv_control": "/api/v1/tv/control",
            "tv_entities": "/api/v1/tv/entities",
            "entities": "/api/v1/entities",
            "entity_state": "/api/v1/entity/{entity_id}/state",
        }
    }


@app.get("/api/v1/entities", response_model=EntityListResponse)
async def list_entities():
    """
    Home Assistant에서 모든 switch entity 목록을 조회합니다.
    웹앱에서 사용 가능한 장치 목록을 가져올 때 사용합니다.
    """
    ha_url, ha_token = _get_ha_config()
    
    if not all([ha_url, ha_token]):
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Home Assistant URL or Token is not configured."
        )
    
    entities = _list_ha_switch_entities(ha_url, ha_token)
    
    return EntityListResponse(
        entities=[
            EntityStateResponse(
                entity_id=e["entity_id"],
                state=e["state"],
                friendly_name=e.get("friendly_name"),
                attributes=e.get("attributes"),
            )
            for e in entities
        ]
    )


@app.get("/api/v1/tv/entities", response_model=EntityListResponse)
async def list_tv_entities():
    """
    Home Assistant에서 모든 media_player entity 목록을 조회합니다.
    웹앱에서 사용 가능한 TV 목록을 가져올 때 사용합니다.
    """
    ha_url, ha_token = _get_ha_config()
    
    if not all([ha_url, ha_token]):
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Home Assistant URL or Token is not configured."
        )
    
    entities = _list_ha_media_player_entities(ha_url, ha_token)
    
    return EntityListResponse(
        entities=[
            EntityStateResponse(
                entity_id=e["entity_id"],
                state=e["state"],
                friendly_name=e.get("friendly_name"),
                attributes=e.get("attributes"),
            )
            for e in entities
        ]
    )


@app.get("/api/v1/entity/{entity_id}/state", response_model=EntityStateResponse)
async def get_entity_state(entity_id: str):
    """
    특정 entity의 현재 상태를 조회합니다.
    """
    ha_url, ha_token = _get_ha_config()
    
    if not all([ha_url, ha_token]):
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: Home Assistant URL or Token is not configured."
        )
    
    state_data = _get_ha_entity_state(ha_url, entity_id, ha_token)
    
    if not state_data:
        raise HTTPException(
            status_code=404,
            detail=f"Entity '{entity_id}' not found or failed to retrieve state."
        )
    
    return EntityStateResponse(
        entity_id=state_data.get("entity_id", entity_id),
        state=state_data.get("state", "unknown"),
        friendly_name=state_data.get("attributes", {}).get("friendly_name"),
        attributes=state_data.get("attributes", {}),
    )

# --- Main execution block to run the server ---
if __name__ == "__main__":
    # Default to port 8000, but allow overriding with an environment variable
    port = int(os.environ.get("XAVIER_API_PORT", 8000))
    logger.info(f"Starting Uvicorn server on host 0.0.0.0 and port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
