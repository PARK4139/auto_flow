import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_target_files_classified_by_x():
    try:
        import logging
        import os
        from pathlib import Path

        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.get_extensions_from_d import get_extensions_from_d
        from pk_internal_tools.pk_functions.classify_files_by_delimiter import classify_files_by_delimiter
        from pk_internal_tools.pk_objects.pk_file_extensions import VIDEO_EXTENSIONS_CASE_INSENSITIVE, IMAGE_EXTENSIONS_CASE_INSENSITIVE
        from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS, D_PK_WORKING, D_PK_ROOT

        """Wrapper script to classify files by their EXTENSION into a structured directory."""
        func_n = get_caller_name()

        # n. Get working and base destination directories
        d_working = ensure_value_completed(key_name='작업 폴더', options=[os.getcwd(), D_PK_WORKING, D_PK_ROOT, D_DOWNLOADS], func_n=func_n)
        if not d_working: return

        d_dst = None
        if QC_MODE:
            d_dst = d_working
        else:
            d_dst = ensure_value_completed(key_name='결과 저장 폴더', options=[d_working, D_PK_WORKING, D_PK_ROOT, D_DOWNLOADS], func_n=func_n)
            if not d_dst: return

        # n. Get organization mode from user
        org_mode_key = '정리 방식 (확장자 기준)'
        org_mode_options = ['모든 확장자', '비디오 파일만', '이미지 파일만', '특정 확장자 직접 입력']
        org_mode = ensure_value_completed(key_name=org_mode_key, options=org_mode_options, func_n=func_n)
        if not org_mode: return

        ext_set = set()
        # 3. Determine the set of extensions to process
        if org_mode == '비디오 파일만':
            ext_set = VIDEO_EXTENSIONS_CASE_INSENSITIVE
        elif org_mode == '이미지 파일만':
            ext_set = IMAGE_EXTENSIONS_CASE_INSENSITIVE
        elif org_mode == '특정 확장자 직접 입력':
            ext_input = ensure_value_completed(key_name='확장자 입력', guide_text='정리할 확장자를 입력하세요 (예: .txt)', func_n=func_n)
            if ext_input:
                ext_set = {ext_input if ext_input.startswith('.') else '.' + ext_input}
        else:  # '모든 확장자'
            ext_set = get_extensions_from_d(d_working)

        if not ext_set:
            logging.warning("처리할 확장자가 없습니다. 작업을 건너뜁니다.")
            return

        logging.info(f"총 {len(ext_set)} 종류의 확장자에 대해 정리를 시작합니다.")
        source_dir = Path(d_working)
        all_files_in_dir = [f for f in source_dir.iterdir() if f.is_file()]

        # 4. For each extension, find files and call the generic organizing function
        for ext in ext_set:
            files_to_organize = [str(f) for f in all_files_in_dir if f.suffix.lower() == ext.lower()]

            if not files_to_organize:
                continue

            # Define the destination for this specific extension
            ext_d_dst = Path(d_dst) / ext.lstrip('.').lower()

            logging.info(f"'{ext}' 확장자 처리 중 ({len(files_to_organize)}개) ---")
            classify_files_by_delimiter(source_files=files_to_organize, destination_dir=str(ext_d_dst))

        logging.info("모든 작업이 완료되었습니다.")
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
