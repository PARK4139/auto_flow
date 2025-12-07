def ensure_memo_duplicate_check():
    """메모 DB에서 중복 내용을 확인하고 정리하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
    import hashlib
    
    def check_duplicates_by_content():
        """내용 기반으로 중복 메모를 확인하는 함수"""
        try:
            db_path = F_PK_MEMO_SQLITE
            
            if not db_path.exists():
                logging.debug("메모 DB 파일이 존재하지 않습니다.")
                return False
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 전체 메모 수 확인
            cursor.execute("SELECT COUNT(*) FROM pk_memos")
            total_count = cursor.fetchone()[0]
            logging.debug(f"전체 메모 수: {total_count}개")
            
            # 내용 기반 중복 확인 (내용이 정확히 동일한 경우)
            cursor.execute("""
                SELECT content, COUNT(*) as count, GROUP_CONCAT(id) as ids, GROUP_CONCAT(title) as titles
                FROM pk_memos 
                GROUP BY content 
                HAVING COUNT(*) > 1
                ORDER BY count DESC
            """)
            
            exact_duplicates = cursor.fetchall()
            
            if exact_duplicates:
                logging.debug(f"정확한 내용 중복 발견: {len(exact_duplicates)}개 그룹")
                for content, count, ids, titles in exact_duplicates:
                    logging.debug(f"중복 {count}개: {titles[:100]}...")
                    logging.debug(f"ID: {ids}")
            else:
                logging.debug("정확한 내용 중복 없음")
            
            # 제목 기반 중복 확인
            cursor.execute("""
                SELECT title, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM pk_memos 
                GROUP BY title 
                HAVING COUNT(*) > 1
                ORDER BY count DESC
            """)
            
            title_duplicates = cursor.fetchall()
            
            if title_duplicates:
                logging.debug(f"제목 중복 발견: {len(title_duplicates)}개 그룹")
                for title, count, ids in title_duplicates:
                    logging.debug(f"제목 중복 {count}개: {title[:100]}...")
                    logging.debug(f"ID: {ids}")
            else:
                logging.debug("제목 중복 없음")
            
            # 내용 길이별 분포 확인
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN LENGTH(content) < 50 THEN '50자 미만'
                        WHEN LENGTH(content) < 100 THEN '50-100자'
                        WHEN LENGTH(content) < 200 THEN '100-200자'
                        WHEN LENGTH(content) < 500 THEN '200-500자'
                        ELSE '500자 이상'
                    END as content_length,
                    COUNT(*) as count
                FROM pk_memos 
                GROUP BY content_length
                ORDER BY 
                    CASE content_length
                        WHEN '50자 미만' THEN 1
                        WHEN '50-100자' THEN 2
                        WHEN '100-200자' THEN 3
                        WHEN '200-500자' THEN 4
                        ELSE 5
                    END
            """)
            
            length_distribution = cursor.fetchall()
            logging.debug("내용 길이별 분포:")
            for length_range, count in length_distribution:
                logging.debug(f"{length_range}: {count}개")
            
            # 태그별 분포 확인
            cursor.execute("""
                SELECT tags, COUNT(*) as count
                FROM pk_memos 
                WHERE tags IS NOT NULL AND tags != ''
                GROUP BY tags
                ORDER BY count DESC
                LIMIT 10
            """)
            
            tag_distribution = cursor.fetchall()
            if tag_distribution:
                logging.debug("️ 상위 태그 분포:")
                for tags, count in tag_distribution:
                    logging.debug(f"{tags}: {count}개")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            logging.debug(f"중복 확인 실패: {str(e)}")
            return False
    
    def check_duplicates_by_hash():
        """해시 기반으로 중복 메모를 확인하는 함수 (내용 정규화 후)"""
        try:
            db_path = F_PK_MEMO_SQLITE
            
            if not db_path.exists():
                logging.debug("메모 DB 파일이 존재하지 않습니다.")
                return False
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # 모든 메모 내용 가져오기
            cursor.execute("SELECT id, title, content FROM pk_memos")
            all_memos = cursor.fetchall()
            
            # 내용 정규화 및 해시 생성
            hash_dict = {}
            normalized_duplicates = []
            
            for memo_id, title, content in all_memos:
                # 내용 정규화 (공백, 줄바꿈 정리)
                normalized_content = ' '.join(content.strip().split())
                content_hash = hashlib.md5(normalized_content.encode('utf-8')).hexdigest()
                
                if content_hash in hash_dict:
                    normalized_duplicates.append({
                        'hash': content_hash,
                        'original': hash_dict[content_hash],
                        'duplicate': {'id': memo_id, 'title': title, 'content': content}
                    })
                else:
                    hash_dict[content_hash] = {'id': memo_id, 'title': title, 'content': content}
            
            if normalized_duplicates:
                logging.debug(f"정규화 후 중복 발견: {len(normalized_duplicates)}개")
                for dup in normalized_duplicates[:5]:  # 상위 5개만 표시
                    logging.debug(f"중복: {dup['duplicate']['title'][:50]}...")
                    logging.debug(f"원본 ID: {dup['original']['id']}, 중복 ID: {dup['duplicate']['id']}")
            else:
                logging.debug("정규화 후 중복 없음")
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            logging.debug(f"해시 기반 중복 확인 실패: {str(e)}")
            return False
    
    try:
        logging.debug("메모 DB 중복 확인 시작...")
        
        # n. 기본 중복 확인
        logging.debug(" 1단계: 기본 중복 확인")
        check_duplicates_by_content()
        
        # n. 해시 기반 중복 확인
        logging.debug(" 2단계: 해시 기반 중복 확인")
        check_duplicates_by_hash()
        
        logging.debug(" 메모 DB 중복 확인 완료")
        return True
        
    except Exception as e:
        logging.debug(f"중복 확인 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    ensure_memo_duplicate_check()
