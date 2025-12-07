

def ensure_memo_db_connected():
    """메모 DB 연결 상태를 확인하고 연결을 보장하는 함수"""
    from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    from pathlib import Path
    
    try:
        db_path = F_PK_MEMO_SQLITE
        
        if not db_path.exists():
            logging.debug("메모 DB 파일이 존재하지 않습니다.")
            return False
        
        # DB 연결 테스트
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 연결 상태 확인
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            logging.debug("메모 DB 연결 상태: 정상")
            
            # DB 버전 확인
            cursor.execute("SELECT sqlite_version()")
            version = cursor.fetchone()[0]
            logging.debug(f"SQLite 버전: {version}")
            
            # DB 모드 확인
            cursor.execute("PRAGMA journal_mode")
            journal_mode = cursor.fetchone()[0]
            logging.debug(f"저널 모드: {journal_mode}")
            
            # 외래키 제약 확인
            cursor.execute("PRAGMA foreign_keys")
            foreign_keys = cursor.fetchone()[0]
            logging.debug(f"외래키 제약: {'활성' if foreign_keys else '비활성'}")
            
        else:
            logging.debug("메모 DB 연결 상태: 비정상")
            return False
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        logging.debug(f"메모 DB 연결 확인 실패: {str(e)}")
        return False










