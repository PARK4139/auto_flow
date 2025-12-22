from enum import Enum
from enum import IntFlag, auto


class PkModesForMVP(Enum):
    AI_COMMIT_MASSAGE_MODE = "ai_commit_massage_mode"
    MANUAL_COMMIT_MASSAGE_MODE = "manual_commit_massage_mode"
    MSP_COMMIT_MASSAGE_MODE = "msp_commit_massage_mode"


class PkModesForDemo(IntFlag):
    REMOTE_TARGET = auto()  # TODO Deprecate


class PkModesForEnsureValueCompleted(Enum):
    """
    ensure_value_completed_2025_12_12 함수의 정렬 옵션.
    """
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
    HISTORY = "HISTORY"  # 기본값: 히스토리 순 정렬 (가장 최근 사용된 것이 위로)

class PkModesForPkLogging(Enum):
    MODE_WITH_FILE_LOGGING = "WITH LOG FILE LOGGING"
    MODE_WITHOUT_FILE_LOGGING = "WITHOUT LOG FILE LOGGING"


class PlayerSelectionMode(Enum):
    """
    재생할 파일 후보를 선택하는 모드를 정의합니다.
    """
    AUTO = "AUTO"  # 자동 선택 (현재 로직 유지)
    MANUAL = "MANUAL"  # 수동 선택 (fzf 창으로 사용자 선택)


class PkModesForManualMediaFileSelection(Enum):
    """
    수동 미디어 파일 선택 시 전체 경로 또는 파일명만 표시할지 여부 옵션.
    """
    FULL_PATH = "FULL_PATH"
    FILENAME_ONLY = "FILENAME_ONLY"


# 필요에 따라 다른 Enum 정의를 추가할 수 있습니다.


class PkModesForPnxReplacement(Enum):
    """
    PNX 이름 및 파일 콘텐츠 교체 기능의 작업 범위를 정의합니다.
    """
    DIRECTORY_NAMES_ONLY = "DIRECTORY_NAMES_ONLY"
    FILE_NAMES_ONLY = "FILE_NAMES_ONLY"
    FILE_CONTENTS_ONLY = "FILE_CONTENTS_ONLY"
    FILE_NAMES_AND_CONTENTS_ONLY = "FILE_NAMES_AND_CONTENTS_ONLY"


class PkModesForPnxTextTransformation(Enum):
    """
    PNX 텍스트 교체 시 원본 텍스트에 적용할 변환을 정의합니다.
    """
    NONE = "NONE"
    TO_UPPER = "TO_UPPER"
    TO_LOWER = "TO_LOWER"
    # DE_PREFIX_DOUBLE는 복잡하여 추후 구현 고려


class PkModesForPnxTargetScope(Enum):
    """
    PNX 교체 작업의 대상 범위를 정의합니다.
    """
    FULL_PROJECT = "FULL_PROJECT"
    CUSTOM_DIRECTORIES = "CUSTOM_DIRECTORIES"
    SPECIFIC_FILES = "SPECIFIC_FILES"


class PkModesForPnxSearchDepth(Enum):
    """
    PNX 검색 깊이를 정의합니다.
    """
    RECURSIVE = "RECURSIVE"  # 기본값: 현재처럼 os.walk를 사용하여 재귀적으로 탐색
    SHALLOW = "SHALLOW"  # 얕은 탐색: 현재 디렉토리만 탐색하고 하위 디렉토리로 내려가지 않음


class PkModesForEnsurePnxBackedUp(Enum):
    """
    ensure_pnx_backed_up 함수에서 백업 모드를 정의합니다.
    """
    LOCAL_BACK_UP = "LOCAL_BACK_UP"
    GIT_HUB_BACK_UP = "GIT_HUB_BACK_UP"


class PkModesForPkEnsurePkSystemStarted(Enum):
    AS_CONVENIENCE_MODE = "AS_CONVENIENCE_MODE"
    AS_FAST_MODE = "AS_FAST_MODE"


class PkModesForSdkManager(Enum):
    CLI = "CLI"
    GUI = "GUI"


class PkModesForGetListFromClass(Enum):
    ALL = "ALL"
    METHOD = "METHOD"
    ATTRIBUTE = "ATTRIBUTE"
    ATTRIBUTE_VALUE = "ATTRIBUTE_VALUE"


class PkModesForEnsureVideoPlayedAtLosslesscut(Enum):
    AS_VOID = "AS_VOID"
    AS_LOOP = "AS_LOOP"
    AS_EVENT = "AS_EVENT"


class PkModesForEnsureSlept(IntFlag):
    NORMAL = auto()
    SILENT = auto()


class PkModesForGetPkInterestingInfo(IntFlag):
    NONE = 0
    DATE = auto()
    TIME = auto()
    DAY_OF_WEEK = auto()
    LOCATION_WEATHER = auto()
    STOCK = auto()
    HELP = auto()
    CONNECTED_DRIVES = auto()
    SCREEN = auto()
    PROJECT = auto()
    OS = auto()
    WINDOW_TITLES = auto()
    PROCESSES = auto()
    TASKLIST = auto()
    WIFI = auto()
    PYTHON_IMPORTS = auto()
    IMAGE_NAMES_INFO = auto()
    AI_IDE_PROCESSES_INFO = auto()
    TOP_CPU_PROCESSES = auto()
    TOP_MEMORY_PROCESSES = auto()
    ALL = DATE | TIME | DAY_OF_WEEK | LOCATION_WEATHER | STOCK | HELP | CONNECTED_DRIVES | SCREEN | PROJECT | OS | WINDOW_TITLES | PROCESSES | TASKLIST | WIFI | PYTHON_IMPORTS | IMAGE_NAMES_INFO | AI_IDE_PROCESSES_INFO | TOP_CPU_PROCESSES | TOP_MEMORY_PROCESSES
    DEFAULT = ALL  # Example default


class PkModesForEnsureTargetFilenameAndFileContentTextReplaced(Enum):
    ONLY_FILENAME = "ONLY_FILENAME"
    ONLY_FILE_CONTENT_TEXT = "ONLY_FILE_CONTENT_TEXT"
    FILENAME_AND_FILECONTENT = "FILENAME_AND_FILECONTENT"


class PkWebSeverManageOps(Enum):
    """
    Operations for managing the pk_web_server on a remote target.
    """
    DEPLOY = "DEPLOY"
    RUN = "RUN"
    STOP = "STOP"
    HEALTH_CHECK = "HEALTH_CHECK"
    TERMINAL = "TERMINAL"
