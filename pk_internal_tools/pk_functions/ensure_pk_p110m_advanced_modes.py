#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P110M 고급 제어 모드: 시퀀스 제어, 에너지 절감 모드 등

이 모듈은 P110M의 고급 제어 기능을 제공합니다:
- 시퀀스 제어: 시간대별 자동 켜기/끄기
- 에너지 절감 모드: 사용량 모니터링 및 자동 제어
- 스케줄 기반 제어: 특정 시간에 자동 실행
"""
import logging
import time
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass

from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_ha_api import (
    ensure_pk_p110m_controlled_via_ha_api,
    get_ha_entity_state,
)
import requests
from pk_internal_tools.pk_functions.ensure_seconds_measured import (
    ensure_seconds_measured,
)

logger = logging.getLogger(__name__)


@dataclass
class SequenceStep:
    """시퀀스 단계 정의"""
    time_offset: int  # 시작 시간으로부터의 오프셋 (초)
    action: str  # "on" 또는 "off"
    description: Optional[str] = None


@dataclass
class EnergySavingConfig:
    """에너지 절감 모드 설정"""
    idle_timeout_seconds: int = 3600  # 사용 안 함 시간 (초) - 기본 1시간
    auto_off_enabled: bool = True  # 자동 끄기 활성화
    power_threshold_watts: Optional[float] = None  # 전력 임계값 (와트)
    check_interval_seconds: int = 300  # 체크 간격 (초) - 기본 5분


@ensure_seconds_measured
def ensure_pk_p110m_sequence_control(
    sequence: List[SequenceStep],
    *,
    entity_id: Optional[str] = None,
    ha_url: Optional[str] = None,
    ha_token: Optional[str] = None,
    start_delay_seconds: int = 0,
) -> bool:
    """
    P110M을 시퀀스에 따라 제어합니다.
    
    예시:
        sequence = [
            SequenceStep(0, "on", "켜기"),
            SequenceStep(60, "off", "1분 후 끄기"),
            SequenceStep(120, "on", "2분 후 다시 켜기"),
        ]
        ensure_pk_p110m_sequence_control(sequence)
    
    :param sequence: 시퀀스 단계 목록 (시간 순서대로 정렬되어야 함)
    :param entity_id: Entity ID
    :param ha_url: Home Assistant URL
    :param ha_token: Home Assistant Token
    :param start_delay_seconds: 시작 전 대기 시간 (초)
    :return: 성공 여부
    """
    if not sequence:
        logger.error("시퀀스가 비어있습니다.")
        return False
    
    # 시퀀스를 시간 순서대로 정렬
    sorted_sequence = sorted(sequence, key=lambda x: x.time_offset)
    
    logger.info("P110M 시퀀스 제어 시작: %d 단계", len(sorted_sequence))
    
    if start_delay_seconds > 0:
        logger.info("시작 전 %d초 대기...", start_delay_seconds)
        time.sleep(start_delay_seconds)
    
    start_time = time.time()
    
    try:
        for i, step in enumerate(sorted_sequence):
            # 이전 단계로부터의 경과 시간 계산
            if i == 0:
                wait_time = step.time_offset
            else:
                wait_time = step.time_offset - sorted_sequence[i-1].time_offset
            
            if wait_time > 0:
                logger.info("다음 단계까지 %d초 대기...", wait_time)
                time.sleep(wait_time)
            
            # 액션 실행
            description = step.description or f"단계 {i+1}"
            logger.info("시퀀스 실행: %s (%s)", description, step.action)
            
            success = ensure_pk_p110m_controlled_via_ha_api(
                action=step.action,
                entity_id=entity_id,
                ha_url=ha_url,
                ha_token=ha_token,
            )
            
            if not success:
                logger.error("시퀀스 단계 실패: %s", description)
                return False
        
        elapsed = time.time() - start_time
        logger.info("시퀀스 제어 완료 (총 소요 시간: %.1f초)", elapsed)
        return True
        
    except KeyboardInterrupt:
        logger.warning("시퀀스 제어가 사용자에 의해 중단되었습니다.")
        return False
    except Exception as e:
        logger.error("시퀀스 제어 중 오류 발생: %s", e, exc_info=True)
        return False


@ensure_seconds_measured
def ensure_pk_p110m_energy_saving_mode(
    config: EnergySavingConfig,
    *,
    entity_id: Optional[str] = None,
    ha_url: Optional[str] = None,
    ha_token: Optional[str] = None,
    duration_seconds: Optional[int] = None,
    callback: Optional[Callable[[str, Dict[str, Any]], None]] = None,
) -> bool:
    """
    P110M 에너지 절감 모드를 활성화합니다.
    
    이 모드는 다음을 수행합니다:
    1. 주기적으로 장치 상태를 확인
    2. 일정 시간 동안 사용되지 않으면 자동으로 끄기
    3. 전력 소비량 모니터링 (지원되는 경우)
    
    :param config: 에너지 절감 설정
    :param entity_id: Entity ID
    :param ha_url: Home Assistant URL
    :param ha_token: Home Assistant Token
    :param duration_seconds: 모니터링 지속 시간 (None이면 무한)
    :param callback: 상태 변경 시 호출할 콜백 함수 (state, data)
    :return: 성공 여부
    """
    logger.info("P110M 에너지 절감 모드 시작")
    logger.info("설정: idle_timeout=%ds, auto_off=%s, check_interval=%ds",
                config.idle_timeout_seconds, config.auto_off_enabled, config.check_interval_seconds)
    
    start_time = time.time()
    last_activity_time = time.time()
    last_state = None
    
    try:
        while True:
            # 지속 시간 체크
            if duration_seconds and (time.time() - start_time) >= duration_seconds:
                logger.info("에너지 절감 모드 종료 (지속 시간 도달)")
                break
            
            # 현재 상태 확인
            current_state = get_ha_entity_state(
                entity_id=entity_id,
                ha_url=ha_url,
                ha_token=ha_token,
            )
            
            if current_state is None:
                logger.warning("상태를 조회할 수 없습니다. 재시도합니다...")
                time.sleep(config.check_interval_seconds)
                continue
            
            # 상태 변경 감지
            if current_state != last_state:
                logger.info("상태 변경: %s -> %s", last_state, current_state)
                last_state = current_state
                
                if current_state == "on":
                    last_activity_time = time.time()
                    logger.info("장치가 켜졌습니다. 활동 시간 갱신.")
                
                # 콜백 호출
                if callback:
                    try:
                        callback(current_state, {
                            "entity_id": entity_id,
                            "timestamp": datetime.now().isoformat(),
                        })
                    except Exception as e:
                        logger.error("콜백 실행 중 오류: %s", e)
            
            # 에너지 절감 로직
            if config.auto_off_enabled and current_state == "on":
                idle_time = time.time() - last_activity_time
                
                if idle_time >= config.idle_timeout_seconds:
                    logger.info("장치가 %d초 동안 사용되지 않았습니다. 자동으로 끕니다.", idle_time)
                    
                    success = ensure_pk_p110m_controlled_via_ha_api(
                        action="off",
                        entity_id=entity_id,
                        ha_url=ha_url,
                        ha_token=ha_token,
                    )
                    
                    if success:
                        logger.info("에너지 절감: 장치를 끄는 데 성공했습니다.")
                        last_state = "off"
                    else:
                        logger.error("에너지 절감: 장치를 끄는 데 실패했습니다.")
            
            # 전력 임계값 체크 (Matter 1.3 지원)
            if config.power_threshold_watts is not None and current_state == "on":
                energy_data = get_p110m_energy_data(
                    entity_id=entity_id,
                    ha_url=ha_url,
                    ha_token=ha_token,
                )
                
                if energy_data and energy_data.get("power_watts") is not None:
                    current_power = energy_data["power_watts"]
                    
                    if current_power > config.power_threshold_watts:
                        logger.warning(
                            "전력 임계값 초과: 현재 %sW > 임계값 %sW",
                            current_power,
                            config.power_threshold_watts,
                        )
                        
                        # 콜백 호출
                        if callback:
                            try:
                                callback("power_threshold_exceeded", {
                                    "entity_id": entity_id,
                                    "current_power": current_power,
                                    "threshold": config.power_threshold_watts,
                                    "timestamp": datetime.now().isoformat(),
                                })
                            except Exception as e:
                                logger.error("콜백 실행 중 오류: %s", e)
                        
                        # 필요시 자동 끄기 (설정에 따라)
                        # ensure_pk_p110m_controlled_via_ha_api(action="off", ...)
            
            # 다음 체크까지 대기
            time.sleep(config.check_interval_seconds)
            
    except KeyboardInterrupt:
        logger.info("에너지 절감 모드가 사용자에 의해 중단되었습니다.")
        return True
    except Exception as e:
        logger.error("에너지 절감 모드 중 오류 발생: %s", e, exc_info=True)
        return False


@ensure_seconds_measured
def ensure_pk_p110m_scheduled_control(
    schedule: List[Dict[str, Any]],
    *,
    entity_id: Optional[str] = None,
    ha_url: Optional[str] = None,
    ha_token: Optional[str] = None,
) -> bool:
    """
    P110M을 스케줄에 따라 제어합니다.
    
    예시:
        schedule = [
            {"time": "08:00", "action": "on", "description": "아침 켜기"},
            {"time": "22:00", "action": "off", "description": "밤 끄기"},
        ]
        ensure_pk_p110m_scheduled_control(schedule)
    
    :param schedule: 스케줄 목록 (각 항목은 "time" (HH:MM), "action", "description" 포함)
    :param entity_id: Entity ID
    :param ha_url: Home Assistant URL
    :param ha_token: Home Assistant Token
    :return: 성공 여부
    """
    logger.info("P110M 스케줄 제어 시작: %d 개 항목", len(schedule))
    
    # 스케줄을 시간 순서대로 정렬
    def parse_time(time_str: str) -> datetime:
        hour, minute = map(int, time_str.split(":"))
        now = datetime.now()
        scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if scheduled_time < now:
            scheduled_time += timedelta(days=1)
        return scheduled_time
    
    sorted_schedule = sorted(schedule, key=lambda x: parse_time(x["time"]))
    
    for item in sorted_schedule:
        scheduled_time = parse_time(item["time"])
        wait_seconds = (scheduled_time - datetime.now()).total_seconds()
        
        if wait_seconds > 0:
            logger.info("다음 스케줄까지 대기: %s (%s) - %d초 후",
                       item.get("description", item["time"]), item["action"], int(wait_seconds))
            time.sleep(wait_seconds)
        
        logger.info("스케줄 실행: %s (%s)", item.get("description", item["time"]), item["action"])
        
        success = ensure_pk_p110m_controlled_via_ha_api(
            action=item["action"],
            entity_id=entity_id,
            ha_url=ha_url,
            ha_token=ha_token,
        )
        
        if not success:
            logger.error("스케줄 실행 실패: %s", item.get("description", item["time"]))
            return False
    
    logger.info("스케줄 제어 완료")
    return True


@ensure_seconds_measured
def get_p110m_energy_data(
    entity_id: Optional[str] = None,
    ha_url: Optional[str] = None,
    ha_token: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    P110M의 에너지 데이터를 조회합니다 (Matter 1.3 지원).
    
    Matter 1.3 펌웨어(1.3.2 Build 250526 Rel.171305 이상)에서 에너지 모니터링을 지원합니다.
    Home Assistant에서 전력 센서를 자동으로 찾아 데이터를 반환합니다.
    
    참고: https://community.tp-link.com/en/smart-home/forum/topic/835354
    
    :param entity_id: Switch entity ID (전력 센서는 자동으로 찾음)
    :param ha_url: Home Assistant URL
    :param ha_token: Home Assistant Token
    :return: 에너지 데이터 딕셔너리 또는 None
        형식: {
            "power_watts": float,  # 실시간 전력 (W)
            "energy_kwh": float,   # 누적 에너지 (kWh)
            "timestamp": str,       # ISO 형식 타임스탬프
            "power_entity_id": str,  # 전력 센서 Entity ID
            "energy_entity_id": str, # 에너지 센서 Entity ID
        }
    """
    import requests
    from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_ha_api import (
        get_ha_entity_state,
    )
    from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
        ensure_env_var_completed_2025_11_24,
    )
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    
    # 환경변수에서 설정값 가져오기
    if not ha_url:
        func_n = get_caller_name()
        try:
            ha_ip = ensure_env_var_completed_2025_11_24(
                key_name="HA_IP",
                func_n=func_n,
                guide_text="Home Assistant IP 주소를 입력하세요 (예: 119.207.161.56):",
            )
            default_url = f"http://{ha_ip}:8123" if ha_ip else "http://localhost:8123"
        except Exception:
            default_url = "http://localhost:8123"
        
        ha_url = ensure_env_var_completed_2025_11_24(
            key_name="HA_URL",
            func_n="get_p110m_energy_data",
            guide_text=f"Home Assistant 기본 URL을 입력하세요 (예: {default_url}):",
            default_value=default_url,
        )
    
    if not ha_token:
        import getpass
        from pk_internal_tools.pk_functions.get_env_var_name_id import get_env_var_id
        from pk_internal_tools.pk_functions.ensure_pk_env_file_setup import (
            ensure_pk_env_file_setup,
        )
        from dotenv import get_key
        
        env_path = ensure_pk_env_file_setup()
        env_var_id = get_env_var_id("HA_TOKEN", "get_p110m_energy_data")
        
        try:
            ha_token = get_key(env_path, env_var_id)
        except Exception:
            ha_token = None
        
        if not ha_token:
            ha_token = getpass.getpass("Home Assistant Long-Lived Access Token을 입력하세요: ")
    
    if not ha_token:
        logger.error("HA_TOKEN이 설정되어 있지 않습니다.")
        return None
    
    # entity_id가 없으면 기본값 사용
    if not entity_id:
        entity_id = ensure_env_var_completed_2025_11_24(
            key_name="HA_ENTITY",
            func_n="get_p110m_energy_data",
            guide_text="P110M Entity ID를 입력하세요 (예: switch.tapo_p110m_plug):",
            default_value="switch.tapo_p110m_plug",
        )
    
    # 전력 센서 Entity ID 찾기
    # Matter 1.3의 경우: sensor.matter_xxxxx_power 또는 sensor.tapo_p110m_plug_power
    # TP-Link 통합의 경우: sensor.tapo_p110m_plug_power
    power_entity_candidates = [
        f"sensor.{entity_id.replace('switch.', '')}_power",  # switch.tapo_p110m_plug -> sensor.tapo_p110m_plug_power
        f"sensor.matter_{entity_id.split('.')[-1]}_power",  # Matter 통합
        f"sensor.{entity_id.replace('switch.', '')}_current_power",  # 대체 이름
    ]
    
    energy_entity_candidates = [
        f"sensor.{entity_id.replace('switch.', '')}_energy",  # switch.tapo_p110m_plug -> sensor.tapo_p110m_plug_energy
        f"sensor.matter_{entity_id.split('.')[-1]}_energy",  # Matter 통합
        f"sensor.{entity_id.replace('switch.', '')}_total_energy",  # 대체 이름
    ]
    
    # 모든 센서 목록 조회하여 매칭
    states_url = ha_url.rstrip("/") + "/api/states"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json",
    }
    
    try:
        resp = requests.get(states_url, headers=headers, timeout=10)
        if resp.status_code // 100 != 2:
            logger.error("센서 목록 조회 실패: %s %s", resp.status_code, resp.text)
            return None
        
        all_states = resp.json()
        
        # 전력 센서 찾기
        power_entity_id = None
        for candidate in power_entity_candidates:
            for state in all_states:
                if state.get("entity_id") == candidate:
                    power_entity_id = candidate
                    break
            if power_entity_id:
                break
        
        # 에너지 센서 찾기
        energy_entity_id = None
        for candidate in energy_entity_candidates:
            for state in all_states:
                if state.get("entity_id") == candidate:
                    energy_entity_id = candidate
                    break
            if energy_entity_id:
                break
        
        if not power_entity_id and not energy_entity_id:
            logger.warning(
                "에너지 센서를 찾을 수 없습니다. Matter 1.3 펌웨어(1.3.2 이상)가 설치되어 있는지 확인하세요."
            )
            logger.debug("시도한 전력 센서: %s", power_entity_candidates)
            logger.debug("시도한 에너지 센서: %s", energy_entity_candidates)
            return None
        
        # 전력 데이터 조회
        power_watts = None
        if power_entity_id:
            power_state_url = ha_url.rstrip("/") + f"/api/states/{power_entity_id}"
            try:
                power_resp = requests.get(power_state_url, headers=headers, timeout=10)
                if power_resp.status_code // 100 == 2:
                    power_data = power_resp.json()
                    power_state = power_data.get("state", "unknown")
                    if power_state != "unknown" and power_state != "unavailable":
                        try:
                            power_watts = float(power_state)
                        except (ValueError, TypeError):
                            logger.warning("전력 값을 파싱할 수 없습니다: %s", power_state)
            except Exception as e:
                logger.warning("전력 데이터 조회 중 오류: %s", e)
        
        # 에너지 데이터 조회
        energy_kwh = None
        if energy_entity_id:
            energy_state_url = ha_url.rstrip("/") + f"/api/states/{energy_entity_id}"
            try:
                energy_resp = requests.get(energy_state_url, headers=headers, timeout=10)
                if energy_resp.status_code // 100 == 2:
                    energy_data = energy_resp.json()
                    energy_state = energy_data.get("state", "unknown")
                    if energy_state != "unknown" and energy_state != "unavailable":
                        try:
                            energy_kwh = float(energy_state)
                        except (ValueError, TypeError):
                            logger.warning("에너지 값을 파싱할 수 없습니다: %s", energy_state)
            except Exception as e:
                logger.warning("에너지 데이터 조회 중 오류: %s", e)
        
        if power_watts is None and energy_kwh is None:
            logger.warning("에너지 데이터를 조회할 수 없습니다.")
            return None
        
        result = {
            "power_watts": power_watts,
            "energy_kwh": energy_kwh,
            "timestamp": datetime.now().isoformat(),
            "power_entity_id": power_entity_id,
            "energy_entity_id": energy_entity_id,
        }
        
        logger.info(
            "에너지 데이터 조회 성공: 전력=%sW, 누적=%skWh",
            power_watts if power_watts is not None else "N/A",
            energy_kwh if energy_kwh is not None else "N/A",
        )
        
        return result
        
    except Exception as e:
        logger.error("에너지 데이터 조회 중 예외 발생: %s", e, exc_info=True)
        return None


# 사용 예시 함수들
def example_sequence_control():
    """시퀀스 제어 예시"""
    sequence = [
        SequenceStep(0, "on", "켜기"),
        SequenceStep(60, "off", "1분 후 끄기"),
        SequenceStep(120, "on", "2분 후 다시 켜기"),
        SequenceStep(180, "off", "3분 후 끄기"),
    ]
    ensure_pk_p110m_sequence_control(sequence)


def example_energy_saving_mode():
    """에너지 절감 모드 예시"""
    config = EnergySavingConfig(
        idle_timeout_seconds=1800,  # 30분
        auto_off_enabled=True,
        check_interval_seconds=300,  # 5분마다 체크
    )
    ensure_pk_p110m_energy_saving_mode(config, duration_seconds=3600)  # 1시간 동안 모니터링


def example_scheduled_control():
    """스케줄 제어 예시"""
    schedule = [
        {"time": "08:00", "action": "on", "description": "아침 켜기"},
        {"time": "12:00", "action": "off", "description": "점심 끄기"},
        {"time": "18:00", "action": "on", "description": "저녁 켜기"},
        {"time": "22:00", "action": "off", "description": "밤 끄기"},
    ]
    ensure_pk_p110m_scheduled_control(schedule)

