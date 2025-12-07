from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE


def ensure_memo_deduplication():
    """메모 DB에서 중복 내용을 제거하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    from pathlib import Path
    import hashlib
    
    def remove_duplicates_by_hash():
        """해시 기반으로 중복 메모를 제거하는 함수"""
        try:
            db_path = F_PK_MEMO_SQLITE
            
            if not db_path.exists():
                logging.debug("메모 DB 파일이 존재하지 않습니다.")
                return False
            
            # 백업 생성
            backup_path = db_path.parent / f"pk_memo_backup_before_dedup_{Path(__file__).stem}.sqlite"
            import shutil
            shutil.copy2(db_path, backup_path)
            logging.debug(f"백업 생성: {backup_path}")
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 전체 메모 수 확인
            cursor.execute("SELECT COUNT(*) FROM pk_memos")
            total_before = cursor.fetchone()[0]
            logging.debug(f"중복 제거 전 총 메모 수: {total_before}개")
            
            # 모든 메모 내용 가져오기
            cursor.execute("SELECT id, title, content, created_at, updated_at FROM pk_memos ORDER BY id")
            all_memos = cursor.fetchall()
            
            # 내용 정규화 및 해시 생성
            hash_dict = {}
            duplicates_to_remove = []
            
            for memo_id, title, content, created_at, updated_at in all_memos:
                # 내용 정규화 (공백, 줄바꿈 정리)
                normalized_content = ' '.join(content.strip().split())
                content_hash = hashlib.md5(normalized_content.encode('utf-8')).hexdigest()
                
                if content_hash in hash_dict:
                    # 중복 발견: 더 오래된 메모를 제거 대상으로 설정
                    existing_memo = hash_dict[content_hash]
                    if created_at < existing_memo['created_at']:
                        # 기존 메모가 더 최신이면 현재 메모를 제거
                        duplicates_to_remove.append(memo_id)
                    else:
                        # 현재 메모가 더 최신이면 기존 메모를 제거하고 현재 메모로 교체
                        duplicates_to_remove.append(existing_memo['id'])
                        hash_dict[content_hash] = {
                            'id': memo_id, 
                            'title': title, 
                            'content': content,
                            'created_at': created_at,
                            'updated_at': updated_at
                        }
                else:
                    hash_dict[content_hash] = {
                        'id': memo_id, 
                        'title': title, 
                        'content': content,
                        'created_at': created_at,
                        'updated_at': updated_at
                    }
            
            if duplicates_to_remove:
                logging.debug(f"제거할 중복 메모 수: {len(duplicates_to_remove)}개")
                
                # 중복 메모 제거
                placeholders = ','.join(['?' for _ in duplicates_to_remove])
                cursor.execute(f"DELETE FROM pk_memos WHERE id IN ({placeholders})", duplicates_to_remove)
                
                # 변경사항 커밋
                conn.commit()
                
                # 중복 제거 후 메모 수 확인
                cursor.execute("SELECT COUNT(*) FROM pk_memos")
                total_after = cursor.fetchone()[0]
                
                logging.debug(f"중복 제거 완료: {total_before}개 → {total_after}개")
                logging.debug(f"제거된 메모: {total_before - total_after}개")
                
            else:
                logging.debug("제거할 중복 메모가 없습니다.")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            logging.debug(f"중복 제거 실패: {str(e)}")
            return False
    
    def remove_title_duplicates():
        """제목 중복을 제거하는 함수"""
        try:
            db_path = F_PK_MEMO_SQLITE
            
            if not db_path.exists():
                logging.debug("메모 DB 파일이 존재하지 않습니다.")
                return False
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 제목 중복 확인
            cursor.execute("""
                SELECT title, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM pk_memos 
                GROUP BY title 
                HAVING COUNT(*) > 1
                ORDER BY count DESC
            """)
            
            title_duplicates = cursor.fetchall()
            
            if title_duplicates:
                logging.debug(f"제목 중복 그룹: {len(title_duplicates)}개")
                
                removed_count = 0
                for title, count, ids in title_duplicates:
                    id_list = [int(id_str) for id_str in ids.split(',')]
                    # 첫 번째 ID는 유지하고 나머지는 제거
                    ids_to_remove = id_list[1:]
                    
                    if ids_to_remove:
                        placeholders = ','.join(['?' for _ in ids_to_remove])
                        cursor.execute(f"DELETE FROM pk_memos WHERE id IN ({placeholders})", ids_to_remove)
                        removed_count += len(ids_to_remove)
                
                conn.commit()
                logging.debug(f"제목 중복 제거 완료: {removed_count}개 제거")
            else:
                logging.debug("제목 중복이 없습니다.")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            logging.debug(f"제목 중복 제거 실패: {str(e)}")
            return False
    
    try:
        logging.debug("메모 DB 중복 제거 시작...")
        
        # n. 내용 중복 제거 (해시 기반)
        logging.debug(" 1단계: 내용 중복 제거")
        remove_duplicates_by_hash()
        
        # n. 제목 중복 제거
        logging.debug(" 2단계: 제목 중복 제거")
        remove_title_duplicates()
        
        # n. 최종 상태 확인
        logging.debug(" 3단계: 최종 상태 확인")
        from pk_internal_tools.pk_functions.ensure_memo_db_status import ensure_memo_db_status
        ensure_memo_db_status()
        
        logging.debug(" 메모 DB 중복 제거 완료")
        return True
        
    except Exception as e:
        logging.debug(f"중복 제거 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    ensure_memo_deduplication()
