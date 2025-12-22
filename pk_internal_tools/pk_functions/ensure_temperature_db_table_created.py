import sqlite3
import logging
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_objects.pk_files import F_pk_SQLITE


def ensure_temperature_db_table_created(db_path: Optional[Path] = None) -> bool:
    """
    기온 데이터를 저장할 테이블을 생성합니다.
    
    Args:
        db_path: DB 파일 경로. None이면 기본 경로 사용.
        
    Returns:
        bool: 성공 시 True, 실패 시 False.
    """
    try:
        if db_path is None:
            db_path = F_pk_SQLITE
        
        # DB 파일이 없으면 디렉토리 생성
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        # 기온 데이터 테이블 생성
        cur.execute("""
            CREATE TABLE IF NOT EXISTS temperature_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                latitude REAL,
                longitude REAL,
                city TEXT,
                country_code TEXT,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 인덱스 생성 (조회 성능 향상)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_temperature_collected_at 
            ON temperature_data(collected_at DESC)
        """)
        
        conn.commit()
        conn.close()
        
        logging.debug(f"기온 데이터 테이블 생성 완료: {db_path}")
        return True
        
    except Exception as e:
        logging.error(f"기온 데이터 테이블 생성 실패: {e}")
        return False

