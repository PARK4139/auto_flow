import sqlite3
import logging
import os
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE


def ensure_pk_p110m_energy_db_table_created(db_path: Optional[Path] = None) -> bool:
    """
    P110M 에너지 데이터를 저장할 테이블을 생성합니다.
    
    Args:
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
        
        # DB 파일이 없으면 디렉토리 생성
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        # 에너지 데이터 테이블 생성
        cur.execute("""
            CREATE TABLE IF NOT EXISTS p110m_energy_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_host TEXT NOT NULL,
                current_power REAL,
                today_energy REAL,
                today_runtime INTEGER,
                month_energy REAL,
                month_runtime INTEGER,
                local_time TIMESTAMP,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 인덱스 생성 (조회 성능 향상)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_p110m_energy_collected_at 
            ON p110m_energy_data(collected_at DESC)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_p110m_energy_device_host 
            ON p110m_energy_data(device_host)
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_p110m_energy_local_time 
            ON p110m_energy_data(local_time DESC)
        """)
        
        conn.commit()
        conn.close()
        
        logging.debug(f"P110M 에너지 데이터 테이블 생성 완료: {db_path}")
        return True
        
    except Exception as e:
        logging.error(f"P110M 에너지 데이터 테이블 생성 실패: {e}")
        return False

