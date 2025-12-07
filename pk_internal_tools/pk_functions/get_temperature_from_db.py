import sqlite3
import logging
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime, timedelta

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE


def get_temperature_from_db(
    max_age_minutes: int = 5,
    db_path: Optional[Path] = None
) -> Optional[Tuple[float, datetime]]:
    """
    DB에서 최근 기온 데이터를 조회합니다.
    
    Args:
        max_age_minutes: 최대 허용 데이터 나이 (분). 기본값 5분.
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        Optional[Tuple[float, datetime]]: (기온, 수집시간) 튜플 또는 None.
    """
    try:
        if db_path is None:
            db_path = F_pk_SQLITE
        
        if not db_path.exists():
            logging.debug(f"DB 파일이 존재하지 않습니다: {db_path}")
            return None
        
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 최근 max_age_minutes 이내의 데이터 조회
        cutoff_time = datetime.now() - timedelta(minutes=max_age_minutes)
        
        cur.execute("""
            SELECT temperature, collected_at 
            FROM temperature_data 
            WHERE collected_at >= ?
            ORDER BY collected_at DESC
            LIMIT 1
        """, (cutoff_time,))
        
        row = cur.fetchone()
        conn.close()
        
        if row is None:
            logging.debug(f"최근 {max_age_minutes}분 이내의 기온 데이터가 없습니다.")
            return None
        
        # collected_at을 datetime 객체로 변환
        collected_at_str = row['collected_at']
        if isinstance(collected_at_str, str):
            try:
                # ISO 형식 파싱 시도
                if 'T' in collected_at_str:
                    collected_at = datetime.fromisoformat(collected_at_str)
                else:
                    # 공백으로 구분된 형식 처리
                    collected_at = datetime.fromisoformat(collected_at_str.replace(' ', 'T', 1))
            except ValueError:
                # 파싱 실패 시 현재 시간 사용
                logging.warning(f"날짜 파싱 실패, 현재 시간 사용: {collected_at_str}")
                collected_at = datetime.now()
        elif isinstance(collected_at_str, (int, float)):
            collected_at = datetime.fromtimestamp(collected_at_str)
        else:
            collected_at = datetime.now()
        
        temperature = float(row['temperature'])
        
        logging.debug(f"DB에서 기온 조회 성공: {temperature}°C (수집시간: {collected_at})")
        return (temperature, collected_at)
        
    except Exception as e:
        logging.error(f"DB에서 기온 조회 실패: {e}")
        return None

