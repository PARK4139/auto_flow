from enum import Enum, IntFlag, auto


class SetupOpsForPkEnsurePkSystemStarted(Enum):
    AS_CONVENIENCE_MODE = "AS_CONVENIENCE_MODE"
    AS_FAST_MODE = "AS_FAST_MODE"


class SetupOpsForPkWirelessTargetController(IntFlag):
    INITIALIZE_NONE = 0
    SELF = auto()
    TARGET = auto()
    WSL_DISTRO = auto()
    ALL = SELF | TARGET | WSL_DISTRO


class SetupOpsForSdkManager(Enum):
    CLI = "CLI"
    GUI = "GUI"


class SetupOpsForGetListFromClass(Enum):
    ALL = "ALL"
    METHOD = "METHOD"
    ATTRIBUTE = "ATTRIBUTE"
    ATTRIBUTE_VALUE = "ATTRIBUTE_VALUE"


class SetupOpsForEnsureVideoPlayedAtLosslesscut(Enum):
    AS_VOID = "AS_VOID"
    AS_LOOP = "AS_LOOP"
    AS_EVENT = "AS_EVENT"


class SetupOpsForEnsureSlept(IntFlag):
    NORMAL = auto()
    SILENT = auto()


class SetupOpsForGetPkInterestingInfo(IntFlag):
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
    QC_MODE = auto()
    ALL = DATE | TIME | DAY_OF_WEEK | LOCATION_WEATHER | STOCK | HELP | CONNECTED_DRIVES | SCREEN | PROJECT | OS | WINDOW_TITLES | PROCESSES | TASKLIST | WIFI | PYTHON_IMPORTS | IMAGE_NAMES_INFO | AI_IDE_PROCESSES_INFO | TOP_CPU_PROCESSES | TOP_MEMORY_PROCESSES | QC_MODE
    DEFAULT = ALL # Example default

class SetupOpsForEnsureTargetFilenameAndFileContentTextReplaced(Enum):
    ONLY_FILENAME = "ONLY_FILENAME"
    ONLY_FILE_CONTENT_TEXT = "ONLY_FILE_CONTENT_TEXT"
    FILENAME_AND_FILECONTENT = "FILENAME_AND_FILECONTENT"