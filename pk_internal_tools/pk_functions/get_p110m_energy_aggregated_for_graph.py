import logging
import os
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from collections import defaultdict

from pk_internal_tools.pk_functions.get_p110m_energy_history_from_db import get_p110m_energy_history_from_db


def get_p110m_energy_aggregated_for_graph(
    device_host: Optional[str] = None,
    period: str = "year",  # "day", "week", "month", "year"
    db_path: Optional[Path] = None
) -> List[Dict]:
    """
    P110M 에너지 데이터를 그래프용으로 집계합니다.
    
    Args:
        device_host: 장치 호스트. None이면 모든 장치 조회.
        period: 집계 기간 ("day", "week", "month", "year"). 기본값 "year".
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        List[Dict]: 집계된 에너지 데이터 리스트. 각 항목은 다음 키를 포함:
            - date: 날짜 (YYYY-MM-DD 형식)
            - total_energy: 총 사용 에너지 (Wh)
            - avg_power: 평균 소비 전력 (W)
            - max_power: 최대 소비 전력 (W)
            - total_runtime: 총 가동 시간 (초)
            - data_points: 데이터 포인트 수
    """
    try:
        # 기간에 따른 조회 일수 설정
        days_map = {
            "day": 1,
            "week": 7,
            "month": 30,
            "year": 365
        }
        
        days = days_map.get(period, 365)
        
        # 히스토리 데이터 조회
        history_data = get_p110m_energy_history_from_db(
            device_host=device_host,
            days=days,
            limit=None,
            db_path=db_path
        )
        
        if not history_data:
            logging.debug(f"집계할 에너지 데이터가 없습니다.")
            return []
        
        # 날짜별로 집계
        aggregated = defaultdict(lambda: {
            'total_energy': 0.0,
            'power_values': [],
            'total_runtime': 0,
            'data_points': 0
        })
        
        for record in history_data:
            # 날짜 키 생성 (collected_at 또는 local_time 사용)
            date_key = None
            if record.get('collected_at'):
                date_key = record['collected_at'].date().isoformat()
            elif record.get('local_time'):
                if isinstance(record['local_time'], datetime):
                    date_key = record['local_time'].date().isoformat()
                elif isinstance(record['local_time'], str):
                    try:
                        date_key = datetime.fromisoformat(record['local_time']).date().isoformat()
                    except (ValueError, AttributeError):
                        continue
            else:
                continue
            
            if not date_key:
                continue
            
            # 에너지 데이터 집계
            if record.get('today_energy') is not None:
                # 오늘 사용 에너지는 일일 데이터이므로 그대로 사용
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
        
        # 결과 리스트 생성
        result = []
        for date_key in sorted(aggregated.keys()):
            data = aggregated[date_key]
            
            # 평균 및 최대 전력 계산
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
        
        logging.debug(f"P110M 에너지 데이터 집계 완료: {len(result)}개 ({period} 기간)")
        return result
        
    except Exception as e:
        logging.error(f"P110M 에너지 데이터 집계 실패: {e}", exc_info=True)
        return []

