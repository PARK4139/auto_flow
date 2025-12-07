"""
P110M 에너지 데이터를 조회하고 표시하는 함수
"""

import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

from pk_internal_tools.pk_functions.get_p110m_energy_history_from_db import get_p110m_energy_history_from_db
from pk_internal_tools.pk_functions.get_p110m_energy_aggregated_for_graph import get_p110m_energy_aggregated_for_graph
from pk_internal_tools.pk_functions.print_structured_data import print_structured_data


def ensure_p110m_energy_viewed(
    device_host: Optional[str] = None,
    period: str = "year",  # "day", "week", "month", "year"
    days: Optional[int] = None,
    limit: Optional[int] = 100,
    show_summary: bool = True,
    show_raw_data: bool = False
) -> bool:
    """
    P110M 에너지 데이터를 조회하고 표시합니다.
    
    Args:
        device_host: 장치 호스트. None이면 모든 장치 조회.
        period: 집계 기간 ("day", "week", "month", "year"). 기본값 "year".
        days: 조회할 날짜 범위 (일). None이면 period에 따라 자동 설정.
        limit: 최대 조회 개수. None이면 제한 없음.
        show_summary: 요약 정보 표시 여부.
        show_raw_data: 원본 데이터 표시 여부.
        
    Returns:
        bool: 조회 성공 여부
    """
    try:
        # 기간에 따른 일수 자동 설정
        if days is None:
            days_map = {
                "day": 1,
                "week": 7,
                "month": 30,
                "year": 365
            }
            days = days_map.get(period, 365)
        
        # 집계된 데이터 조회
        aggregated_data = get_p110m_energy_aggregated_for_graph(
            device_host=device_host,
            period=period,
            db_path=None
        )
        
        if not aggregated_data:
            logging.warning("조회된 에너지 데이터가 없습니다.")
            return False
        
        # 요약 정보 표시
        if show_summary:
            print_structured_data(
                {
                    "period": period,
                    "days": days,
                    "device_host": device_host or "모든 장치",
                    "total_records": len(aggregated_data),
                    "date_range": {
                        "start": aggregated_data[0]["date"] if aggregated_data else None,
                        "end": aggregated_data[-1]["date"] if aggregated_data else None
                    },
                    "total_energy": sum(d.get("total_energy", 0) for d in aggregated_data),
                    "avg_power": sum(d.get("avg_power", 0) for d in aggregated_data) / len(aggregated_data) if aggregated_data else 0,
                    "max_power": max((d.get("max_power", 0) for d in aggregated_data), default=0),
                    "total_runtime": sum(d.get("total_runtime", 0) for d in aggregated_data)
                },
                title="P110M 에너지 데이터 요약",
                summary_title="집계 정보",
                show_json=True,
                show_summary=True
            )
        
        # 원본 데이터 표시
        if show_raw_data:
            history_data = get_p110m_energy_history_from_db(
                device_host=device_host,
                days=days,
                limit=limit,
                db_path=None
            )
            
            if history_data:
                print_structured_data(
                    {
                        "total_records": len(history_data),
                        "sample_records": history_data[:10]  # 처음 10개만 샘플로 표시
                    },
                    title="P110M 에너지 원본 데이터 (샘플)",
                    summary_title="데이터 샘플",
                    show_json=True,
                    show_summary=False
                )
        
        logging.info(f"P110M 에너지 데이터 조회 완료: {len(aggregated_data)}개 ({period} 기간)")
        return True
        
    except Exception as e:
        logging.error(f"P110M 에너지 데이터 조회 실패: {e}", exc_info=True)
        return False

