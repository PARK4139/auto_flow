import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE


def get_p110m_energy_history_from_db(
    device_host: Optional[str] = None,
    days: int = 365,
    limit: Optional[int] = None,
    db_path: Optional[Path] = None
) -> List[Dict]:
    """
    DB에서 P110M 에너지 히스토리 데이터를 조회합니다 (그래프용).
    
    Args:
        device_host: 장치 호스트. None이면 모든 장치 조회.
        days: 조회할 날짜 범위 (일). 기본값 365일 (1년).
        limit: 최대 조회 개수. None이면 제한 없음.
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        List[Dict]: 에너지 데이터 리스트. 각 항목은 다음 키를 포함:
            - device_host: 장치 호스트
            - current_power: 현재 소비 전력 (W)
            - today_energy: 오늘 사용 에너지 (Wh)
            - today_runtime: 오늘 가동 시간 (초)
            - month_energy: 이번 달 사용 에너지 (Wh)
            - month_runtime: 이번 달 가동 시간 (초)
            - local_time: 조회 시간 (datetime)
            - collected_at: 수집 시간 (datetime)
    """
    try:
        if db_path is None:
            # 환경 변수에서 DB 경로 확인 (Xavier에서 실행 시)
            env_db_path = os.environ.get("pk_SQLITE_PATH")
            if env_db_path:
                db_path = Path(env_db_path)
            else:
                db_path = F_pk_SQLITE
        
        if not db_path.exists():
            logging.debug(f"DB 파일이 존재하지 않습니다: {db_path}")
            return []
        
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        # 최근 days 일 이내의 데이터 조회
        cutoff_time = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT device_host, current_power, today_energy, today_runtime,
                   month_energy, month_runtime, local_time, collected_at
            FROM p110m_energy_data 
            WHERE collected_at >= ?
        """
        params = [cutoff_time]
        
        if device_host:
            query += " AND device_host = ?"
            params.append(device_host)
        
        query += " ORDER BY collected_at DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            # local_time과 collected_at을 datetime 객체로 변환
            local_time = None
            if row['local_time']:
                local_time_str = row['local_time']
                try:
                    if isinstance(local_time_str, str):
                        if 'T' in local_time_str:
                            local_time = datetime.fromisoformat(local_time_str.replace('Z', '+00:00'))
                        else:
                            local_time = datetime.fromisoformat(local_time_str.replace(' ', 'T', 1))
                    else:
                        local_time = local_time_str
                except (ValueError, AttributeError):
                    logging.warning(f"날짜 파싱 실패: {local_time_str}")
                    local_time = None
            
            collected_at = None
            if row['collected_at']:
                collected_at_str = row['collected_at']
                try:
                    if isinstance(collected_at_str, str):
                        if 'T' in collected_at_str:
                            collected_at = datetime.fromisoformat(collected_at_str.replace('Z', '+00:00'))
                        else:
                            collected_at = datetime.fromisoformat(collected_at_str.replace(' ', 'T', 1))
                    else:
                        collected_at = collected_at_str
                except (ValueError, AttributeError):
                    logging.warning(f"날짜 파싱 실패: {collected_at_str}")
                    collected_at = datetime.now()
            else:
                collected_at = datetime.now()
            
            result.append({
                'device_host': row['device_host'],
                'current_power': row['current_power'],
                'today_energy': row['today_energy'],
                'today_runtime': row['today_runtime'],
                'month_energy': row['month_energy'],
                'month_runtime': row['month_runtime'],
                'local_time': local_time,
                'collected_at': collected_at
            })
        
        logging.debug(f"P110M 에너지 히스토리 조회 성공: {len(result)}개 (최근 {days}일)")
        return result
        
    except Exception as e:
        logging.error(f"P110M 에너지 히스토리 조회 실패: {e}", exc_info=True)
        return []

