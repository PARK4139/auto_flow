import os
from pathlib import Path
import logging
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

def get_f_media_to_load(media_files):
    func_n = get_caller_name()
    
    # Filter out non-existent files before presenting to user
    existing_media_files = [file.strip() for file in media_files if os.path.exists(file.strip())]
    
    if not existing_media_files:
        logging.info("재생할 미디어 파일이 없습니다.")
        return None

    # Use ensure_value_completed to allow user selection via fzf
    selected_file_path = ensure_value_completed(
        key_name="media_file_selection",
        func_n=func_n,
        options=existing_media_files,
        guide_text="재생할 미디어 파일을 선택하세요:"
    )
    
    if selected_file_path:
        logging.debug(f"사용자가 선택한 미디어 파일: {selected_file_path}")
        return selected_file_path
    else:
        logging.info("미디어 파일 선택이 취소되었습니다.")
        return None