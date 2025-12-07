import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE


def get_temperature_history_from_db(
    hours: int = 24,
    limit: Optional[int] = None,
    db_path: Optional[Path] = None
) -> List[Dict]:
    """
    DB에서 기온 히스토리 데이터를 조회합니다 (그래프용).
    
    Args:
        hours: 조회할 시간 범위 (시간). 기본값 24시간.
        limit: 최대 조회 개수. None이면 제한 없음.
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        List[Dict]: 기온 데이터 리스트. 각 항목은 {'temperature': float, 'collected_at': datetime, 'city': str, ...}
    """
    try:
        if db_path is None:
            db_path = F_pk_SQLITE
        
        if not db_path.exists():
            logging.debug(f"DB 파일이 존재하지 않습니다: {db_path}")
            return []
        
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 최근 hours 시간 이내의 데이터 조회
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        query = """
            SELECT temperature, collected_at, latitude, longitude, city, country_code
            FROM temperature_data 
            WHERE collected_at >= ?
            ORDER BY collected_at DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cur.execute(query, (cutoff_time,))
        rows = cur.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            # collected_at을 datetime 객체로 변환
            collected_at_str = row['collected_at']
            if isinstance(collected_at_str, str):
                try:
                    if 'T' in collected_at_str:
                        collected_at = datetime.fromisoformat(collected_at_str)
                    else:
                        collected_at = datetime.fromisoformat(collected_at_str.replace(' ', 'T', 1))
                except ValueError:
                    logging.warning(f"날짜 파싱 실패: {collected_at_str}")
                    collected_at = datetime.now()
            elif isinstance(collected_at_str, (int, float)):
                collected_at = datetime.fromtimestamp(collected_at_str)
            else:
                collected_at = datetime.now()
            
            result.append({
                'temperature': float(row['temperature']),
                'collected_at': collected_at,
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'city': row['city'],
                'country_code': row['country_code']
            })
        
        logging.debug(f"기온 히스토리 조회 성공: {len(result)}개 (최근 {hours}시간)")
        return result
        
    except Exception as e:
        logging.error(f"기온 히스토리 조회 실패: {e}")
        return []

