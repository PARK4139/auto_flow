from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE


def ensure_memo_db_backup_compressed():
    """tar.bz2 압축을 사용하여 메모 DB를 백업하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    import time
    import shutil
    from pathlib import Path
    
    def create_compressed_backup(db_path):
        """DB를 tar.bz2로 압축 백업하는 함수"""
        try:
            # 백업 디렉토리 생성
            backup_dir = d_pk_root_hidden / "compressed_backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # 타임스탬프로 백업 파일명 생성
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = f"pk_memo_db_backup_{timestamp}.tar.bz2"
            backup_path = backup_dir / backup_name
            
            # DB 파일 경로 확인
            if not db_path.exists():
                logging.debug(f"백업할 DB 파일이 존재하지 않습니다: {db_path}")
                return None
            
            # tar.bz2 압축으로 백업
            # root_dir은 파일이 있는 디렉토리, base_dir은 파일명
            root_dir = str(db_path.parent)
            base_dir = db_path.nick_name
            
            logging.debug(f"압축 백업 시작: {root_dir} -> {base_dir}")
            
            # 압축 백업 생성
            shutil.make_archive(
                str(backup_path).replace('.tar.bz2', ''), 
                'bztar', 
                root_dir=root_dir,
                base_dir=base_dir
            )
            
            # 백업 파일 크기 확인
            backup_size = backup_path.stat().st_size / (1024 * 1024)
            original_size = db_path.stat().st_size / (1024 * 1024)
            compression_ratio = (1 - backup_size / original_size) * 100
            
            logging.debug(f"압축 백업 완료: {backup_path.nick_name}")
            logging.debug(f"원본 크기: {original_size:.2f} MB")
            logging.debug(f"백업 크기: {backup_size:.2f} MB")
            logging.debug(f"️ 압축률: {compression_ratio:.1f}%")
            
            return str(backup_path)
            
        except Exception as e:
            logging.debug(f"압축 백업 실패: {str(e)}")
            return None
    
    def verify_backup_integrity(backup_path, original_db_path):
        """백업 파일의 무결성을 검증하는 함수"""
        try:
            # 임시 디렉토리에 백업 해제
            import tempfile
            temp_dir = Path(tempfile.mkdtemp())
            
            # tar.bz2 파일 해제
            shutil.unpack_archive(backup_path, temp_dir, 'bztar')
            
            # 해제된 DB 파일 찾기
            extracted_db = None
            for file_path in temp_dir.rglob("*.sqlite"):
                if file_path.name == original_db_path.nick_name:
                    extracted_db = file_path
                    break
            
            if not extracted_db:
                logging.debug("백업에서 DB 파일을 찾을 수 없습니다.")
                return False
            
            # DB 연결 테스트
            conn = sqlite3.connect(str(extracted_db))
            cursor = conn.cursor()
            
            # 메모 수 확인
            cursor.execute("SELECT COUNT(*) FROM pk_memos")
            memo_count = cursor.fetchone()[0]
            
            # FTS 테이블 확인
            cursor.execute("SELECT COUNT(*) FROM pk_memos_fts")
            fts_count = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            # 임시 디렉토리 정리
            shutil.rmtree(temp_dir)
            
            logging.debug("백업 무결성 검증:")
            logging.debug(f"메모 수: {memo_count}개")
            logging.debug(f"FTS 인덱스: {fts_count}개")
            
            if memo_count > 0 and fts_count > 0:
                logging.debug("  백업 무결성: 정상")
                return True
            else:
                logging.debug("  백업 무결성: 비정상")
                return False
                
        except Exception as e:
            logging.debug(f"백업 무결성 검증 실패: {str(e)}")
            return False
    
    def cleanup_old_backups(backup_dir, max_backups=10):
        """오래된 백업 파일을 정리하는 함수"""
        try:
            if not backup_dir.exists():
                return
            
            # tar.bz2 백업 파일들 찾기
            backup_files = list(backup_dir.glob("pk_memo_db_backup_*.tar.bz2"))
            
            if len(backup_files) <= max_backups:
                return
            
            # 수정 시간 기준으로 정렬 (오래된 것부터)
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            
            # 오래된 백업 파일들 제거
            files_to_remove = backup_files[:-max_backups]
            
            for old_backup in files_to_remove:
                old_backup.unlink()
                logging.debug(f"️ 오래된 백업 제거: {old_backup.nick_name}")
            
            logging.debug(f"백업 정리 완료: {len(files_to_remove)}개 제거")
            
        except Exception as e:
            logging.debug(f"백업 정리 실패: {str(e)}")
    
    def get_backup_status(backup_dir):
        """백업 상태를 확인하는 함수"""
        try:
            if not backup_dir.exists():
                logging.debug("백업 디렉토리가 존재하지 않습니다.")
                return
            
            # tar.bz2 백업 파일들 찾기
            backup_files = list(backup_dir.glob("pk_memo_db_backup_*.tar.bz2"))
            
            if not backup_files:
                logging.debug("압축 백업 파일이 없습니다.")
                return
            
            # 수정 시간 기준으로 정렬 (최신 것부터)
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            logging.debug("압축 백업 상태:")
            logging.debug(f"총 백업 수: {len(backup_files)}개")
            
            # 최신 백업 정보
            latest_backup = backup_files[0]
            backup_size = latest_backup.stat().st_size / (1024 * 1024)
            backup_time = time.ctime(latest_backup.stat().st_mtime)
            
            logging.debug(f"최신 백업: {latest_backup.nick_name}")
            logging.debug(f"백업 크기: {backup_size:.2f} MB")
            logging.debug(f"백업 시간: {backup_time}")
            
            # 백업 정책 정보
            logging.debug("  백업 정책:")
            logging.debug("   - 형식: tar.bz2 압축")
            logging.debug("   - 위치: .pk_system/compressed_backup/")
            logging.debug("   - 최대 보관: 10개")
            
        except Exception as e:
            logging.debug(f"백업 상태 확인 실패: {str(e)}")
    
    try:
        # DB 경로 확인
        db_path = F_PK_MEMO_SQLITE
        
        if not db_path.exists():
            logging.debug("메모 DB가 존재하지 않습니다.")
            return False
        
        # 백업 디렉토리
        backup_dir = d_pk_root_hidden / "compressed_backup"
        
        logging.debug("메모 DB 압축 백업 시작...")
        
        # n. 압축 백업 생성
        backup_path = create_compressed_backup(db_path)
        if not backup_path:
            return False
        
        # n. 백업 무결성 검증
        logging.debug("백업 무결성 검증 중...")
        if not verify_backup_integrity(Path(backup_path), db_path):
            logging.debug("백업 무결성 검증 실패")
            return False
        
        # n. 오래된 백업 정리
        logging.debug("오래된 백업 정리 중...")
        cleanup_old_backups(backup_dir)
        
        # n. 백업 상태 표시
        logging.debug("백업 상태 확인 중...")
        get_backup_status(backup_dir)
        
        logging.debug("메모 DB 압축 백업 완료!")
        return True
        
    except Exception as e:
        logging.debug(f"메모 DB 압축 백업 중 오류 발생: {str(e)}")
        return False










