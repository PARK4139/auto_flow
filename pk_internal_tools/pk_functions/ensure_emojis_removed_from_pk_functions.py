#!/usr/bin/env python3
"""
pk_functions 폴더 내 모든 파일에서 이모지를 제거하는 함수
"""

import os
import re
from pathlib import Path


def remove_emojis_from_text(text):
    """텍스트에서 이모지를 제거하는 함수"""
    # 이모지 유니코드 범위들을 정의
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "\U00002300-\U000023FF"  # miscellaneous technical
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def process_file(file_path):
    """파일에서 이모지를 제거하고 변경사항을 반환"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        cleaned_content = remove_emojis_from_text(original_content)
        
        if original_content != cleaned_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            return True
        return False
    
    except Exception as e:
        print(f"파일 처리 오류 {file_path}: {e}")
        return False


def ensure_emojis_removed_from_pk_functions():
    """pk_functions 폴더에서 이모지를 제거하는 메인 함수"""
    import logging
    
    pk_functions_dir = Path("pk_external_tools/pk_functions")
    
    if not pk_functions_dir.exists():
        logging.debug(f"디렉토리를 찾을 수 없습니다: {pk_functions_dir}")
        return
    
    logging.debug(f"pk_functions 폴더에서 이모지 제거 시작...")
    
    processed_files = []
    changed_files = []
    
    # .py 파일들만 처리
    for py_file in pk_functions_dir.glob("*.py"):
        if py_file.name.startswith("__"):  # __pycache__ 등 제외
            continue
            
        logging.debug(f"처리 중: {py_file.name}")
        processed_files.append(py_file.name)
        
        if process_file(py_file):
            changed_files.append(py_file.name)
            logging.debug(f"이모지 제거됨: {py_file.name}")
        else:
            logging.debug(f"변경사항 없음: {py_file.name}")
    
    logging.debug(f"작업 완료!")
    logging.debug(f"총 처리된 파일: {len(processed_files)}개")
    logging.debug(f"변경된 파일: {len(changed_files)}개")
    
    if changed_files:
        logging.debug(f"변경된 파일 목록:")
        for file_name in changed_files:
            logging.debug(f"{file_name}")


if __name__ == "__main__":
    ensure_emojis_removed_from_pk_functions()