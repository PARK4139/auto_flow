import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# HA 헬퍼 함수 임포트
from pk_internal_tools.pk_functions._pk_ha_utils import (
    _get_ha_config, _list_ha_switch_entities, _list_ha_media_player_entities,
    _get_ha_entity_state, call_ha_switch, call_ha_media_player
)
# P110M 헬퍼 함수 임포트
from pk_internal_tools.pk_functions._pk_p110m_utils import (
    get_p110m_energy_history_from_db, get_p110m_energy_aggregated_for_graph
)
# Pydantic 모델 임포트
from pk_internal_tools.pk_objects._pk_api_models import (
    SwitchControlRequest, TvControlRequest, EntityStateResponse, EntityListResponse
)
from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT  # D_PK_ROOT 사용을 위해 임포트
# 대시보드 HTML 임포트
from pk_internal_tools.pk_web_server.routers.dashboard import get_dashboard_html

# --- Logging Configuration ---
# uvicorn에 의해 직접 실행되므로 basicConfig 대신 getLogger 사용
logger = logging.getLogger("UnifiedWebServer")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="PK Unified Web Server API",
    description="Unified API to control devices (Home Assistant, P110M) and provide dashboards.",
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

# --- DB 경로 설정 ---
# 로컬 또는 원격(Xavier)에서 DB 경로 설정
db_dir = Path(D_PK_ROOT) / ".pk_system"

db_dir.mkdir(parents=True, exist_ok=True)
db_path = db_dir / "pk_system.sqlite"


# os.environ["PK_SQLITE_PATH"] = str(db_path) # _pk_p110m_utils에서 인자로 받으므로 불필요


# --- API Endpoints ---
@app.post("/api/v1/plug/control")
async def control_plug_api(request: SwitchControlRequest):
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
async def control_tv_api(request: TvControlRequest):
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


@app.get("/api/v1/entities", response_model=EntityListResponse)
async def list_ha_entities_api():
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
async def list_tv_entities_api():
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
async def get_entity_state_api(entity_id: str):
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


@app.get("/api/p110m/energy/history")
async def get_p110m_energy_history_api(device_host: Optional[str] = None, days: int = 365, limit: Optional[int] = None):
    """P110M 에너지 히스토리 조회"""
    try:
        history = get_p110m_energy_history_from_db(db_path=db_path, device_host=device_host, days=days, limit=limit)
        result = [
            {
                "device_host": item["device_host"],
                "current_power": item["current_power"],
                "today_energy": item["today_energy"],
                "month_energy": item["month_energy"],
                "collected_at": item["collected_at"].isoformat() if isinstance(item["collected_at"], datetime) else str(item.get("collected_at", "")),
                "local_time": item["local_time"].isoformat() if isinstance(item.get("local_time"), datetime) else str(item.get("local_time", ""))
            }
            for item in history
        ]
        return JSONResponse(content=result)
    except Exception as e:
        logger.error("P110M 에너지 히스토리 조회 실패: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/p110m/energy/aggregated")
async def get_p110m_energy_aggregated_api(device_host: Optional[str] = None, period: str = "year"):
    """P110M 에너지 데이터 집계"""
    try:
        aggregated = get_p110m_energy_aggregated_for_graph(db_path=db_path, device_host=device_host, period=period)
        return JSONResponse(content=aggregated)
    except Exception as e:
        logger.error("P110M 에너지 집계 조회 실패: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/p110m/control")
async def control_p110m_api(action: str, device_host: Optional[str] = None):
    """P110M 제어 (on, off, toggle, info, energy)"""
    try:
        # TODO: remote_target에서 직접 P110M 제어 구현 - HA 연동을 고려할 것
        # 현재는 기본 응답만 반환
        result = {"status": "success", "action": action, "message": f"P110M {action} 명령 실행됨 (HA 연동 필요)"}
        return JSONResponse(content=result)
    except Exception as e:
        logger.error("P110M 제어 실패: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """API 상태 확인 및 대시보드 홈"""
    return HTMLResponse(content=get_dashboard_html())