from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE


def ensure_memo_db_status():
    """메모 DB 상태를 확인하고 상태 정보를 출력하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    import os
    from pathlib import Path
    
    try:
        db_path = F_PK_MEMO_SQLITE
        
        if not db_path.exists():
            logging.debug("메모 DB 파일이 존재하지 않습니다.")
            return False
        
        # DB 연결
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 테이블 정보 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # 메모 개수 확인
        cursor.execute("SELECT COUNT(*) FROM pk_memos")
        memo_count = cursor.fetchone()[0]
        
        # DB 파일 크기 확인
        file_size = os.path.getsize(db_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # 최근 메모 확인
        cursor.execute("SELECT title, updated_at FROM pk_memos ORDER BY updated_at DESC LIMIT 3")
        recent_memos = cursor.fetchall()
        
        # 상태 정보 출력
        logging.debug("메모 DB 상태 정보:")
        logging.debug(f"DB 경로: {db_path}")
        logging.debug(f"파일 크기: {file_size_mb:.2f} MB")
        logging.debug(f"️ 테이블 수: {len(tables)}")
        logging.debug(f"메모 개수: {memo_count}")
        
        if tables:
            logging.debug(f"테이블 목록: {[table[0] for table in tables]}")
        
        if recent_memos:
            logging.debug("  최근 메모:")
            for title, updated_at in recent_memos:
                logging.debug(f"{title} (수정: {updated_at})")
        else:
            logging.debug("  저장된 메모가 없습니다.")
        
        cursor.close()
        conn.close()
        
        logging.debug("메모 DB 상태 확인 완료")
        return True
        
    except Exception as e:
        logging.debug(f"메모 DB 상태 확인 실패: {str(e)}")
        return False


if __name__ == "__main__":
    ensure_memo_db_status()

