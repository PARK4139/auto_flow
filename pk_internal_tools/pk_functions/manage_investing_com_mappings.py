import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path

# d_pk_cache는 pk_objects/pk_directories.py에 정의되어 있습니다.
from pk_internal_tools.pk_objects.pk_directories import d_pk_cache

STOCK_DB_PATH = Path(d_pk_cache) / "stock_data.sqlite"

# 자주 사용되는 티커에 대한 investing.com 기본 URL 매핑
DEFAULT_INVESTING_COM_MAPPINGS = {
    "QQQ": {"url": "https://www.investing.com/etfs/powershares-qqqq", "selector": '[data-test="instrument-price-last"]', "structure_hash": None},
    # "AAPL": {"url": "https://www.investing.com/equities/apple-computer-inc", "selector": None, "structure_hash": None}, # 필요시 추가
    # "NVDA": {"url": "https://www.investing.com/equities/nvidia-corp", "selector": None, "structure_hash": None}, # 필요시 추가
}

def _get_db_connection():
    """SQLite DB 연결을 반환합니다."""
    conn = sqlite3.connect(STOCK_DB_PATH)
    conn.row_factory = sqlite3.Row # 컬럼 이름으로 접근 가능하도록 설정
    return conn

def _create_mapping_table():
    """매핑 테이블이 없으면 생성하고, 'selector' 컬럼이 없으면 추가합니다."""
    with _get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS investing_com_url_mappings (
                ticker TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                selector TEXT,
                structure_hash TEXT, -- New column
                last_updated TEXT NOT NULL
            )
        """)
        # Check if 'selector' column exists and add if not (for existing databases)
        cursor = conn.execute("PRAGMA table_info(investing_com_url_mappings)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'selector' not in columns:
            conn.execute("ALTER TABLE investing_com_url_mappings ADD COLUMN selector TEXT")
        # Check if 'structure_hash' column exists and add if not
        if 'structure_hash' not in columns:
            conn.execute("ALTER TABLE investing_com_url_mappings ADD COLUMN structure_hash TEXT")
        conn.commit()
    logging.info("investing_com_url_mappings 테이블이 준비되었습니다.")

def get_investing_com_url(ticker: str) -> Optional[Dict[str, str]]:
    """
    주어진 티커에 대한 investing.com URL, 선택자, 구조 해시를 DB에서 조회합니다.
    DB에 없으면 DEFAULT_INVESTING_COM_MAPPINGS에서 찾아 자동으로 저장하고 반환합니다.
    """
    _create_mapping_table() # 테이블이 없으면 생성
    ticker_upper = ticker.upper()
    with _get_db_connection() as conn:
        cursor = conn.execute("SELECT url, selector, structure_hash FROM investing_com_url_mappings WHERE ticker = ?", (ticker_upper,))
        row = cursor.fetchone()
        if row:
            logging.debug(f"DB에서 {ticker_upper}의 investing.com URL을 찾았습니다: {row['url']}, 선택자: {row['selector']}, 구조 해시: {row['structure_hash']}")
            return {'url': row['url'], 'selector': row['selector'], 'structure_hash': row['structure_hash']}
        
        # DB에 없으면 기본 매핑에서 찾아 자동으로 저장
        if ticker_upper in DEFAULT_INVESTING_COM_MAPPINGS:
            default_mapping = DEFAULT_INVESTING_COM_MAPPINGS[ticker_upper]
            default_url = default_mapping['url']
            default_selector = default_mapping['selector']
            default_structure_hash = default_mapping.get('structure_hash') # 기본 매핑에 해시가 없을 수도 있음
            set_investing_com_url(ticker_upper, default_url, default_selector, default_structure_hash) # DB에 자동 저장
            logging.info(f"기본 매핑에서 {ticker_upper}의 investing.com URL을 찾아 DB에 자동 저장했습니다: {default_url}, 선택자: {default_selector}, 구조 해시: {default_structure_hash}")
            return {'url': default_url, 'selector': default_selector, 'structure_hash': default_structure_hash}

        logging.debug(f"DB 및 기본 매핑에서 {ticker_upper}에 대한 investing.com URL을 찾을 수 없어 None을 반환합니다.")
        return None

def set_investing_com_url(ticker: str, url: str, selector: Optional[str] = None, structure_hash: Optional[str] = None):
    """
    주어진 티커에 대한 investing.com URL, 선택자, 구조 해시를 DB에 저장하거나 업데이트합니다.
    """
    _create_mapping_table() # 테이블이 없으면 생성
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _get_db_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO investing_com_url_mappings (ticker, url, selector, structure_hash, last_updated) VALUES (?, ?, ?, ?, ?)",
            (ticker.upper(), url, selector, structure_hash, current_time)
        )
        conn.commit()
    logging.info(f"DB에 {ticker}의 investing.com URL ({url}), 선택자 ({selector}), 구조 해시 ({structure_hash})를 저장/업데이트했습니다.")

def delete_investing_com_url(ticker: str):
    """
    주어진 티커에 대한 investing.com URL 매핑을 DB에서 삭제합니다.
    """
    _create_mapping_table() # 테이블이 없으면 생성
    with _get_db_connection() as conn:
        conn.execute("DELETE FROM investing_com_url_mappings WHERE ticker = ?", (ticker.upper(),))
        conn.commit()
    logging.info(f"DB에서 {ticker}의 investing.com URL 매핑을 삭제했습니다.")

# 초기화 시 테이블 생성
_create_mapping_table()
