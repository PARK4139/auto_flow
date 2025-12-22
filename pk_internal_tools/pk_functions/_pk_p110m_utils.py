import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

def get_p110m_energy_history_from_db(db_path: Path, device_host: Optional[str] = None, days: int = 365, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """DB에서 P110M 에너지 히스토리 조회"""
    try:
        if not db_path.exists():
            logger.debug("DB 파일이 존재하지 않습니다: %s", db_path)
            return []
        
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cutoff_time = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT device_host, current_power, today_energy, today_runtime,
                   month_energy, month_runtime, local_time, collected_at
            FROM p110m_energy_data 
            WHERE collected_at >= ?
        """
        params = [cutoff_time.isoformat()]
        
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
            local_time = None
            if row['local_time']:
                try:
                    local_time = datetime.fromisoformat(row['local_time'].replace('Z', '+00:00'))
                except Exception as e:
                    pass
            
            collected_at = None
            if row['collected_at']:
                try:
                    collected_at = datetime.fromisoformat(row['collected_at'].replace('Z', '+00:00'))
                except Exception as e:
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
        
        logger.debug("에너지 히스토리 조회 완료: %d개 레코드", len(result))
        return result
    except Exception as e:
        logger.error("에너지 히스토리 조회 실패: %s", e, exc_info=True)
        return []

def get_p110m_energy_aggregated_for_graph(db_path: Path, device_host: Optional[str] = None, period: str = "year") -> List[Dict[str, Any]]:
    """P110M 에너지 데이터 집계"""
    try:
        days_map = {"day": 1, "week": 7, "month": 30, "year": 365}
        days = days_map.get(period, 365)
        
        history_data = get_p110m_energy_history_from_db(db_path=db_path, device_host=device_host, days=days, limit=None)
        
        if not history_data:
            logger.debug("집계할 에너지 데이터가 없습니다.")
            return []
        
        aggregated = defaultdict(lambda: {
            'total_energy': 0.0,
            'power_values': [],
            'total_runtime': 0,
            'data_points': 0
        })
        
        for record in history_data:
            date_key = None
            if record.get('collected_at'):
                date_key = record['collected_at'].date().isoformat()
            elif record.get('local_time'):
                if isinstance(record['local_time'], datetime):
                    date_key = record['local_time'].date().isoformat()
                elif isinstance(record['local_time'], str):
                    try:
                        date_key = datetime.fromisoformat(record['local_time']).date().isoformat()
                    except Exception as e:
                        continue
            else:
                continue
            
            if not date_key:
                continue
            
            if record.get('today_energy') is not None:
                aggregated[date_key]['total_energy'] = max(
                    aggregated[date_key]['total_energy'],
                    record.get('today_energy', 0.0) or 0.0
                )
            
            if record.get('current_power') is not None:
                power = record.get('current_power', 0.0) or 0.0
                aggregated[date_key]['power_values'].append(power)
            
            if record.get('today_runtime') is not None:
                aggregated[date_key]['total_runtime'] = max(
                    aggregated[date_key]['total_runtime'],
                    record.get('today_runtime', 0) or 0
                )
            
            aggregated[date_key]['data_points'] += 1
        
        result = []
        for date_key in sorted(aggregated.keys()):
            data = aggregated[date_key]
            
            avg_power = 0.0
            max_power = 0.0
            if data['power_values']:
                avg_power = sum(data['power_values']) / len(data['power_values'])
                max_power = max(data['power_values'])
            
            result.append({
                'date': date_key,
                'total_energy': data['total_energy'],
                'avg_power': avg_power,
                'max_power': max_power,
                'total_runtime': data['total_runtime'],
                'data_points': data['data_points']
            })
        
        logger.debug("에너지 데이터 집계 완료: %d개 날짜", len(result))
        return result
    except Exception as e:
        logger.error("에너지 집계 실패: %s", e, exc_info=True)
        return []