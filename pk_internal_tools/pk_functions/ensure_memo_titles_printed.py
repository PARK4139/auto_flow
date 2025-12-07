import ipdb

from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
from pk_internal_tools.pk_functions.ensure_memo_contents_found import ensure_memo_contents_found


def ensure_memo_titles_printed(f):
    import re
    import os
    import json
    from datetime import datetime

    import logging
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pathlib import Path
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made

    f = Path(f)

    if not os.path.exists(f):
        logging.debug(f"파일이 존재하지 않습니다: {f}")
        return

    # 캐시 파일 경로 설정
    cache_dir = os.path.join(os.path.dirname(f), ".memo_cache")
    cache_file = os.path.join(cache_dir, f"memo_titles_cache_{os.path.basename(f)}.json")

    # 파일 정보 가져오기
    file_stat = os.stat(f)
    file_size = file_stat.st_size
    file_mtime = file_stat.st_mtime

    # 캐시 디렉토리 생성
    ensure_pnx_made(pnx=cache_dir, mode='d')

    # 캐시에서 이전 정보 확인
    cache_data = None
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as cache_f:
                cache_data = json.load(cache_f)
        except Exception as e:
            logging.debug(f"캐시 파일 읽기 오류: {str(e)}")

    # 파일 변경 여부 확인
    file_changed = True
    if cache_data:
        cached_size = cache_data.get('file_size')
        cached_mtime = cache_data.get('file_mtime')

        if cached_size == file_size and cached_mtime == file_mtime:
            file_changed = False
            logging.debug("파일이 변경되지 않았습니다. 캐시된 결과를 사용합니다.")

    titles_found = []

    if file_changed:
        logging.debug("파일이 변경되었습니다. 제목을 다시 추출합니다.")

        # 파일을 한 줄씩 읽어가며 처리 (메모리 효율적)
        try:
            with open(file=f, mode='r', encoding=PkEncoding.UTF8.value, errors='ignore') as file_obj:
                line_number = 0
                previous_line = ""

                for line in file_obj:
                    line_number += 1
                    line = line.strip()

                    # 구분선 패턴 (50개 이상의 언더스코어)
                    if re.match(r'^_{50,}$', line):
                        # 이전 줄이 구분선이 아니고, 현재 줄이 구분선이면
                        # 다음 줄이 제목일 가능성이 높음
                        previous_line = line
                        continue

                    # 이전 줄이 구분선이고, 현재 줄이 비어있지 않으면 제목으로 인식
                    if re.match(r'^_{50,}$', previous_line) and line:
                        titles_found.append({
                            'title': line,
                            'line_number': line_number,
                            'separator_line': line_number - 1
                        })

                    previous_line = line

        except Exception as e:
            logging.debug(f"파일 읽기 오류: {str(e)}")
            return

        # 캐시에 결과 저장
        cache_data = {
            'file_size': file_size,
            'file_mtime': file_mtime,
            'titles': titles_found,
            'cached_at': datetime.now().isoformat()
        }

        try:
            with open(cache_file, 'w', encoding='utf-8') as cache_f:
                json.dump(cache_data, cache_f, ensure_ascii=False, indent=2)
            logging.debug("결과가 캐시에 저장되었습니다.")
        except Exception as e:
            logging.debug(f"캐시 저장 오류: {str(e)}")

    else:
        # 캐시에서 제목 정보 가져오기
        titles_found = cache_data.get('titles', [])

    # 제목들을 출력
    if titles_found:
        logging.debug(f"메모 제목 목록 ({len(titles_found)}개)")
        for i, title_info in enumerate(titles_found, 1):
            logging.debug(f"{i}. [줄 {title_info['line_number']}] {title_info['title']}")

        # 캐시 정보 출력
        if not file_changed and cache_data:
            cached_at = cache_data.get('cached_at', '알 수 없음')
            logging.debug(f"캐시된 시간: {cached_at}")
    else:
        logging.debug("메모 제목을 찾을 수 없습니다.")




