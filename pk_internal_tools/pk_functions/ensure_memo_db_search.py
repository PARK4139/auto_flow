def ensure_memo_db_search():
    """DB 기반 실시간 메모 검색을 구현하는 함수"""
    from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
    import logging
    import sqlite3
    import time

    def search_memos_by_keyword(keyword, db_path):
        """키워드로 메모를 검색하는 함수"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            # FTS5를 사용한 전문 검색
            query = """
            SELECT id, title, content, tags, category, updated_at,
                   snippet(pk_memos_fts, -1, '<mark>', '</mark>', '...', 32) as snippet
            FROM pk_memos_fts 
            WHERE pk_memos_fts MATCH ?
            ORDER BY rank
            LIMIT 20
            """

            cursor.execute(query, (keyword,))
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            return results

        except Exception as e:
            logging.debug(f"검색 실패: {str(e)}")
            return []

    def search_memos_by_tag(tag, db_path):
        """태그로 메모를 검색하는 함수"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            query = """
            SELECT id, title, content, tags, category, updated_at
            FROM pk_memos 
            WHERE tags LIKE ?
            ORDER BY updated_at DESC
            LIMIT 20
            """

            cursor.execute(query, (f'%{tag}%',))
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            return results

        except Exception as e:
            logging.debug(f"태그 검색 실패: {str(e)}")
            return []

    def search_memos_by_category(category, db_path):
        """카테고리로 메모를 검색하는 함수"""
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            query = """
            SELECT id, title, content, tags, category, updated_at
            FROM pk_memos 
            WHERE category = ?
            ORDER BY updated_at DESC
            LIMIT 20
            """

            cursor.execute(query, (category,))
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            return results

        except Exception as e:
            logging.debug(f"카테고리 검색 실패: {str(e)}")
            return []

    def display_search_results(results, search_type="키워드"):
        """검색 결과를 표시하는 함수"""
        if not results:
            logging.debug(f"{search_type} 검색 결과가 없습니다.")
            return

        logging.debug(f"{search_type} 검색 결과: {len(results)}개")
        logging.debug("=" * 60)

        for i, result in enumerate(results, 1):
            memo_id, title, content, tags, category, updated_at, *extra = result

            logging.debug(f"메모 #{i} (ID: {memo_id})")
            logging.debug(f"제목: {title}")

            if extra and extra[0]:  # snippet이 있는 경우
                logging.debug(f"내용: {extra[0]}")
            else:
                content_preview = content[:100] + "..." if len(content) > 100 else content
                logging.debug(f"내용: {content_preview}")

            if tags:
                logging.debug(f"️ 태그: {tags}")

            logging.debug(f"카테고리: {category}")
            logging.debug(f"수정: {updated_at}")
            logging.debug("-" * 40)

    def interactive_search(db_path):
        """대화형 검색 인터페이스"""
        logging.debug("DB 기반 실시간 메모 검색 시작")
        logging.debug("사용법:")
        logging.debug(" - 키워드 검색: 그냥 입력")
        logging.debug(" - 태그 검색: #태그명")
        logging.debug(" - 카테고리 검색: @카테고리명")
        logging.debug(" - 종료: quit 또는 exit")
        logging.debug("=" * 60)

        while True:
            try:
                query = input(" 검색어 입력: ").strip()

                if query.lower() in ['quit', 'exit', '종료']:
                    logging.debug("검색을 종료합니다.")
                    break

                if not query:
                    continue

                start_time = time.time()

                if query.startswith('#'):
                    # 태그 검색
                    tag = query[1:]
                    results = search_memos_by_tag(tag, db_path)
                    display_search_results(results, f"태그 '{tag}'")

                elif query.startswith('@'):
                    # 카테고리 검색
                    category = query[1:]
                    results = search_memos_by_category(category, db_path)
                    display_search_results(results, f"카테고리 '{category}'")

                else:
                    # 키워드 검색
                    results = search_memos_by_keyword(query, db_path)
                    display_search_results(results, f"키워드 '{query}'")

                search_time = time.time() - start_time
                logging.debug(f"️ 검색 시간: {search_time:.3f}초")
                logging.debug("=" * 60)

            except KeyboardInterrupt:
                logging.debug(" 검색을 종료합니다.")
                break
            except Exception as e:
                logging.debug(f"검색 중 오류 발생: {str(e)}")

    try:
        # DB 경로 확인
        db_path = F_PK_MEMO_SQLITE

        if not db_path.exists():
            logging.debug("메모 DB가 존재하지 않습니다.")
            return False

        # DB 연결 테스트
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pk_memos")
        memo_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if memo_count == 0:
            logging.debug("DB에 메모가 없습니다. 먼저 마이그레이션을 진행하세요.")
            return False

        logging.debug(f"DB 검색 준비 완료 (메모 {memo_count}개)")

        # 대화형 검색 시작
        interactive_search(db_path)

        return True

    except Exception as e:
        logging.debug(f"DB 검색 초기화 실패: {str(e)}")
        return False



