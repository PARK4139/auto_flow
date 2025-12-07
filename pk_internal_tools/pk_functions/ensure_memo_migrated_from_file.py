def ensure_memo_migrated_from_file():
    """기존 메모 파일을 DB로 마이그레이션하는 함수"""
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
    import logging
    import sqlite3
    import re
    from pathlib import Path
    
    def parse_memo_file(file_path):
        """메모 파일을 파싱하여 메모 섹션들을 추출하는 함수"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 메모 섹션을 구분하는 패턴 (44개 이상의 연속된 언더스코어)
            import re
            sections = re.split(r'_{44,}', content)
            
            memos = []
            for section in sections:
                if section.strip():
                    lines = section.strip().split('\n')
                    
                    # 첫 번째 줄을 제목으로 사용 (사용자 요청사항)
                    title = lines[0].strip() if lines else "제목 없음"
                    content_start = 1
                    
                    if title and content_start < len(lines):
                        content_lines = lines[content_start:]
                        content_text = '\n'.join(content_lines).strip()
                        
                        # 내용이 있는 경우만 추가 (빈 섹션 제외)
                        if content_text and len(content_text) > 5:  # 최소 5자 이상
                            # 태그 추출
                            tags = []
                            tag_match = re.search(r'#(\w+)', content_text)
                            if tag_match:
                                tags = re.findall(r'#(\w+)', content_text)
                            
                            memos.append({
                                'title': title,
                                'content': content_text,
                                'tags': ', '.join(tags) if tags else None,
                                'category': 'general'
                            })
            
            logging.debug(f"파싱된 섹션 수: {len(sections)}")
            logging.debug(f"유효한 메모 수: {len(memos)}")
            
            return memos
            
        except Exception as e:
            logging.debug(f"메모 파일 파싱 실패: {str(e)}")
            return []
    
    def migrate_memos_to_db(memos, db_path):
        from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
        """메모들을 DB에 저장하는 함수"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            migrated_count = 0
            for memo in memos:
                cursor.execute("""
                INSERT INTO pk_memos (title, content, tags, category, created_at, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, (memo['title'], memo['content'], memo['tags'], memo['category']))
                migrated_count += 1
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return migrated_count
            
        except Exception as e:
            logging.debug(f"DB 마이그레이션 실패: {str(e)}")
            return 0
    
    try:
        # 메모 파일 경로
        memo_file_path = Path("/mnt/c/Users/wjdgn/Downloads/pk_memo/pkg_pk/pk_memo_how.pk")
        
        if not memo_file_path.exists():
            logging.debug("메모 파일을 찾을 수 없습니다.")
            return False
        
        # DB 경로
        db_path = F_PK_MEMO_SQLITE
        
        if not db_path.exists():
            logging.debug("메모 DB가 존재하지 않습니다.")
            return False
        
        logging.debug("메모 파일 마이그레이션 시작...")
        logging.debug(f"메모 파일: {memo_file_path}")
        logging.debug(f"파일 크기: {memo_file_path.stat().st_size / (1024*1024):.2f} MB")
        
        # 메모 파일 파싱
        logging.debug("  메모 파일 파싱 중...")
        memos = parse_memo_file(memo_file_path)
        
        if not memos:
            logging.debug("파싱된 메모가 없습니다.")
            return False
        
        logging.debug(f"파싱된 메모 수: {len(memos)}")
        
        # DB로 마이그레이션
        logging.debug("  DB로 마이그레이션 중...")
        migrated_count = migrate_memos_to_db(memos, db_path)
        
        if migrated_count > 0:
            logging.debug(f"메모 마이그레이션 완료: {migrated_count}개")
            
            # 마이그레이션 결과 확인
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pk_memos")
            total_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            logging.debug(f"DB 총 메모 수: {total_count}개")
            return True
        else:
            logging.debug("메모 마이그레이션 실패")
            return False
            
    except Exception as e:
        logging.debug(f"메모 마이그레이션 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    ensure_memo_migrated_from_file()
