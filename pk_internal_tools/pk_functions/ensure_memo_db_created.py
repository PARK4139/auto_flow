def ensure_memo_db_created():
    """메모용 SQLite 데이터베이스와 테이블을 생성하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    import sqlite3
    import time
    import shutil
    from pathlib import Path
    
    def create_memo_table(cursor):
        """메모 테이블 생성"""
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pk_memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            category TEXT DEFAULT 'general',
            file_line_start INTEGER,
            file_line_end INTEGER,
            file_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 검색 성능 향상을 위한 인덱스 생성
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON pk_memos(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_content ON pk_memos(content)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON pk_memos(tags)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON pk_memos(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_updated_at ON pk_memos(updated_at)")
        
        # 전문 검색을 위한 FTS5 가상 테이블 생성
        cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS pk_memos_fts USING fts5(
            title, content, tags, category,
            content='pk_memos',
            content_rowid='id'
        )
        """)
        
        # 트리거: 메인 테이블 변경 시 FTS 테이블 자동 업데이트
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS pk_memos_ai AFTER INSERT ON pk_memos BEGIN
            INSERT INTO pk_memos_fts(rowid, title, content, tags, category) 
            VALUES (new.id, new.title, new.content, new.tags, new.category);
        END
        """)
        
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS pk_memos_ad AFTER DELETE ON pk_memos BEGIN
            INSERT INTO pk_memos_fts(pk_memos_fts, rowid, title, content, tags, category) 
            VALUES('delete', old.id, old.title, old.content, old.tags, old.category);
        END
        """)
        
        cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS pk_memos_au AFTER UPDATE ON pk_memos BEGIN
            INSERT INTO pk_memos_fts(pk_memos_fts, rowid, title, content, tags, category) 
            VALUES('delete', old.id, old.title, old.content, old.content, old.category);
            INSERT INTO pk_memos_fts(rowid, title, content, tags, category) 
            VALUES (new.id, new.title, new.content, new.tags, new.category);
        END
        """)
    
    try:
        # DB 디렉토리 생성
        db_dir = d_pk_root_hidden
        db_dir.mkdir(parents=True, exist_ok=True)
        
        # 메인 DB 파일 경로
        from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
        main_db_path = F_PK_MEMO_SQLITE
        
        # 기존 DB가 있으면 백업
        if main_db_path.exists():
            timestamp = time.strftime("%Y_%m_%d_%H%M%S")
            backup_name = f"pk_memo_{timestamp}.sqlite"
            backup_path = db_dir / backup_name
            
            shutil.copy2(main_db_path, backup_path)
            logging.debug(f"기존 DB 백업 완료: {backup_path}")
        
        # DB 연결 및 테이블 생성
        conn = sqlite3.connect(str(main_db_path))
        cursor = conn.cursor()
        
        # 테이블 생성
        create_memo_table(cursor)
        
        # 변경사항 저장
        conn.commit()
        
        # 테이블 정보 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        logging.debug(f"메모 DB 생성 완료: {main_db_path}")
        logging.debug(f"생성된 테이블: {[table[0] for table in tables]}")
        
        cursor.close()
        conn.close()
        
        return str(main_db_path)
        
    except Exception as e:
        logging.debug(f"메모 DB 생성 실패: {str(e)}")
        return None

