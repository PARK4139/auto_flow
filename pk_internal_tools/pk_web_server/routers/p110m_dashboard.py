from fastapi import APIRouter, Depends, HTTPException, status
import logging
import traceback
from typing import Dict, Any

# Lazy import to avoid circular dependencies and improve startup time
from pk_internal_tools.pk_functions.ensure_pk_p110m_off import ensure_pk_p110m_off
from pk_internal_tools.pk_functions.ensure_pk_p110m_on import ensure_pk_p110m_on
from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_tapo_library import ensure_pk_p110m_controlled_via_tapo_library
from pk_internal_tools.pk_functions.get_p110m_energy_history_from_db import get_p110m_energy_history_from_db
from pk_internal_tools.pk_functions.ensure_pk_p110m_energy_db_table_created import ensure_pk_p110m_energy_db_table_created


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/p110m", tags=["p110m"])


@router.on_event("startup")
async def startup_event():
    """
    Startup event to ensure P110M energy database table is created.
    """
    logger.info("P110M dashboard router startup: Ensuring energy database table.")
    success = ensure_pk_p110m_energy_db_table_created()
    if success:
        logger.info("P110M energy database table is ready.")
    else:
        logger.error("Failed to ensure P110M energy database table. Check logs.")


@router.get("/status", response_model=Dict[str, Any])
async def get_p110m_status():
    """
    P110M 스마트 플러그의 현재 상태를 조회합니다.
    """
    logger.info("P110M 상태 조회 요청 받음.")
    try:
        # TODO: 실제 P110M 상태 조회 로직 구현 (예: Kasa/Tapo 라이브러리 직접 호출)
        # 현재는 더미 데이터 반환
        status_data = {
            "device_id": "P110M_DEVICE_01",
            "is_on": True,
            "current_power_mw": 15000,
            "voltage_mv": 220000,
            "current_a": 0.068,
            "total_consumption_wh": 12345.67,
            "last_updated": "2025-12-09T10:30:00Z"
        }
        logger.info(f"P110M 상태 반환: {status_data}")
        return status_data
    except Exception as e:
        logger.error(f"P110M 상태 조회 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="P110M 상태 조회 실패")


@router.post("/on", response_model=Dict[str, Any])
async def turn_on_p110m():
    """
    P110M 스마트 플러그를 웁니다.
    """
    logger.info("P110M 켜기 요청 받음.")
    try:
        success = ensure_pk_p110m_on()
        if success:
            logger.info("P110M 켜기 성공.")
            return {"status": "success", "message": "P110M 켜짐"}
        else:
            logger.warning("P110M 켜기 실패.")
            return {"status": "failed", "message": "P110M 켜기 실패"}
    except Exception as e:
        logger.error(f"P110M 켜기 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="P110M 켜기 실패")


@router.post("/off", response_model=Dict[str, Any])
async def turn_off_p110m():
    """
    P110M 스마트 플러그를 끕니다.
    """
    logger.info("P110M 끄기 요청 받음.")
    try:
        success = ensure_pk_p110m_off()
        if success:
            logger.info("P110M 끄기 성공.")
            return {"status": "success", "message": "P110M 꺼짐"}
        else:
            logger.warning("P110M 끄기 실패.")
            return {"status": "failed", "message": "P110M 끄기 실패"}
    except Exception as e:
        logger.error(f"P110M 끄기 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="P110M 끄기 실패")


@router.post("/toggle", response_model=Dict[str, Any])
async def toggle_p110m():
    """
    P110M 스마트 플러그의 상태를 토글합니다 (켜져 있으면 끄고, 꺼져 있으면 켭니다).
    """
    logger.info("P110M 토글 요청 받음.")
    try:
        # TODO: 실제 P110M 토글 로직 구현 (현재는 off/on 함수를 활용하는 예시)
        # 이 부분은 P110M 제어 라이브러리가 토글 기능을 제공하거나
        # 현재 상태를 조회하여 on/off를 결정하는 로직이 필요합니다.
        result = ensure_pk_p110m_controlled_via_tapo_library(action="toggle") # tapo 라이브러리가 toggle 지원 시
        if result and result.get("status") == "success":
            logger.info(f"P110M 토글 성공: {result.get('message')}")
            return {"status": "success", "message": f"P110M 상태 토글됨: {result.get('message')}"}
        else:
            logger.warning(f"P110M 토글 실패: {result.get('message') if result else 'Unknown error'}")
            return {"status": "failed", "message": f"P110M 토글 실패: {result.get('message') if result else 'Unknown error'}"}
    except Exception as e:
        logger.error(f"P110M 토글 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="P110M 토글 실패")


@router.get("/energy-history", response_model=Dict[str, Any])
async def get_p110m_energy_data(
    start_date: str = "2025-12-01",
    end_date: str = "2025-12-31"
):
    """
    P110M 스마트 플러그의 에너지 사용량 기록을 조회합니다.
    """
    logger.info(f"P110M 에너지 사용량 기록 조회 요청 받음: {start_date} ~ {end_date}")
    try:
        history = get_p110m_energy_history_from_db(start_date=start_date, end_date=end_date)
        logger.info(f"P110M 에너지 기록 {len(history)}개 반환.")
        return {"status": "success", "data": history}
    except Exception as e:
        logger.error(f"P110M 에너지 기록 조회 중 오류 발생: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="P110M 에너지 기록 조회 실패")
