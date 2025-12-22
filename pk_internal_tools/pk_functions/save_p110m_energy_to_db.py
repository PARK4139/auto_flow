import sqlite3
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE
from pk_internal_tools.pk_functions.ensure_pk_p110m_energy_db_table_created import ensure_pk_p110m_energy_db_table_created


def save_p110m_energy_to_db(
    device_host: str,
    energy_data: Dict[str, Any],
    db_path: Optional[Path] = None
) -> bool:
    """
    P110M 에너지 데이터를 DB에 저장합니다.
    
    Args:
        device_host: P110M 장치의 IP 주소 또는 호스트명
        energy_data: 에너지 데이터 딕셔너리. 다음 키를 포함할 수 있음:
            - current_power: 현재 소비 전력 (W)
            - today_energy: 오늘 사용 에너지 (Wh)
            - today_runtime: 오늘 가동 시간 (초)
            - month_energy: 이번 달 사용 에너지 (Wh)
            - month_runtime: 이번 달 가동 시간 (초)
            - local_time: 조회 시간 (datetime 또는 ISO 문자열)
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        bool: 성공 시 True, 실패 시 False.
    """
    try:
        if db_path is None:
            # 환경 변수에서 DB 경로 확인 (Xavier에서 실행 시)
            env_db_path = os.environ.get("pk_SQLITE_PATH")
            if env_db_path:
                db_path = Path(env_db_path)
            else:
                db_path = F_pk_SQLITE
        
        # 테이블이 없으면 생성
        ensure_pk_p110m_energy_db_table_created(db_path)
        
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        # local_time 처리 (datetime 객체 또는 ISO 문자열)
        local_time = energy_data.get("local_time")
        if local_time is not None:
            if isinstance(local_time, datetime):
                local_time_str = local_time.isoformat()
            elif isinstance(local_time, str):
                local_time_str = local_time
            else:
                local_time_str = str(local_time)
        else:
            local_time_str = None
        
        # 에너지 데이터 저장
        cur.execute("""
            INSERT INTO p110m_energy_data 
            (device_host, current_power, today_energy, today_runtime, 
             month_energy, month_runtime, local_time, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            device_host,
            energy_data.get("current_power"),
            energy_data.get("today_energy"),
            energy_data.get("today_runtime"),
            energy_data.get("month_energy"),
            energy_data.get("month_runtime"),
            local_time_str,
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
        logging.debug(f"P110M 에너지 데이터 저장 완료: {device_host} (전력: {energy_data.get('current_power', 'N/A')}W)")
        return True
        
    except Exception as e:
        logging.error(f"P110M 에너지 데이터 저장 실패: {e}", exc_info=True)
        return False

