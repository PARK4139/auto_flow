from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE


def ensure_memo_db_only():
    """원본 메모 파일을 제거하고 DB 전용 구조로 전환하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    import shutil
    from pathlib import Path
    
    def backup_original_file(original_path):
        """원본 파일을 백업하는 함수"""
        try:
            if not original_path.exists():
                logging.debug("원본 파일이 이미 제거되었습니다.")
                return True
            
            # 백업 디렉토리 생성
            backup_dir = d_pk_root_hidden / "original_backup"
            backup_dir.mkdir(exist_ok=True)
            
            # 백업 파일명 생성 (타임스탬프 포함)
            timestamp = time.strftime("%Y_%m_%d_%H%M%S")
            backup_name = f"pk_memo_how_original_{timestamp}.pk"
            backup_path = backup_dir / backup_name
            
            # 파일 복사
            shutil.copy2(original_path, backup_path)
            
            file_size = original_path.stat().st_size / (1024 * 1024)
            logging.debug(f"원본 파일 백업 완료: {backup_path.nick_name} ({file_size:.2f} MB)")
            
            return True
            
        except Exception as e:
            logging.debug(f"원본 파일 백업 실패: {str(e)}")
            return False
    
    def verify_db_integrity(db_path):
        """DB 무결성을 검증하는 함수"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 메모 수 확인
            cursor.execute("SELECT COUNT(*) FROM pk_memos")
            memo_count = cursor.fetchone()[0]
            
            # FTS 테이블 동기화 확인
            cursor.execute("SELECT COUNT(*) FROM pk_memos_fts")
            fts_count = cursor.fetchone()[0]
            
            # 테이블 구조 확인
            cursor.execute("PRAGMA table_info(pk_memos)")
            columns = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            logging.debug("DB 무결성 검증:")
            logging.debug(f"메모 수: {memo_count}개")
            logging.debug(f"FTS 인덱스: {fts_count}개")
            logging.debug(f"컬럼 수: {len(columns)}개")
            
            # FTS 동기화 확인
            if memo_count == fts_count:
                logging.debug("  FTS 동기화: 정상")
            else:
                logging.debug(" ️ FTS 동기화: 불일치")
            
            return memo_count > 0
            
        except Exception as e:
            logging.debug(f"DB 무결성 검증 실패: {str(e)}")
            return False
    
    def remove_original_file(original_path):
        """원본 파일을 제거하는 함수"""
        try:
            if original_path.exists():
                original_path.unlink()
                logging.debug("️ 원본 메모 파일 제거 완료")
            else:
                logging.debug("원본 파일이 이미 제거되었습니다.")
            
            return True
            
        except Exception as e:
            logging.debug(f"원본 파일 제거 실패: {str(e)}")
            return False
    
    def create_db_only_structure(db_path):
        """DB 전용 구조를 생성하는 함수"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # DB 전용 메타데이터 테이블 생성
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pk_memo_metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # DB 전용 구조임을 표시
            cursor.execute("""
            INSERT OR REPLACE INTO pk_memo_metadata (key, value, updated_at)
            VALUES ('db_only_mode', 'true', CURRENT_TIMESTAMP)
            """)
            
            # 마이그레이션 완료 시간 기록
            cursor.execute("""
            INSERT OR REPLACE INTO pk_memo_metadata (key, value, updated_at)
            VALUES ('migration_completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logging.debug("DB 전용 구조 생성 완료")
            return True
            
        except Exception as e:
            logging.debug(f"DB 전용 구조 생성 실패: {str(e)}")
            return False
    
    try:
        import time
        
        logging.debug("DB 전용 구조로 전환 시작...")
        
        # n. 원본 파일 경로
        original_path = Path("/mnt/c/Users/wjdgn/Downloads/pk_memo/pkg_pk/pk_memo_how.pk")
        
        # n. DB 경로
        db_path = F_PK_MEMO_SQLITE
        
        if not db_path.exists():
            logging.debug("메모 DB가 존재하지 않습니다.")
            return False
        
        # n. DB 무결성 검증
        logging.debug("DB 무결성 검증 중...")
        if not verify_db_integrity(db_path):
            logging.debug("DB 무결성 검증 실패")
            return False
        
        # n. 원본 파일 백업
        logging.debug("원본 파일 백업 중...")
        if not backup_original_file(original_path):
            logging.debug("원본 파일 백업 실패")
            return False
        
        # n. DB 전용 구조 생성
        logging.debug("️ DB 전용 구조 생성 중...")
        if not create_db_only_structure(db_path):
            logging.debug("DB 전용 구조 생성 실패")
            return False
        
        # 6. 원본 파일 제거
        logging.debug("️ 원본 파일 제거 중...")
        if not remove_original_file(original_path):
            logging.debug("원본 파일 제거 실패")
            return False
        
        logging.debug("DB 전용 구조로 전환 완료!")
        logging.debug("이제 모든 메모는 DB에서 관리됩니다.")
        
        return True
        
    except Exception as e:
        logging.debug(f"DB 전용 전환 중 오류 발생: {str(e)}")
        return False










