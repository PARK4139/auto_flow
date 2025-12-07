import logging
import os
import traceback
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
# Import the new generic function
from pk_internal_tools.pk_functions.classify_files_by_delimiter import classify_files_by_delimiter
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_WORKING, d_pk_root

def ensure_target_files_classified_by_keyword():
    """Wrapper script to classify files by a KEYWORD into a structured directory."""
    func_n = get_caller_name()

    # n. Get working dir, destination dir, and keyword from user
    d_working = ensure_value_completed_2025_10_13_0000(key_name='작업 폴더', options=[os.getcwd(), D_PK_WORKING, d_pk_root, D_DOWNLOADS], func_n=func_n)
    if not d_working: return

    d_dst = ensure_value_completed_2025_10_13_0000(key_name='결과 저장 폴더', options=[d_working, D_PK_WORKING, d_pk_root, D_DOWNLOADS], func_n=func_n)
    if not d_dst: return

    keyword = ensure_value_completed_2025_10_13_0000(key_name='키워드 입력', guide_text='파일 이름에 포함된 분류용 키워드를 입력하세요', func_n=func_n)
    if not keyword: return

    # n. Find all files in d_working that contain the keyword
    source_dir = Path(d_working)
    if not source_dir.is_dir():
        logging.error(f"소스 디렉토리가 존재하지 않습니다: {d_working}")
        return

    files_to_organize = [str(f) for f in source_dir.iterdir() if f.is_file() and keyword in f.name]

    if not files_to_organize:
        logging.warning(f"'{d_working}'에서 '{keyword}' 키워드가 포함된 파일을 찾을 수 없습니다.")
        return

    # 3. Define the destination for this specific keyword
    keyword_d_dst = Path(d_dst) / keyword

    logging.info(f"'{keyword}' 키워드로 찾은 {len(files_to_organize)}개 파일에 대해 정리를 시작합니다.")
    
    # 4. Call the generic organizing function
    classify_files_by_delimiter(source_files=files_to_organize, destination_dir=str(keyword_d_dst))

    logging.info("모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_target_files_classified_by_keyword()
    except Exception as e:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)