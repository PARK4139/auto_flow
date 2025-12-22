
"""
파일 확장자 상수를 정의합니다.
- 기본 확장자 세트는 비공개(_ 접두사)로 관리합니다.
- 대소문자를 구분하지 않는(case-insensitive) 세트를 기본으로 제공합니다.
- 모든 확장자 그룹을 통합한 FILE_EXTENSIONS 딕셔너리를 통해 일관성 있게 접근합니다.
"""

_IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
    '.svg', '.ico', '.raw', '.heic', '.heif', '.tga', '.ppm',
    '.pgm', '.pbm', '.xpm', '.xbm', '.pcx', '.dib', '.jfif'
}

_VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
    '.m4v', '.3gp', '.ogv', '.ts', '.mts', '.m2ts', '.vob',
    '.asf', '.rm', '.rmvb', '.divx', '.xvid', '.h264', '.h265'
}

_AUDIO_EXTENSIONS = {
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a',
    '.opus', '.amr', '.ra', '.mid', '.midi', '.aiff', '.au',
    '.cda', '.wv', '.ape', '.alac', '.dts', '.ac3'
}

_DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages',
    '.tex', '.md', '.markdown', '.html', '.htm', '.xml', '.json',
    '.csv', '.xls', '.xlsx', '.ppt', '.pptx', '.key', '.odp'
}

_ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.lzma',
    '.cab', '.arj', '.ace', '.lha', '.lzh', '.uue', '.xxe',
    '.z', '.lz', '.lz4', '.zstd', '.br'
}

_CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss',
    '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb',
    '.go', '.rs', '.swift', '.kt', '.scala', '.pl', '.sh', '.bat',
    '.ps1', '.vbs', '.sql', '.r', '.m', '.dart', '.lua'
}

_DATA_EXTENSIONS = {
    '.json', '.xml', '.csv', '.sql', '.db', '.sqlite', '.sqlite3',
    '.xlsx', '.xls', '.ods', '.yaml', '.yml', '.toml', '.ini',
    '.cfg', '.conf', '.log', '.dat', '.bin', '.dbf', '.mdb'
}


# --- 대소문자 변환 헬퍼 함수 ---

def get_extensions_with_case_variations(extensions_set):
    """확장자 세트에 대소문자 변형을 추가하여 반환"""
    result = set(extensions_set)
    for ext in extensions_set:
        if ext.startswith('.'):
            result.add(ext.upper())
            result.add(ext[0] + ext[1:].upper())
    return result


# --- 공개: 대소문자 구분 없는 확장자 세트 ---

IMAGE_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_IMAGE_EXTENSIONS)
VIDEO_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_VIDEO_EXTENSIONS)
AUDIO_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_AUDIO_EXTENSIONS)
DOCUMENT_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_DOCUMENT_EXTENSIONS)
ARCHIVE_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_ARCHIVE_EXTENSIONS)
CODE_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_CODE_EXTENSIONS)
DATA_EXTENSIONS_CASE_INSENSITIVE = get_extensions_with_case_variations(_DATA_EXTENSIONS)

# --- 공개: 모든 확장자를 통합한 최종 딕셔너리 ---

PK_FILE_EXTENSIONS = {
    'images': IMAGE_EXTENSIONS_CASE_INSENSITIVE,
    'videos': VIDEO_EXTENSIONS_CASE_INSENSITIVE,
    'audios': AUDIO_EXTENSIONS_CASE_INSENSITIVE,
    'documents': DOCUMENT_EXTENSIONS_CASE_INSENSITIVE,
    'archives': ARCHIVE_EXTENSIONS_CASE_INSENSITIVE,
    'code': CODE_EXTENSIONS_CASE_INSENSITIVE,
    'data': DATA_EXTENSIONS_CASE_INSENSITIVE
}

# 기본 코드 확장자 목록 (fzf 옵션 등에 사용)
ALL_CODE_EXTENSIONS = tuple(sorted(list(_CODE_EXTENSIONS)))
