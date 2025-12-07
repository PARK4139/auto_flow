
def ensure_memo_contents_found_improved():
    """
    개선된 메모 검색 및 편집 시스템
    
    주요 개선사항:
    1. 더 안정적인 실시간 검색
    2. 향상된 로그 파일 관리
    3. 개선된 변경 감지 및 적용 로직
    4. 더 나은 에러 처리
    """
    import logging, get_fzf_command, does_pnx_exist, ensure_chcp_65001, get_os_n, ensure_console_cleared
    from pk_internal_tools.pk_objects.pk_files import F_MEMO_RAW
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    import re
    import subprocess
    import sys
    import locale
    import os
    import time
    import shutil
    import threading
    import hashlib
    from pathlib import Path

    def backup_memo_file():
        """pk_memo_how.pk 파일을 백업하는 함수 (개선됨)"""
        try:
            d_destination = Path(d_pk_logs) / "pk_memo_backup"
            d_destination.mkdir(parents=True, exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            f_destination_name = f"pk_memo_how_backup_{timestamp}.tar.bz2"
            f_destination = d_destination / f_destination_name
            
            memo_file_path = Path(F_MEMO_RAW)
            if not memo_file_path.exists():
                logging.debug(f"백업할 파일이 존재하지 않습니다: {F_MEMO_RAW}")
                return None
            
            # 개선된 백업: 파일 크기 체크
            file_size = memo_file_path.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB 이상이면 경고
                logging.debug(f"파일이 큽니다 ({file_size / 1024 / 1024:.1f}MB). 백업에 시간이 걸릴 수 있습니다.")
            
            root_dir = str(memo_file_path.parent)
            base_dir = memo_file_path.name
            
            logging.debug(f"백업 시작: {root_dir} -> {base_dir}")
            
            shutil.make_archive(
                str(f_destination).replace('.tar.bz2', ''),
                'bztar', 
                root_dir=root_dir,
                base_dir=base_dir
            )
            
            logging.debug(f"메모 파일 백업 완료: {f_destination}")
            return str(f_destination)
        except Exception as e:
            logging.debug(f"백업 실패: {str(e)}")
            return None

    def open_result_log_file():
        """로그 파일을 열고 초기화하는 함수 (개선됨)"""
        try:
            from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
            
            log_file = Path(d_pk_logs) / "ensure_pk_memo_searched.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            initial_content = f"개선된 메모 검색 로그 파일 ===\n"
            initial_content += f"프로그램 시작 시간: {current_time}\n"
            initial_content += f"로그 파일이 초기화되었습니다.\n"
            initial_content += f"사용법: 이 파일에서 메모 내용을 수정하면 자동으로 원본에 적용됩니다.\n"
            initial_content += f"주의: 수정할 때는 메모 내용만 변경하고, 구분선([숫자] (줄 번호) 등)은 건드리지 마세요.\n"
            initial_content += "_" * 80 + "\n\n"
            
            with open(log_file, 'w', encoding=PkEncoding.UTF8.value) as f:
                f.write(initial_content)
            
            logging.debug(f"로그 파일이 초기화되었습니다: {log_file}")
            
            ensure_pnx_opened_by_ext(str(log_file))
            logging.debug(f"검색 결과 로그 파일이 열렸습니다: {log_file}")
            return str(log_file)
        except Exception as e:
            logging.debug(f"로그 파일 열기 실패: {str(e)}")
            return None

    def write_search_results_to_log(found_contents, search_keywords, log_file_path):
        """검색 결과를 로그 파일에 쓰는 함수 (개선됨)"""
        try:
            with open(log_file_path, 'w', encoding=PkEncoding.UTF8.value) as f:
                f.write(f"'{' '.join(search_keywords)}' 검색 결과 ({len(found_contents)}개) ===\n")
                f.write(f"생성 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"편집 안내: 아래 메모 내용을 수정하면 자동으로 원본 파일에 적용됩니다.\n")
                f.write(f"주의: 수정할 때는 메모 내용만 변경하고, 구분선([숫자] (줄 번호) 등)은 건드리지 마세요.\n")
                f.write("_" * 80 + "\n\n")
                
                for i, (start_line, content) in enumerate(found_contents, 1):
                    f.write(f"[{i}] (줄 {start_line})\n")
                    f.write(content)
                    f.write("\n" + "_" * 80 + "\n\n")
            
            logging.debug(f"검색 결과가 로그 파일에 저장되었습니다: {log_file_path}")
        except Exception as e:
            logging.debug(f"로그 파일 쓰기 실패: {str(e)}")

    def detect_file_changes_and_apply(log_file_path, original_file_path):
        """로그 파일의 변경을 감지하고 원본 파일에 적용하는 함수 (개선됨)"""
        if not hasattr(detect_file_changes_and_apply, 'call_count'):
            detect_file_changes_and_apply.call_count = 0
        
        detect_file_changes_and_apply.call_count += 1
        
        if detect_file_changes_and_apply.call_count > 100:  # 호출 횟수 증가
            logging.debug(f"파일 변경 감지 함수가 {detect_file_changes_and_apply.call_count}번 호출되어 중단됩니다.")
            return
        
        try:
            # 개선된 변경 감지: 해시 기반
            with open(log_file_path, 'r', encoding=PkEncoding.UTF8.value) as f:
                log_content = f.read()
            
            current_hash = hashlib.md5(log_content.encode()).hexdigest()
            last_hash = getattr(detect_file_changes_and_apply, 'last_hash', '')
            
            if current_hash == last_hash:
                return  # 변경 없음
            
            if QC_MODE:
                logging.debug("로그 파일 변경이 감지되었습니다. 원본 파일을 업데이트합니다...")
            
            # 원본 파일 백업
            backup_path = backup_memo_file()
            
            # 원본 파일 읽기
            with open(original_file_path, 'r', encoding=PkEncoding.UTF8.value) as f:
                original_content = f.read()
            
            # 편집된 메모 추출
            edited_memos = extract_edited_memos_from_log(log_content, getattr(detect_file_changes_and_apply, 'last_log_content', ''))
            
            if edited_memos:
                if QC_MODE:
                    logging.debug(f"편집된 메모 {len(edited_memos)}개를 감지했습니다:")
                    for i, memo in enumerate(edited_memos, 1):
                        title = extract_memo_title(memo)
                        logging.debug(f"{i}. {title}")
                
                # 원본 파일에 편집된 내용 적용
                result = apply_edits_to_original(original_content, edited_memos)
                if isinstance(result, tuple):
                    updated_content, updated_sections = result
                else:
                    updated_content = result
                    updated_sections = len(edited_memos)
                
                # 업데이트된 내용을 원본 파일에 쓰기
                with open(original_file_path, 'w', encoding=PkEncoding.UTF8.value) as f:
                    f.write(updated_content)
                
                if QC_MODE:
                    logging.debug(f"원본 파일 업데이트가 완료되었습니다. 실제로 {updated_sections}개의 메모가 수정되었습니다.")
            
            # 현재 상태 저장
            detect_file_changes_and_apply.last_log_content = log_content
            detect_file_changes_and_apply.last_hash = current_hash
            
        except Exception as e:
            logging.debug(f"파일 변경 감지 및 적용 오류: {str(e)}")
            time.sleep(1)

    def extract_edited_memos_from_log(log_content, previous_log_content=""):
        """로그에서 편집된 메모만 추출하는 함수 (개선됨)"""
        edited_memos = []
        
        try:
            current_memos = extract_all_memos_from_log(log_content)
            previous_memos = extract_all_memos_from_log(previous_log_content) if previous_log_content else []
            
            for current_memo in current_memos:
                current_title = extract_memo_title(current_memo)
                previous_memo = None
                
                for prev_memo in previous_memos:
                    if extract_memo_title(prev_memo) == current_title:
                        previous_memo = prev_memo
                        break
                
                if not previous_memo:
                    if QC_MODE:
                        logging.debug(f"새로운 메모 감지: {current_title}")
                    edited_memos.append(current_memo)
                else:
                    # 개선된 내용 비교: 공백 정규화
                    current_normalized = re.sub(r'\s+', ' ', current_memo.strip())
                    previous_normalized = re.sub(r'\s+', ' ', previous_memo.strip())
                    
                    if current_normalized != previous_normalized:
                        if QC_MODE:
                            logging.debug(f"수정된 메모 감지: {current_title}")
                        edited_memos.append(current_memo)
            
        except Exception as e:
            logging.debug(f"편집된 메모 추출 오류: {str(e)}")
        
        return edited_memos

    def extract_all_memos_from_log(log_content):
        """로그에서 모든 메모를 추출하는 함수 (개선됨)"""
        memos = []
        current_memo = []
        in_memo_section = False
        
        for line in log_content.split('\n'):
            if line.startswith('===') and '검색 결과' in line:
                in_memo_section = True
                continue
            
            if not in_memo_section:
                continue
                
            # 개선된 구분자 패턴 감지
            if (re.match(r'^_{80}$', line) or           
                re.match(r'^_{50,}={50,}$', line) or    
                re.match(r'^={80}$', line)):            
                
                if current_memo:
                    memo_content = '\n'.join(current_memo).strip()
                    if memo_content:
                        memos.append(memo_content)
                    current_memo = []
            else:
                if not (line.startswith('[') and ']' in line and '(' in line) and not line.startswith('생성 시간'):
                    current_memo.append(line)
        
        if current_memo:
            memo_content = '\n'.join(current_memo).strip()
            if memo_content:
                memos.append(memo_content)
        
        return memos

    def extract_memo_title(memo_content):
        """메모에서 제목을 추출하는 함수 (개선됨)"""
        lines = memo_content.split('\n')
        for line in lines:
            line_stripped = line.strip()
            if (line_stripped and 
                not re.match(r'^_{50,}$', line_stripped) and 
                not re.match(r'^_{80}$', line_stripped) and
                not re.match(r'^_{50,}={50,}$', line_stripped)):
                return line_stripped
        return "제목 없음"

    def apply_edits_to_original(original_content, edited_memos):
        """편집된 메모를 원본 파일에 적용하는 함수 (개선됨)"""
        if not hasattr(apply_edits_to_original, 'call_count'):
            apply_edits_to_original.call_count = 0
        
        apply_edits_to_original.call_count += 1
        
        if apply_edits_to_original.call_count > 30:
            logging.debug(f"원본 파일 업데이트 함수가 {apply_edits_to_original.call_count}번 호출되어 중단됩니다.")
            return original_content
        
        try:
            # 원본 내용을 구분자로 분할
            sections = re.split(r'^_{50,}$', original_content, flags=re.MULTILINE)
            
            # 각 섹션을 구조화
            structured_sections = []
            for i, section in enumerate(sections):
                if section.strip():
                    structured_sections.append({
                        'content': section.strip(),
                        'title': extract_memo_title(section.strip()),
                        'original_content': section.strip()
                    })
            
            # 편집된 메모를 원본 섹션과 매칭하여 교체
            updated_sections = 0
            for section in structured_sections:
                for edited_memo in edited_memos:
                    edited_title = extract_memo_title(edited_memo)
                    
                    if section['title'] == edited_title:
                        # 내용이 실제로 변경되었는지 확인
                        original_normalized = re.sub(r'\s+', ' ', section['original_content'].strip())
                        edited_normalized = re.sub(r'\s+', ' ', edited_memo.strip())
                        
                        if original_normalized != edited_normalized:
                            if QC_MODE:
                                logging.debug(f"메모 업데이트: {section['title']}")
                            
                            section['content'] = edited_memo.strip()
                            updated_sections += 1
            
            # 수정된 섹션들을 다시 조합
            updated_content_parts = []
            for i, section in enumerate(structured_sections):
                if i > 0:
                    updated_content_parts.append('_' * 50)
                updated_content_parts.append(section['content'])
            
            updated_content = '\n'.join(updated_content_parts)
            
            if QC_MODE:
                logging.debug(f"실제로 업데이트된 섹션: {updated_sections}개")
            
            return updated_content, updated_sections
            
        except Exception as e:
            logging.debug(f"원본 파일 업데이트 오류: {str(e)}")
            return original_content

    def perform_search(f_memo, search_keywords):
        """메모 파일에서 키워드를 검색하는 함수 (개선됨)"""
        found_contents = []
        
        try:
            with open(f_memo, 'r', encoding=PkEncoding.UTF8.value) as f:
                content = f.read()
            
            # 메모를 구분자로 분할
            sections = re.split(r'^_{50,}$', content, flags=re.MULTILINE)
            
            current_start_line = 1
            for section in sections:
                if section.strip():
                    content_lower = section.lower()
                    all_keywords_found = all(keyword.lower() in content_lower for keyword in search_keywords)
                    if all_keywords_found:
                        found_contents.append((current_start_line, section))
                current_start_line += section.count('\n') + 1
                
        except Exception as e:
            logging.debug(f"파일 읽기 오류: {str(e)}")
            return []
        
        return found_contents

    def display_search_results(found_contents, search_keywords):
        """검색 결과를 출력하는 함수 (개선됨)"""
        keyword_str = " ".join(search_keywords)
        logging.debug(f"'{keyword_str}'가 모두 포함된 메모 컨텐츠 ({len(found_contents)}개)")

        max_line_num_width = len(str(max([start_line for start_line, _ in found_contents]))) if found_contents else 1
        max_index_width = len(str(len(found_contents))) if found_contents else 1

        for i, (start_line, content) in enumerate(found_contents, 1):
            lines = content.split('\n')
            title = ""
            for line in lines:
                line_stripped = line.strip()
                if line_stripped and not re.match(r'^_{50,}$', line_stripped):
                    title = line_stripped
                    break

            index_str = f"{i:>{max_index_width}}"
            line_num_str = f"{start_line:>{max_line_num_width}}"

            lines = content.split('\n')
            if lines and re.match(r'^_{50,}$', lines[0].strip()):
                print(f'\033[38;5;159m{lines[0]}\033[0m')
                lines = lines[1:]
            
            from pk_internal_tools.pk_functions.get_keyword_colors import highlight_multiple_keywords_fast
            title_highlighted = highlight_multiple_keywords_fast(title, search_keywords)
            title_colored = f'\033[38;5;75m{title_highlighted}\033[0m'
            print(f"[{index_str}] (줄 {line_num_str}) {title_colored}")
            
            if lines and lines[0].strip() == title:
                lines = lines[1:]
            
            out_lines = []
            for content_line in lines:
                if re.match(r'^_{50,}$', content_line.strip()):
                    out_lines.append(f'\033[38;5;159m{content_line}\033[0m')
                else:
                    out_lines.append(highlight_multiple_keywords_fast(content_line, search_keywords))

            content_output = "\n".join(out_lines).strip()
            if content_output:
                print(content_output)
            print()

    # 메인 실행 로직
    logging.debug("개선된 메모 편집 시스템 초기화")
    
    # n. pk_memo_how.pk 백업
    backup_path = backup_memo_file()
    
    # n. 로그 파일 열기
    log_file_path = open_result_log_file()
    
    if not log_file_path:
        logging.debug("로그 파일을 열 수 없어 편집 기능이 제한됩니다.")

    # n. 인코딩 설정
    if get_os_n() == 'windows':
        ensure_chcp_65001()
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        try:
            locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'Korean_Korea.65001')
            except:
                pass

    # n. 메모 파일 확인
    f_memo = rf'{F_MEMO_RAW}'
    if not does_pnx_exist(f_memo):
        logging.debug(f'''{f_memo} does not exist %%%FOO%%%''')
        return

    # n. 실시간 검색 인터페이스
    try:
        ensure_console_cleared()
        logging.debug("개선된 실시간 메모 검색 + 편집 시스템")
        logging.debug("검색할 키워드를 입력하세요 (실시간으로 검색 결과가 업데이트됩니다): ")
        logging.debug("Ctrl+U: 입력창 지우기, Ctrl+C: 종료")
        logging.debug("편집: d_pk_logs/ensure_pk_memo_searched.log 파일을 수정하면 자동으로 원본에 적용됩니다")
        print()
        
        search_keywords = []
        current_input = ""
        last_search_input = ""
        last_input_time = time.time()
        file_monitor_thread = None
        
        # 6. 파일 모니터링 스레드 시작
        def monitor_file_changes():
            last_check_time = 0
            error_count = 0
            max_errors = 5
            check_count = 0
            max_checks = 200
            
            while True:
                try:
                    time.sleep(2)
                    current_time = time.time()
                    check_count += 1
                    
                    if check_count >= max_checks:
                        logging.debug(f"파일 모니터링 스레드가 {max_checks}번 체크 후 자동 종료됩니다.")
                        break
                    
                    if (current_time - last_input_time > 3 and 
                        current_time - last_check_time > 5 and 
                        log_file_path and 
                        os.path.exists(log_file_path)):
                        
                        try:
                            file_size = os.path.getsize(log_file_path)
                            if file_size > 1024 * 1024:
                                logging.debug(f"로그 파일이 너무 큽니다 ({file_size} bytes). 모니터링을 건너뜁니다.")
                                time.sleep(10)
                                continue
                        except:
                            pass
                        
                        detect_file_changes_and_apply(log_file_path, f_memo)
                        last_check_time = current_time
                        error_count = 0
                        
                except Exception as e:
                    error_count += 1
                    logging.debug(f"파일 모니터링 오류 ({error_count}/{max_errors}): {str(e)}")
                    
                    if error_count >= max_errors:
                        logging.debug(f"파일 모니터링 스레드가 {max_errors}번 연속 오류로 인해 종료됩니다.")
                        break
                    
                    time.sleep(5)

        if log_file_path:
            file_monitor_thread = threading.Thread(target=monitor_file_changes, daemon=True)
            file_monitor_thread.start()
        
        # 7. 키보드 입력 처리
        if get_os_n() == 'windows':
            import msvcrt
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    last_input_time = time.time()
                    
                    if char == b'\r':
                        break
                    elif char == b'\x08':
                        if current_input:
                            current_input = current_input[:-1]
                            print('\r' + ' ' * (len(current_input) + 20) + '\r', end='')
                    elif char == b'\x15':
                        current_input = ""
                        ensure_console_cleared()
                        logging.debug("개선된 실시간 메모 검색 + 편집 시스템")
                        logging.debug("검색할 키워드를 입력하세요 (실시간으로 검색 결과가 업데이트됩니다): ")
                        logging.debug("Ctrl+U: 입력창 지우기, Ctrl+C: 종료")
                        logging.debug("편집: d_pk_logs/ensure_pk_memo_searched.log 파일을 수정하면 자동으로 원본에 적용됩니다")
                        print()
                        print("키워드: ", end='', flush=True)
                        continue
                    elif char == b'\x03':
                        logging.debug("검색이 취소되었습니다.")
                        return
                    else:
                        try:
                            char_str = char.decode('utf-8')
                            current_input += char_str
                        except UnicodeDecodeError:
                            try:
                                char_str = char.decode('cp949')
                                current_input += char_str
                            except:
                                continue
                    
                    print(f'\r키워드: {current_input}', end='', flush=True)
                    
                    if len(current_input) >= 2:
                        temp_keywords = [kw.strip() for kw in current_input.split() if kw.strip()]
                        if temp_keywords and temp_keywords != last_search_input:
                            print(f'\n\033[33m실시간 검색 중...\033[0m')
                            search_keywords = temp_keywords
                            last_search_input = temp_keywords.copy()
                            
                            ensure_console_cleared()
                            logging.debug("개선된 실시간 메모 검색 + 편집 시스템")
                            logging.debug(f"검색 키워드: {' '.join(search_keywords)}")
                            print()
                            
                            real_time_search_results = perform_search(f_memo, search_keywords)
                            if real_time_search_results:
                                display_search_results(real_time_search_results, search_keywords)
                                
                                if log_file_path:
                                    write_search_results_to_log(real_time_search_results, search_keywords, log_file_path)
                            else:
                                print(f"\033[31m'{' '.join(search_keywords)}'가 모두 포함된 메모를 찾을 수 없습니다.\033[0m")
                            
                            print()
                            logging.debug("계속 검색하려면 키워드를 입력하세요:")
                            print("Ctrl+U: 입력창 지우기, Ctrl+C: 종료")
                            print("편집: d_pk_logs/ensure_pk_memo_searched.log 파일을 수정하면 자동으로 원본에 적용됩니다")
                            print(f"키워드: {current_input}", end='', flush=True)
        else:
            # Linux/Mac용 입력 처리
            import tty
            import termios
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                while True:
                    char = sys.stdin.read(1)
                    last_input_time = time.time()
                    
                    if char == '\r' or char == '\n':
                        break
                    elif char == '\x7f':
                        if current_input:
                            current_input = current_input[:-1]
                            print('\r' + ' ' * (len(current_input) + 20) + '\r', end='')
                    elif char == '\x15':
                        current_input = ""
                        ensure_console_cleared()
                        logging.debug("개선된 실시간 메모 검색 + 편집 시스템")
                        logging.debug("검색할 키워드를 입력하세요 (실시간으로 검색 결과가 업데이트됩니다): ")
                        logging.debug("Ctrl+U: 입력창 지우기, Ctrl+C: 종료")
                        logging.debug("편집: d_pk_logs/ensure_pk_memo_searched.log 파일을 수정하면 자동으로 원본에 적용됩니다")
                        print()
                        print("키워드: ", end='', flush=True)
                        continue
                    elif char == '\x03':
                        logging.debug("검색이 취소되었습니다.")
                        return
                    else:
                        current_input += char
                    
                    print(f'\r키워드: {current_input}', end='', flush=True)
                    
                    if len(current_input) >= 2:
                        temp_keywords = [kw.strip() for kw in current_input.split() if kw.strip()]
                        if temp_keywords and temp_keywords != last_search_input:
                            print(f'\n\033[33m실시간 검색 중...\033[0m')
                            search_keywords = temp_keywords
                            last_search_input = temp_keywords.copy()
                            
                            ensure_console_cleared()
                            logging.debug("개선된 실시간 메모 검색 + 편집 시스템")
                            logging.debug(f"검색 키워드: {' '.join(search_keywords)}")
                            print()
                            
                            real_time_search_results = perform_search(f_memo, search_keywords)
                            if real_time_search_results:
                                display_search_results(real_time_search_results, search_keywords)
                                
                                if log_file_path:
                                    write_search_results_to_log(real_time_search_results, search_keywords, log_file_path)
                            else:
                                print(f"\033[31m'{' '.join(search_keywords)}'가 모두 포함된 메모를 찾을 수 없습니다.\033[0m")
                            
                            print()
                            logging.debug("계속 검색하려면 키워드를 입력하세요:")
                            print("Ctrl+U: 입력창 지우기, Ctrl+C: 종료")
                            print("편집: d_pk_logs/ensure_pk_memo_searched.log 파일을 수정하면 자동으로 원본에 적용됩니다")
                            print(f"키워드: {current_input}", end='', flush=True)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        # 최종 키워드 설정
        if current_input:
            search_keywords = [kw.strip() for kw in current_input.split() if kw.strip()]
            print(f'\n\033[34;47m최종 입력된 키워드: {" ".join(search_keywords)}\033[0m')
        else:
            logging.debug("키워드가 입력되지 않았습니다.")
            return

    except Exception as e:
        logging.debug(f"키워드 입력 오류: {str(e)}")
        return

    if not search_keywords:
        logging.debug("검색 키워드가 입력되지 않았습니다.")
        return

    # 8. 최종 검색 결과 출력
    ensure_console_cleared()
    print(f'\n\033[32m=== 최종 검색 결과 요약 ===\033[0m')
    final_search_results = perform_search(f_memo, search_keywords)
    if final_search_results:
        display_search_results(final_search_results, search_keywords)
        
        if log_file_path:
            write_search_results_to_log(final_search_results, search_keywords, log_file_path)
    else:
        keyword_str = " ".join(search_keywords)
        logging.debug(f"'{keyword_str}'가 모두 포함된 메모 컨텐츠를 찾을 수 없습니다.")
        return

    # 9. 검색 완료 및 편집 시스템 안내
    keyword_str = " ".join(search_keywords)
    logging.debug(f"검색 완료: '{keyword_str}'가 모두 포함된 메모 컨텐츠 {len(final_search_results)}개를 찾았습니다.")
    
    if log_file_path:
        logging.debug("편집 시스템이 활성화되었습니다.")
        logging.debug(f"검색 결과를 편집하려면 {log_file_path} 파일을 수정하세요.")
        logging.debug("5초 동안 입력이 없으면 자동으로 원본 파일에 변경사항이 적용됩니다.")
        
        # 편집 시스템 활성 상태 유지
        try:
            while True:
                time.sleep(10)
                if file_monitor_thread and not file_monitor_thread.is_alive():
                    logging.debug("파일 모니터링이 중단되었습니다.")
                    break
        except KeyboardInterrupt:
            logging.debug("편집 시스템을 종료합니다.")

if __name__ == "__main__":
    ensure_memo_contents_found_improved()

