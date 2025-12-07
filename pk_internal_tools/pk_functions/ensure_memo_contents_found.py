from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE


def ensure_memo_contents_found():
    """
    pk_memo.sqlite 데이터베이스에서 메모를 검색하는 함수
    fzf를 사용한 실시간 검색으로 기존 파일 기반 검색을 대체
    """
    import logging, get_fzf_command, ensure_chcp_65001, get_os_n, ensure_console_cleared
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import sys
    import locale
    import time
    import subprocess
    from pathlib import Path
    import sqlite3

    def get_db_connection():
        """pk_memo.sqlite 데이터베이스 연결을 반환합니다."""
        db_path = F_PK_MEMO_SQLITE
        if not db_path.exists():
            logging.debug(f"데이터베이스 파일이 존재하지 않습니다: {db_path}")
            return None

        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row  # 컬럼명으로 접근 가능하도록 설정
            return conn
        except Exception as e:
            logging.debug(f"데이터베이스 연결 실패: {str(e)}")
            return None

    def search_memos_in_db(conn, search_keywords):
        """데이터베이스에서 키워드로 메모를 검색합니다."""
        if not conn:
            return []

        try:
            cursor = conn.cursor()

            # 빈 키워드인 경우 모든 메모 반환
            if not search_keywords:
                query = """
                    SELECT id, title, content, tags, category, file_line_start, file_line_end, created_at, updated_at
                    FROM pk_memos 
                    ORDER BY updated_at DESC, created_at DESC
                    LIMIT 1000
                """
                cursor.execute(query)
            else:
                # 검색 쿼리 구성 (모든 키워드가 포함된 메모 검색)
                query = """
                    SELECT id, title, content, tags, category, file_line_start, file_line_end, created_at, updated_at
                    FROM pk_memos 
                    WHERE 1=1
                """
                params = []

                # 각 키워드에 대해 content와 title에서 검색
                for i, keyword in enumerate(search_keywords):
                    query += f" AND (content LIKE ? OR title LIKE ?)"
                    params.extend([f"%{keyword}%", f"%{keyword}%"])

                query += " ORDER BY updated_at DESC, created_at DESC"
                cursor.execute(query, params)

            results = cursor.fetchall()

            if QC_MODE:
                logging.debug(f"DB 검색 쿼리: {query}")
                if search_keywords:
                    logging.debug(f"검색 파라미터: {params}")
                logging.debug(f"검색 결과 수: {len(results)}")

            return results

        except Exception as e:
            logging.debug(f"데이터베이스 검색 오류: {str(e)}")
            return []

    def display_search_results_db(search_results, search_keywords):
        """DB 검색 결과를 출력합니다."""
        if not search_results:
            keyword_str = " ".join(search_keywords)
            logging.debug(f"'{keyword_str}'가 모두 포함된 메모를 찾을 수 없습니다.")
            return

        # 검색 결과 전체 출력
        keyword_str = " ".join(search_keywords)
        logging.debug(f"'{keyword_str}'가 모두 포함된 메모 ({len(search_results)}개)")

        for i, memo_row in enumerate(search_results, 1):
            # 메모 ID와 제목 출력
            memo_id = memo_row['id']
            title = memo_row['title'] or "제목 없음"

            # 제목에 키워드 하이라이트 적용
            from pk_internal_tools.pk_functions.get_keyword_colors import highlight_multiple_keywords_fast
            title_highlighted = highlight_multiple_keywords_fast(title, search_keywords)
            title_colored = f'\033[38;5;75m{title_highlighted}\033[0m'

            print(f"[{i:>3}] (ID: {memo_id}) {title_colored}")

            # 메모 내용 출력
            content = memo_row['content'] or ""
            if content:
                # 내용에 키워드 하이라이트 적용
                content_highlighted = highlight_multiple_keywords_fast(content, search_keywords)
                print(content_highlighted)

            # 태그와 카테고리 출력
            if memo_row['tags']:
                print(f"태그: {memo_row['tags']}")
            if memo_row['category']:
                print(f"카테고리: {memo_row['category']}")

            # 메타데이터 출력
            meta_parts = []
            if memo_row['file_line_start'] and memo_row['file_line_end']:
                meta_parts.append(f"파일 위치: {memo_row['file_line_start']}-{memo_row['file_line_end']}")
            if memo_row['created_at']:
                meta_parts.append(f"생성: {memo_row['created_at']}")
            if memo_row['updated_at']:
                meta_parts.append(f"수정: {memo_row['updated_at']}")

            if meta_parts:
                print(f"메타: {' | '.join(meta_parts)}")

            print()  # 빈 줄 추가

    def write_search_results_to_log_db(search_results, search_keywords, log_file_path):
        """DB 검색 결과를 로그 파일에 저장합니다."""
        try:
            with open(log_file_path, 'w', encoding=PkEncoding.UTF8.value) as f:
                f.write(f"'{' '.join(search_keywords)}' DB 검색 결과 ({len(search_results)}개) ===\n")
                f.write(f"생성 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("_" * 80 + "\n\n")

                for i, memo_row in enumerate(search_results, 1):
                    f.write(f"[{i}] (ID: {memo_row['id']})\n")
                    f.write(f"제목: {memo_row['title'] or '제목 없음'}\n")
                    f.write(f"내용: {memo_row['content'] or ''}\n")
                    if memo_row['tags']:
                        f.write(f"태그: {memo_row['tags']}\n")
                    if memo_row['category']:
                        f.write(f"카테고리: {memo_row['category']}\n")
                    if memo_row['file_line_start'] and memo_row['file_line_end']:
                        f.write(f"파일 위치: {memo_row['file_line_start']}-{memo_row['file_line_end']}\n")
                    if memo_row['created_at']:
                        f.write(f"생성: {memo_row['created_at']}\n")
                    if memo_row['updated_at']:
                        f.write(f"수정: {memo_row['updated_at']}\n")
                    f.write("_" * 80 + "\n\n")

            logging.debug(f"검색 결과가 로그 파일에 저장되었습니다: {log_file_path}")
        except Exception as e:
            logging.debug(f"로그 파일 쓰기 실패: {str(e)}")

    def open_result_log_file():
        """d_pk_logs/ensure_pk_memo_searched.log 파일을 열고 초기화하는 함수"""
        try:
            from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
            from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made

            # 로그 파일 경로
            log_file = Path(d_pk_logs) / "ensure_pk_memo_searched.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)

            # 프로그램 시작 시 로그 파일 초기화
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            initial_content = f"메모 DB 검색 로그 파일 ===\n"
            initial_content += f"프로그램 시작 시간: {current_time}\n"
            initial_content += f"로그 파일이 초기화되었습니다.\n"
            initial_content += "_" * 80 + "\n\n"

            # 로그 파일에 초기 내용 쓰기 (덮어쓰기)
            with open(log_file, 'w', encoding=PkEncoding.UTF8.value) as f:
                f.write(initial_content)

            logging.debug(f"로그 파일이 초기화되었습니다: {log_file}")

            # 파일 열기
            ensure_pnx_opened_by_ext(str(log_file))
            logging.debug(f"검색 결과 로그 파일이 열렸습니다: {log_file}")
            return str(log_file)
        except Exception as e:
            logging.debug(f"로그 파일 열기 실패: {str(e)}")
            return None

    # 프로그램 시작 시 로그 파일 열기
    logging.debug("메모 DB 검색 시스템 초기화")

    # d_pk_logs/ensure_pk_memo_searched.log 열기
    log_file_path = open_result_log_file()

    if not log_file_path:
        logging.debug("로그 파일을 열 수 없어 검색 기능이 제한됩니다.")

    if get_os_n() == 'windows':
        ensure_chcp_65001()
        # 추가 인코딩 설정
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        # locale 설정
        try:
            locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'Korean_Korea.65001')
            except:
                pass

    # fzf를 사용한 실시간 DB 검색
    try:
        ensure_console_cleared()
        logging.debug("fzf 기반 실시간 메모 DB 검색 시스템")
        logging.debug("fzf를 사용하여 실시간으로 메모를 검색합니다.")
        logging.debug("Ctrl+C: 종료")
        print()  # 빈 줄 추가

        # 데이터베이스 연결
        db_conn = get_db_connection()
        if not db_conn:
            logging.debug("데이터베이스 연결에 실패했습니다. 프로그램을 종료합니다.")
            return

        # fzf 명령어 구성
        fzf_cmd = get_fzf_command()
        if not fzf_cmd:
            logging.debug("fzf가 설치되지 않았습니다. 기본 검색 모드로 전환합니다.")
            # 기본 검색 모드로 전환
            search_input = input("검색 키워드: ").strip()
            if not search_input:
                logging.debug("키워드가 입력되지 않았습니다.")
                return

            search_keywords = [kw.strip() for kw in search_input.split() if kw.strip()]
            if not search_keywords:
                logging.debug("유효한 키워드가 없습니다.")
                return

            logging.debug(f"검색 키워드: {' '.join(search_keywords)}")
            print()

            # DB에서 검색 실행
            logging.debug("데이터베이스에서 검색 중...")
            search_results = search_memos_in_db(db_conn, search_keywords)

            # 검색 결과 출력
            display_search_results_db(search_results, search_keywords)

            # 검색 결과를 로그 파일에 저장
            if log_file_path:
                write_search_results_to_log_db(search_results, search_keywords, log_file_path)

            # 검색 완료 메시지
            keyword_str = " ".join(search_keywords)
            if search_results:
                logging.debug(f"검색 완료: '{keyword_str}'가 모두 포함된 메모 {len(search_results)}개를 찾았습니다.")
            else:
                logging.debug(f"'{keyword_str}'가 모두 포함된 메모를 찾을 수 없습니다.")

            return

        # fzf를 사용한 실시간 검색 실행
        logging.debug("fzf를 사용하여 메모를 검색합니다...")
        logging.debug("검색어를 입력하면 실시간으로 결과가 필터링됩니다.")
        print()

        # 모든 메모를 fzf에 전달할 데이터로 준비
        all_memos = search_memos_in_db(db_conn, [])  # 빈 키워드로 모든 메모 가져오기

        if not all_memos:
            logging.debug("데이터베이스에서 메모를 가져올 수 없습니다.")
            return

        # fzf용 입력 데이터 구성 (제목 | 내용 | 태그 | 카테고리)
        fzf_input_lines = []
        for memo in all_memos:
            title = memo['title'] or "제목 없음"
            content = memo['content'] or ""
            tags = memo['tags'] or ""
            category = memo['category'] or ""

            # fzf에서 검색할 수 있도록 모든 정보를 포함
            fzf_line = f"{title} | {content[:100]} | {tags} | {category}"
            fzf_input_lines.append(fzf_line)

        # fzf 명령어 실행
        try:
            fzf_process = subprocess.Popen(
                fzf_cmd.split() + [
                    '--preview', 'echo "{}"',
                    '--preview-window', 'right:60%',
                    '--height', '80%',
                    '--border',
                    '--header', '메모 검색 (Ctrl+C: 종료)'
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            # fzf에 데이터 전송
            fzf_input = '\n'.join(fzf_input_lines)
            stdout, stderr = fzf_process.communicate(input=fzf_input)

            if fzf_process.returncode == 0 and stdout.strip():
                # 선택된 메모 찾기
                selected_line = stdout.strip()
                selected_index = fzf_input_lines.index(selected_line)
                selected_memo = all_memos[selected_index]

                # 선택된 메모 상세 정보 출력
                ensure_console_cleared()
                logging.debug("선택된 메모 상세 정보")
                print()

                # 선택된 메모만 포함하는 결과 리스트 생성
                search_results = [selected_memo]
                search_keywords = ["선택된 메모"]

                # 검색 결과 출력
                display_search_results_db(search_results, search_keywords)

                # 검색 결과를 로그 파일에 저장
                if log_file_path:
                    write_search_results_to_log_db(search_results, search_keywords, log_file_path)

                logging.debug("메모 선택이 완료되었습니다.")

            else:
                logging.debug("메모가 선택되지 않았습니다.")

        except Exception as e:
            logging.debug(f"fzf 실행 중 오류 발생: {str(e)}")
            logging.debug("기본 검색 모드로 전환합니다.")

            # 기본 검색 모드로 전환
            search_input = input("검색 키워드: ").strip()
            if not search_input:
                logging.debug("키워드가 입력되지 않았습니다.")
                return

            search_keywords = [kw.strip() for kw in search_input.split() if kw.strip()]
            if not search_keywords:
                logging.debug("유효한 키워드가 없습니다.")
                return

            logging.debug(f"검색 키워드: {' '.join(search_keywords)}")
            print()

            # DB에서 검색 실행
            logging.debug("데이터베이스에서 검색 중...")
            search_results = search_memos_in_db(db_conn, search_keywords)

            # 검색 결과 출력
            display_search_results_db(search_results, search_keywords)

            # 검색 결과를 로그 파일에 저장
            if log_file_path:
                write_search_results_to_log_db(search_results, search_keywords, log_file_path)

            # 검색 완료 메시지
            keyword_str = " ".join(search_keywords)
            if search_results:
                logging.debug(f"검색 완료: '{keyword_str}'가 모두 포함된 메모 {len(search_results)}개를 찾았습니다.")
            else:
                logging.debug(f"'{keyword_str}'가 모두 포함된 메모를 찾을 수 없습니다.")

    except Exception as e:
        logging.debug(f"검색 중 오류 발생: {str(e)}")
    finally:
        # 데이터베이스 연결 종료
        if 'db_conn' in locals() and db_conn:
            db_conn.close()
            logging.debug("데이터베이스 연결이 종료되었습니다.")

    # 편집 시스템 안내
    if log_file_path:
        logging.debug("편집 시스템이 활성화되었습니다.")
        logging.debug(f"검색 결과를 편집하려면 {log_file_path} 파일을 수정하세요.")
