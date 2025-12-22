"""
    file_name parts and reg patterns to ignore
"""
from typing import List

FILENAME_PARTS_TO_IGNORE: List[str] = [
    # '봵',
    '-seg',
    'SEG-',
]
REGEX_PATTERNS_TO_IGNORE: List[str] = [
    r'^#',  # 파일명이 #으로 시작하는 경우 제외
    # '봵',
    r'\d{2}\.\d{2}\.\d{2}\.\d{3}-\d{2}\.\d{2}\.\d{2}\.\d{3}',
    r'\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}',
]