def search_memo_contents_by_keyword(f, search_keyword=None):
    import os
    import re
    import subprocess
    import logging
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pathlib import Path
    from pk_internal_tools.pk_functions.get_fzf_command import get_fzf_command

    f = Path(f)
    if not os.path.exists(f):
        logging.debug(f"파일이 존재하지 않습니다: {f}")
        return

    # 사용자 입력이 없으면 입력 받기
    if not search_keyword:
        try:
            search_keyword = input("검색할 키워드를 입력하세요: ").strip()
        except Exception as e:
            logging.debug(f"키워드 입력 오류: {str(e)}")
            return
    if not search_keyword:
        logging.debug("검색 키워드가 입력되지 않았습니다.")
        return

    # 결과 저장
    found_contents = []
    current_content = []
    current_start_line = 1
    separator_pattern = r'^_{50,}$'

    try:
        with open(file=f, mode='r', encoding=PkEncoding.UTF8.value, errors='ignore') as file_obj:
            for idx, line in enumerate(file_obj, 1):
                if re.match(separator_pattern, line.strip()):
                    # 구분선이 나오면 이전 컨텐츠 저장
                    if current_content:
                        content_str = ''.join(current_content)
                        if search_keyword in content_str:
                            found_contents.append((current_start_line, content_str))
                        current_content = []
                    current_content.append(line)  # 구분선 포함
                    current_start_line = idx
                else:
                    current_content.append(line)
            # 마지막 컨텐츠도 검사
            if current_content:
                content_str = ''.join(current_content)
                if search_keyword in content_str:
                    found_contents.append((current_start_line, content_str))
    except Exception as e:
        logging.debug(f"파일 읽기 오류: {str(e)}")
        return

    # 결과가 없으면 종료
    if not found_contents:
        logging.debug(f"'{search_keyword}'가 포함된 메모 컨텐츠를 찾을 수 없습니다.")
        return

    # fzf를 사용한 선택 기능
    fzf_cmd = get_fzf_command()
    selected_index = None

    if fzf_cmd:
        try:
            # fzf용 입력 데이터 준비 (줄번호 + 제목 첫 줄)
            fzf_input_lines = []
            for i, (start_line, content) in enumerate(found_contents):
                # 제목 추출 (구분선 다음 첫 번째 줄)
                lines = content.split('\n')
                title = ""
                for line in lines:
                    if line.strip() and not re.match(separator_pattern, line.strip()):
                        title = line.strip()
                        break

                fzf_input_lines.append(f"[{i + 1}] (줄 {start_line}) {title}")

            fzf_input = "\n".join(fzf_input_lines)

            # fzf 실행
            cmd = [fzf_cmd, "--height", "40%", "--layout=reverse", "--border"]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            out, _ = proc.communicate(input=fzf_input)

            if out.strip():
                # 선택된 결과에서 인덱스 추출
                selected_line = out.strip()
                match = re.search(r'\[(\d+)\]', selected_line)
                if match:
                    selected_index = int(match.group(1)) - 1  # 0-based index

        except Exception as e:
            logging.debug(f"fzf 실행 오류: {str(e)}")
            selected_index = None

    # fzf가 없거나 실패한 경우 fallback 선택
    if selected_index is None:
        logging.debug(f"'{search_keyword}'가 포함된 메모 컨텐츠 ({len(found_contents)}개)")
        for i, (start_line, content) in enumerate(found_contents, 1):
            # 제목 추출
            lines = content.split('\n')
            title = ""
            for line in lines:
                if line.strip() and not re.match(separator_pattern, line.strip()):
                    title = line.strip()
                    break

            logging.debug(f"[{i}] (줄 {start_line}) {title}")

        # # fallback 선택
        # try:
        #     choice = input(f"\n보고 싶은 번호를 입력하세요 (1-{len(found_contents)}, Enter로 취소): ").strip()
        #     if choice:
        #         selected_index = int(choice) - 1
        # except (ValueError, IndexError):
        #     logging.debug("잘못된 선택입니다.")
        #     return
    else:
        logging.debug(f"선택됨: {selected_index + 1}번")

    # 선택된 결과 출력
    # if 0 <= selected_index < len(found_contents):
    #     start_line, content = found_contents[selected_index]
    #     logging.debug(f"=== 선택된 메모 컨텐츠 (줄 {start_line})")
    #     logging.debug(content)
    # else:
    #     logging.debug("선택이 취소되었습니다.")
