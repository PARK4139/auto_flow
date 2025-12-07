from enum import Enum, auto


class SetupOpsForEnsureValueCompleted20251130(Enum):
    """
    ensure_value_completed_2025_11_30 함수의 정렬 옵션.
    """
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
    HISTORY = "HISTORY"  # 기본값: 히스토리 순 정렬 (가장 최근 사용된 것이 위로)


class PlayerSelectionMode(Enum):
    """
    재생할 파일 후보를 선택하는 모드를 정의합니다.
    """
    AUTO = "AUTO"    # 자동 선택 (현재 로직 유지)
    MANUAL = "MANUAL" # 수동 선택 (fzf 창으로 사용자 선택)


class SetupOpsForManualMediaFileSelection(Enum):
    """
    수동 미디어 파일 선택 시 전체 경로 또는 파일명만 표시할지 여부 옵션.
    """
    FULL_PATH = "FULL_PATH"
    FILENAME_ONLY = "FILENAME_ONLY"


# 필요에 따라 다른 Enum 정의를 추가할 수 있습니다.


class SetupOpsForPnxReplacement(Enum):
    """
    PNX 이름 및 파일 콘텐츠 교체 기능의 작업 범위를 정의합니다.
    """
    DIRECTORY_NAMES_ONLY = "DIRECTORY_NAMES_ONLY"
    FILE_NAMES_ONLY = "FILE_NAMES_ONLY"
    FILE_CONTENTS_ONLY = "FILE_CONTENTS_ONLY"
    FILE_NAMES_AND_CONTENTS_ONLY = "FILE_NAMES_AND_CONTENTS_ONLY"


class SetupOpsForPnxTextTransformation(Enum):
    """
    PNX 텍스트 교체 시 원본 텍스트에 적용할 변환을 정의합니다.
    """
    NONE = "NONE"
    TO_UPPER = "TO_UPPER"
    TO_LOWER = "TO_LOWER"
    # DE_PREFIX_DOUBLE는 복잡하여 추후 구현 고려


class SetupOpsForPnxTargetScope(Enum):
    """
    PNX 교체 작업의 대상 범위를 정의합니다.
    """
    FULL_PROJECT = "FULL_PROJECT"
    CUSTOM_DIRECTORIES = "CUSTOM_DIRECTORIES"
    SPECIFIC_FILES = "SPECIFIC_FILES"


class SetupOpsForPnxSearchDepth(Enum):
    """
    PNX 검색 깊이를 정의합니다.
    """
    RECURSIVE = "RECURSIVE" # 기본값: 현재처럼 os.walk를 사용하여 재귀적으로 탐색
    SHALLOW = "SHALLOW"     # 얕은 탐색: 현재 디렉토리만 탐색하고 하위 디렉토리로 내려가지 않음
