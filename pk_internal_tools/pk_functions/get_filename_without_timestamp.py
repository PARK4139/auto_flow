"""
타임스탬프가 포함된 파일명에서 타임스탬프를 제거하여 원본 파일명을 찾는 함수

타임스탬프 패턴: _YYYYMMDD_HHMMSS.xxx 또는 _YYYYMMDD_HHMMSS
"""

import os
import re
from pathlib import Path
from typing import Optional


def get_filename_without_timestamp(timestamped_filename: str, working_dir: str) -> Optional[str]:
    """
    타임스탬프가 포함된 파일명에서 타임스탬프를 제거하여 원본 파일명을 찾습니다.
    
    Args:
        timestamped_filename: 타임스탬프가 포함된 파일명 (예: "file_20231121_143022.mkv")
        working_dir: 작업 디렉토리 경로
        
    Returns:
        Optional[str]: 원본 파일명. 찾을 수 없으면 None 반환
        
    Example:
        >>> get_filename_without_timestamp("video_20231121_143022.mkv", "/path/to/dir")
        "video.mkv"  # 원본 파일이 존재하는 경우
    """
    # 타임스탬프 패턴: _YYYYMMDD_HHMMSS.xxx 또는 _YYYYMMDD_HHMMSS
    timestamp_pattern = r'_\d{8}_\d{6}(\.\d+)?$'
    
    # 타임스탬프 제거
    original_name = re.sub(timestamp_pattern, '', timestamped_filename)
    
    # 원본 파일명이 실제로 존재하는지 확인
    original_path = os.path.join(working_dir, original_name)
    if os.path.exists(original_path):
        return original_name
    
    # 확장자가 다른 경우도 확인 (예: .mkv → .jpg)
    name_without_ext = os.path.splitext(original_name)[0]
    for file in os.listdir(working_dir):
        if file.startswith(name_without_ext) and not re.search(timestamp_pattern, file):
            return file
    
    return None


