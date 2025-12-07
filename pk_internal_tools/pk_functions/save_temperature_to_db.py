import sqlite3
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE
from pk_internal_tools.pk_functions.ensure_temperature_db_table_created import ensure_temperature_db_table_created


def save_temperature_to_db(
    temperature: float,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    city: Optional[str] = None,
    country_code: Optional[str] = None,
    db_path: Optional[Path] = None
) -> bool:
    """
    기온 데이터를 DB에 저장합니다.
    
    Args:
        temperature: 기온 (섭씨)
        latitude: 위도
        longitude: 경도
        city: 도시명
        country_code: 국가 코드
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        bool: 성공 시 True, 실패 시 False.
    """
    try:
        if db_path is None:
            db_path = F_pk_SQLITE
        
        # 테이블이 없으면 생성
        ensure_temperature_db_table_created(db_path)
        
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        # 기온 데이터 저장
        cur.execute("""
            INSERT INTO temperature_data 
            (temperature, latitude, longitude, city, country_code, collected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (temperature, latitude, longitude, city, country_code, datetime.now()))
        
        conn.commit()
        conn.close()
        
        logging.debug(f"기온 데이터 저장 완료: {temperature}°C")
        return True
        
    except Exception as e:
        logging.error(f"기온 데이터 저장 실패: {e}")
        return False

