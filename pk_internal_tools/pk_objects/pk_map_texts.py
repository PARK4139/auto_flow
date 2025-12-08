from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_objects.pk_not_organized import PK_BLANK


class PkTexts:
    RESULT = None
    RENAME = None
    ANSWER = None
    NOT_FOUND = None
    ARE_YOU_WANT_TO_KEEP_GOING = None
    YOUTUBE_PAGE_REQUEST = None
    YOUTUBE_PAGE_MOVING = None
    YOUTUBE_COOKIES_SETUP_FAILED_CONTINUE = None
    YOUTUBE_COOKIES_SET_SUCCESS = None
    YOUTUBE_COOKIES_SET_FAILED = None
    YOUTUBE_COOKIES_COUNT = None
    YES = None
    WSL_RESTART_REQUIRED = None
    WRITE_DONE = None
    WRITE = None
    WRAPPER_IMPORT_SUCCESS = None
    WRAPPER_IMPORT_FAILED = None
    WORK = None
    WINDOWS_SYSTEM_SOUND_TEST = None
    WINDOWS_SOUND_SETTINGS_OPENED = None
    WINDOWS_SAPI_TEST = None
    WINDOWS_SAPI_SUCCESS = None
    WINDOWS_SAPI_FAILED = None
    WINDOWS_REGISTRY_SETUP_SUCCESS = None
    WINDOWS_REGISTRY_SETUP_FAILED = None
    WINDOWS_PERMISSION_PROBLEM_DETECTED = None
    WINDOWS_PERMISSION_CHECK_ERROR = None
    WINDOW_NOT_FOUND_OR_CANNOT_CLOSE = None
    WINDOW_CLOSE_ATTEMPT = None
    WILL_SAVE_AS = None
    WIDE_RANGE_PROGRESS_LIMIT = None
    WHICH_VOICE_BEST = None
    WHICH_TEST_HEARD_SOUND = None
    WHAT_CAN_I_HELP = None
    WEDNESDAY = None
    WAV_TEST_FAILED = None
    WAV_TEST_COMPLETE_FINAL = None
    WAV_TEST_COMPLETE = None
    WAV_TEST = None
    WAV_FILE_PLAYED = None
    WAV_FILE_PLAYBACK_TEST = None
    WAV_FILE_PLAYBACK_FAILED = None
    WAV_FILE_HEARD = None
    WARNING = None
    WAITING = None
    VPC_BIT_PROGRESS = None
    VOLUME_TEST_TEXT = None
    VOLUME_TEST = None
    VOLUME_SUCCESS = None
    VOLUME_SETTINGS_TEST = None
    VOLUME_SETTING_TEST = None
    VOLUME_SETTING = None
    VOLUME_FAILED = None
    VOLUME_BOOST_TEST_FAILED = None
    VOLUME_BOOST_TEST = None
    VOLUME_BOOST_PLAYBACK_COMPLETE = None
    VOLUME_BOOST_HEARD = None
    VOLUME_BOOST_APPLIED = None
    VOLUME_AND_AUDIO_STATUS_CHECK = None
    VOICE_VOLUME = None
    VOICE_TEST_FINAL = None
    VOICE_TEST = None
    VOICE_SUCCESS = None
    VOICE_SPEED = None
    VOICE_SETTINGS_TEST = None
    VOICE_SETTINGS = None
    VOICE_LIST_GET_FAILED = None
    VOICE_LANGUAGE = None
    VOICE_FAILED = None
    VOICE_ERROR = None
    VOICE_CHANGE_TEST_START = None
    VOICE_CHANGE_TEST_COMPLETE = None
    VIDEO_URL_UNAVAILABLE = None
    VIDEO_URL = None
    VIDEO_RELATED_CONTENT_FOUND = None
    VIDEO_PLAYER_NOT_FOUND = None
    VIDEO_PLAYER_FOUND = None
    VIDEO_ID_NOT_DOWNLOADABLE = None
    VIA_HISTORICAL_FILE = None
    VIA_FZF = None
    VERSION_TEST = None
    VERSION_OLD = None
    VERSION_LATEST = None
    VERSION_INFO = None
    VERSION_CHECK_FAILED = None
    VERSION = None
    VENV_TEST_SUCCESS = None
    VENV_TEST_FAILED = None
    VENV_SETUP = None
    VENV_PYTHON_VERSION = None
    VENV_PYTHON_TEST = None
    VENV_PYTHON_NOT_FOUND = None
    VENV_PYTHON_FOUND = None
    VENV_PACKAGE_INSTALL_COMPLETE = None
    VENV_MODULE_TEST = None
    VARIOUS_VOICE_TEST = None
    VARIOUS_TEXT_TEST = None
    UV_VS_PYTHON_PERFORMANCE_COMPARISON_ALT = None
    UV_VS_PYTHON_PERFORMANCE_COMPARISON = None
    UV_INSTALLATION = None
    USER_REQUESTED_EXIT = None
    USER_INTERRUPTED = None
    USER_CANCELLED_EMPTY_COMMIT = None
    USER_CANCELLED_BRANCH_CREATION = None
    USER_AGENT_TEST = None
    USER_AGENT_SUCCESS = None
    USER_AGENT_FAILED = None
    USE_INSTEAD = None
    URL_NOT_ENTERED = None
    URL_MOVEMENT_SUCCESS = None
    UNPROCESSABLE_EXTENSION = None
    UNKNOWN_COMMAND = None
    TUESDAY = None
    TTS_WORKING_NORMALLY = None
    TTS_VOLUME = None
    TTS_TEST = None
    TTS_SPEED_TEST_COMPLETE = None
    TTS_SPEED_IMPROVEMENT_TEST = None
    TTS_SPEED = None
    TTS_SETTINGS = None
    TTS_PRIORITY = None
    TTS_GENERATION_FAILED = None
    TRY_GUIDE = None
    TRUE = None
    TOTAL_EXECUTION_TIME_SECONDS_ALT = None
    TOTAL_EXECUTION_TIME_SECONDS = None
    TOTAL_EXECUTION_TIME = None
    TOTAL_EXCUTION_TIME = None
    TOTAL_DOWNLOAD_COMPLETED = None
    TOTAL = None
    TIMEOUT_5_SECONDS_ALT = None
    TIMEOUT_5_SECONDS = None
    TIME_RESPONSE = None
    TIME_LEFT = None
    TIME = None
    THURSDAY = None
    TESTING_WRAPPER_IMPORT = None
    TESTING = None
    TEST_URL = None
    TEST_TEXT = None
    TEST_SUCCESS = None
    TEST_START = None
    TEST_PASS = None
    TEST_FAILED = None
    TEST_FAIL = None
    TEST_DESCRIPTION_ALT = None
    TEST_DESCRIPTION = None
    TEST_COMPLETE = None
    TEST_CASE = None
    TEST = None
    test = None
    TEMP_FILE_SAVED = None
    TEMP_FILE_DELETED = None
    TEMP_CLEANUP_FAILED = None
    SYSTEM_UPDATE_FAILED = None
    SYSTEM_UPDATE_COMPLETE = None
    SYSTEM_UPDATE = None
    SYSTEM_START_SUCCESS = None
    SYSTEM_START_FAILED = None
    SYSTEM_START_ERROR = None
    SYSTEM_SOUND_PLAYED = None
    SYSTEM_SOUND_HEARD = None
    SYSTEM_SOUND_FAILED = None
    SYSTEM_SETUP_START = None
    SUNDAY = None
    SUMMARY = None
    SUCCESSFULLY_IMPORTED = None
    SUCCESS_TIME_ALT = None
    SUCCESS_TIME = None
    SUCCESS = None
    SUCCEEDED = None
    STOPPED = None
    STEP_FAILED = None
    STEP_COMPLETE = None
    STEP_6 = None
    STEP_5 = None
    STEP_4 = None
    STEP_3 = None
    STEP_2 = None
    STEP_1 = None
    STATUS_WARNING = None
    STATUS_VERIFIED = None
    STATUS_SUCCESS = None
    STATUS_SKIPPED = None
    STATUS_INFO = None
    STATUS_FAILED = None
    STATUS_ERROR = None
    STATUS_CHECKING = None
    STATE = None
    STARTING = None
    STARTED = None
    START_TEST = None
    START = None
    SPLIT_SUMMARY = None
    SPLIT_PLAN = None
    SPLIT = None
    SPEED_TEST = None
    SPEED_SUCCESS = None
    SPEED_SETTINGS_TEST = None
    SPEED_SETTING_TEST = None
    SPEED_SETTING = None
    SPEED_FAILED = None
    SPEED_ERROR = None
    SPEED_ADJUSTMENT = None
    SPECIAL_KEYWORD_CANNOT_BE_EMPTY = None
    SOUND_SETTINGS_OPENED = None
    SOUND_SETTINGS_OPEN_FAILED = None
    SOUND_SETTINGS_FAILED = None
    SOUND_SETTINGS = None
    SKIPPED = None
    SKIP = None
    SIMPLE_BEEP_TEST = None
    SIGNATURE_FAILED = None
    SHUTDOWN = None
    SETTINGS_COMPLETE = None
    SET_VOLUME_TO_100 = None
    SET_VOLUME_SPEED_VOICE_TEST = None
    SET_VOLUME_SPEED_TEST = None
    SET_VOLUME_SPEED_SUCCESS = None
    SET_VOLUME_SPEED_FAILED = None
    SET_VOLUME_SPEED_ERROR = None
    SET_AS_DEFAULT_DEVICE = None
    SET_AS_DEFAULT_COMMUNICATION_DEVICE = None
    SELENIUM_TEST_START = None
    SELENIUM_TEST_FAILED = None
    SELENIUM_NOT_INSTALLED = None
    SELENIUM_DRIVER_DEBUG_MODE = None
    SELENIUM_DIRECT_DOWNLOAD_TEST = None
    SELECT_HEADPHONES = None
    SECONDS = None
    SCROLL_TO_BOTTOM_COMPLETE = None
    SCROLL_TO_BOTTOM = None
    SAVE_COMPLETE = None
    SATURDAY = None
    SATISFIED = None
    SAPI_TEST_SUCCESS = None
    SAPI_TEST_FAILED = None
    SAPI_TEST_ERROR = None
    SAPI_TEST = None
    SAPI_SUCCESS = None
    SAPI_SPEED_TEST_START = None
    SAPI_SPEED_TEST_COMPLETE = None
    SAPI_SPEED_COMPARISON_TEST = None
    SAPI_SPEED_1_5_TEST_SUCCESS = None
    SAPI_SPEED_1_5_TEST_FAILED = None
    SAPI_SPEED_1_5_TEST_ERROR = None
    SAPI_SPEED_1_5_TEST_COMPLETE = None
    SAPI_SPEED_1_5_TEST = None
    SAPI_SPEED_1_0_TEST_SUCCESS = None
    SAPI_SPEED_1_0_TEST_FAILED = None
    SAPI_SPEED_1_0_TEST_ERROR = None
    SAPI_SPEED_1_0_TEST_COMPLETE = None
    SAPI_SPEED_1_0_TEST = None
    SAPI_FAILED = None
    SAPI_ERROR = None
    SAPI_DIRECT_TEST = None
    SAMPLE_TIME_INPUT = None
    REVERTED = None
    REVERT = None
    RETRY = None
    RESPONSE_TIMEOUT = None
    RESPONSE_SIZE = None
    REQUIRED_PACKAGES_INSTALLATION = None
    REQUESTS_TEST_FAILED = None
    REQUESTS_DIRECT_DOWNLOAD_TEST = None
    REQUEST_FAILED = None
    REMOVED = None
    REGISTRY_SETUP_SUCCESS = None
    REGISTRY_SETUP_FAILED = None
    REFERER_TEST = None
    REFERER_SUCCESS = None
    REFERER_FAILED = None
    QUOTA_EXCEEDED = None
    QUITTING = None
    QUIT_MESSAGE = None
    QUIT = None
    QUIET_VOICE_SETTING = None
    QUICK_VOLUME_CHECK = None
    QUICK_SAPI_TEST = None
    QUICK_HYBRID_TEST = None
    PYTTSX3_TEST = None
    PYTTSX3_SUCCESS = None
    PYTTSX3_FAILED = None
    PYTTSX3_DIRECT_TEST_COMPLETE = None
    PYTTSX3_DIRECT_TEST = None
    PROCESS_START = None
    PROCESS_FAILED = None
    PROCESS_COMPLETE = None
    PROCESS = None
    PREVIEW_SUMMARY = None
    PREVIEW_HEADER = None
    PREVIEW_END = None
    PREVIEW = None
    PRESS_ENTER_TO_PROCEED = None
    POTPLAYER_START_FAILED_CONTINUE = None
    POTPLAYER_PLAYLIST_ADDED = None
    POTPLAYER_PLAYLIST_ADD_FAILED_EXCEPTION = None
    POTPLAYER_PLAYLIST_ADD_FAILED = None
    POTPLAYER_COMMAND_FAILED = None
    POSITIVE = None
    PNX_NX_ONLY_ONE_SET = None
    PLAYBACK_FAILED = None
    play = None
    PLAN_TO_MOVE = None
    PLAN = None
    PERMISSION_ERROR = None
    PERFORMING_OPERATION = None
    PERFORMANCE_OPTIMIZATION_TEST_SUCCESS_ALT = None
    PERFORMANCE_OPTIMIZATION_TEST_SUCCESS = None
    PERFORMANCE_OPTIMIZATION_TEST_START_ALT = None
    PERFORMANCE_OPTIMIZATION_TEST_START = None
    PERFORMANCE_OPTIMIZATION_TEST_FAILED_ALT = None
    PERFORMANCE_OPTIMIZATION_TEST_FAILED = None
    PERFORMANCE_OPTIMIZATION_TEST_ERROR_ALT = None
    PERFORMANCE_OPTIMIZATION_TEST_ERROR = None
    PERFORMANCE_OPTIMIZATION_TEST_ALT = None
    PERFORMANCE_COMPARISON_RESULTS_ALT = None
    PERFORMANCE_COMPARISON_RESULTS = None
    PAUSE = None
    PATH_SETUP = None
    PATH_NOT_FOUND = None
    PATH = None
    PAGE_TITLE = None
    PAGE_SIZE = None
    PAGE_REQUEST_SUCCESS = None
    PAGE_REQUEST_FAILED = None
    PAGE_LOADING_FAILED = None
    PAGE_CONTENT_SAVED = None
    PACKAGE_SYNC = None
    PACKAGE_LIST_UPDATE_FAILED = None
    PACKAGE_LIST_UPDATE_COMPLETE = None
    PACKAGE_LIST_UPDATE = None
    PACKAGE_INSTALLING = None
    PACKAGE_INSTALLATION_FAILED = None
    PACKAGE_INSTALLATION_COMPLETE = None
    PACKAGE_INSTALL_SUCCESS = None
    PACKAGE_INSTALL_FAILED = None
    PACKAGE_INSTALL_ERROR = None
    OUTPUT_SETTING = None
    OS_PATH_USER_CLEANED = None
    OS_PATH_CLEAN_FAILED = None
    OS_PATH_CHANGE_NOTIFICATION_SENT = None
    OS_PATH_CHANGE_NOTIFICATION_FAILED = None
    OS_PATH_CHANGE_NOTIFICATION_ERROR = None
    ORIGINAL_AUDIO_LENGTH = None
    ORIGIN = None
    ORGANIZED = None
    OPTIMIZED_FUNCTION_LOADED = None
    OPERATION_SUCCESS = None
    OPERATION_IN_PROGRESS = None
    OPERATION_FAILED = None
    OPENING_WINDOWS_SOUND_SETTINGS = None
    OPENAI_API_KEY_SETUP = None
    OLD_LOG_FILE_DELETED = None
    OK_I_WILL_DO_IT_NOW = None
    NOT_PREPARED_YET = None
    NORMAL_EXIT = None
    NO_WAV_FILE_TO_PLAY = None
    NO_OLD_FILES_TO_DELETE = None
    NO = None
    NEGATIVE = None
    MOVED = None
    MOUSE_MOVEMENT = None
    MONDAY = None
    MODULE_NOT_FOUND = None
    MODE = None
    MILLISECONDS = None
    METADATA_SUCCESS = None
    METADATA_FAILED = None
    METADATA_EXTRACTION_TEST = None
    METADATA_EXTRACTION_FAILED_SKIP = None
    METADATA_EXCEPTION = None
    MASSAGE = None
    LOOP_MODE_N_SECONDS_INTERVAL = None
    LOG_FILE_DELETE_FAILED = None
    LOG_CLEANUP_START = None
    LOG_CLEANUP_ERROR = None
    LOG_CLEANUP_COMPLETE = None
    LOCAL_BACKUP_15_DAYS = None
    LISTED = None
    LINUX_VENV_SETUP = None
    LINUX_VENV_PYTHON_NOT_FOUND = None
    LINUX_VENV_PYTHON_FOUND = None
    LINUX_UV_SYNC_COMPLETE = None
    LINUX_UV_INSTALLATION_COMPLETE = None
    LINUX_UV_INSTALLATION = None
    LINUX_UV_BINARY_ALREADY_INSTALLED = None
    LINUX_UV_ALREADY_INSTALLED = None
    LINUX_SHELL_PATH_SETUP_COMPLETE = None
    LINUX_SHELL_CONFIG_NOT_FOUND = None
    LINUX_PYPROJECT_TOML_OR_ROOT_FOUND = None
    LINUX_PYPROJECT_TOML_FOUND = None
    LINUX_PATH_SETUP_COMPLETE = None
    LINUX_PATH_SETUP = None
    LINUX_PACKAGE_SYNC = None
    LINUX_PACKAGE_INSTALLING = None
    LINUX_PACKAGE_INSTALL_FAILED = None
    LINUX_PACKAGE_INSTALL_COMPLETE = None
    LINUX_FZF_INSTALLATION_COMPLETE = None
    LINUX_FZF_INSTALLATION = None
    LINUX_FZF_BINARY_ALREADY_INSTALLED = None
    LINUX_FZF_ALREADY_INSTALLED = None
    LINUX_ALIAS_SETUP_FAILED = None
    LINUX_ALIAS_SETUP_COMPLETE = None
    LINUX_ALIAS_SETUP = None
    LATEST_WORK_TRACKING = None
    LATEST_STATUS_CSV_SAVE_COMPLETE = None
    LANGUAGE_SETTING = None
    KILL = None
    KEEPING_BROWSER_OPEN = None
    JUST = None
    INTERNET_CONNECTION_REQUIRED = None
    INTERACTIVE = None
    INSTALLATION_VERIFICATION = None
    INSTALLATION_SUCCESS = None
    INSTALLATION_FAILED = None
    INSTALL_SELENIUM = None
    INSTALL_FAILED = None
    INSERTED = None
    INPUT_D_SRC_NOT_EXISTS = None
    INFO_MESSAGE = None
    INFO = None
    INCOMPLETE_DOWNLOAD_COMMAND = None
    IMPORTS_SKIPPED = None
    IMPORTS_INSERTED = None
    IMPORTANT_COOKIES_FOUND = None
    IMPORT_THIRD_PARTY_LIBRARIES = None
    IMPORT_SCRIPT_START = None
    IMPORT_SCRIPT_COMPLETE = None
    IMPORT_FILE_READ_ERROR = None
    IMPORT_FILE_PROCESS_ERROR = None
    IMAGE_FIND = None
    IMAGE_CENTER_CLICK = None
    CONTINUE = None
    I_WANT_TO_DO_NEXT_TIME = None
    HYBRID_TTS_TEST_COMPLETE = None
    HYBRID_TTS_TEST = None
    HYBRID_TTS_FAILED = None
    HYBRID_TTS_DIRECT_CALL = None
    HYBRID_TTS_COMPONENTS_TEST = None
    HYBRID_TEST_FAILED = None
    HIGH_SPEED_TTS_TEST_FAILED = None
    HIGH_SPEED_TTS_TEST_COMPLETE = None
    HIGH_SPEED_TTS_TEST = None
    HIGH_SPEED_PLAYBACK_FAILED = None
    HIGH_SPEED_PLAYBACK_COMPLETE = None
    HIGH_SPEED_AUDIO_PLAYBACK_START = None
    HELP_RESPONSE = None
    HELP_COMMANDS = None
    HELP = None
    HELLO_RESPONSE = None
    HELLO_GREETING = None
    HELLO = None
    HEADPHONE_TTS_FINAL_TEST_COMPLETE = None
    HEADPHONE_TTS_FINAL_CONFIRMATION = None
    HEADPHONE_SOUND_HEARD_NORMAL = None
    HEADPHONE_DEBUGGING_START = None
    HEADPHONE_DEBUGGING_COMPLETE = None
    HEADPHONE_CHECK = None
    HEADPHONE_10_PERCENT_VOLUME_TTS_FINAL_TEST = None
    HEADER = None
    GUIDE = None
    GTTS_TEST = None
    GTTS_SUCCESS = None
    GTTS_FAILED = None
    GOOD_MORNING = None
    GOOD_EVENING = None
    GOOD_AFTERNOON = None
    GIT_WORK_COMPLETE = None
    GIT_PULL_FAILED = None
    GIT_CLONE_FAILED = None
    FZF_PATH_NOT_FOUND = None
    FZF_PATH_FOUND = None
    FZF_OTHER_ERROR = None
    FZF_OS_ERROR = None
    FZF_NOT_FOUND = None
    FZF_NOT_AVAILABLE = None
    FZF_INSTALLATION = None
    FZF_FOUND = None
    FZF_FILE_NOT_FOUND = None
    FZF_EXECUTION_SUCCESS = None
    FZF_EXECUTION_FAILED = None
    FZF_EXE_NOT_FOUND = None
    FZF_EXE_FOUND = None
    FZF_DIAGNOSIS_START = None
    FZF_CORRUPTED_FILE = None
    FZF_AVAILABLE = None
    FUNCTION_TEST_START = None
    FUNCTION_COMPLETED = None
    FULL_EQUIPMENT_STATUS_CSV_SAVE_COMPLETE = None
    FRIDAY = None
    FOUND_WINDOWS = None
    FORMAT_UNAVAILABLE = None
    FORMAT_LIST_CHECK_FAILED = None
    FORMAT_INFO_UNAVAILABLE = None
    FORCE_DOWNLOAD_TEST = None
    FORCE_DOWNLOAD_START = None
    FORCE_DOWNLOAD_FAILED = None
    FORCE_DOWNLOAD_COMPLETE = None
    FOLLOW_THESE_STEPS = None
    FINISHED = None
    FINAL_TTS_CHECK = None
    FINAL_SETTINGS_TEST_START = None
    FINAL_SETTINGS_TEST_COMPLETE = None
    FINAL_SETTINGS_APPLIED_TEST = None
    FINAL_FILE_NOT_FOUND = None
    FINAL_CHECK_COMPLETE = None
    FILES_KEPT = None
    FILES_DELETED = None
    FILE_SIZE = None
    FILE_OPEN_FAILED_WSL = None
    FILE_NOT_FOUND = None
    FILE_GEN_TIME_STABLE_MODE = None
    FILE_COPY_SUCCESS = None
    FILE_COPY_FAILED = None
    FAST_VOICE_SETTING = None
    FALSE = None
    FALLBACK_SYSTEM_TEST_START = None
    FALLBACK_OPTION_TEST = None
    FALLBACK_OPTION_SUCCESS = None
    FALLBACK_OPTION_FAILED = None
    FALLBACK_OPTION_EXCEPTION = None
    FALLBACK_NEEDED = None
    FAILURE_STDERR_ALT = None
    FAILURE_STDERR = None
    FAILURE = None
    FAILED = None
    fail = None
    EXTENSION = None
    EXISTING_WAV_FILE_PLAYBACK = None
    EXECUTION_TIME = None
    EXECUTION = None
    EXCEPTION_OCCURRED = None
    ERROR_PATTERN_DETECTION_TEST = None
    ERROR_OCCURRED_FINAL = None
    ERROR_OCCURRED_ALT = None
    ERROR_OCCURRED = None
    ERROR = None
    ERROR_MASSAGE = None
    EQUIPMENT_QUERIED = None
    ENGINE_SETTING = None
    END = None
    EMPTY_COMMIT_PUSH_FAILED = None
    EMERGENCY_BACKUP = None
    DUPLICATE_FUNCTION = None
    DRY_RUN = None
    DRIVER_GET_TARGET_URL = None
    DOWNLOAD_TEST = None
    DOWNLOAD_SUCCESS = None
    DOWNLOAD_START = None
    DOWNLOAD_RESULT_CHECK = None
    DOWNLOAD_FILE_MOVE_ATTEMPT = None
    DOWNLOAD_FAILED_ALT = None
    DOWNLOAD_FAILED = None
    DOWNLOAD_EXCEPTION = None
    DOWNLOAD_COMPLETE = None
    DONE = None
    DOCKER_SERVICE_START_FAILED = None
    DOCKER_SERVICE_START_COMPLETE = None
    DOCKER_SERVICE_START = None
    DOCKER_REPOSITORY_ADDITION_FAILED = None
    DOCKER_REPOSITORY_ADDITION_COMPLETE = None
    DOCKER_REPOSITORY_ADDITION = None
    DOCKER_INSTALLATION_WSL_UBUNTU = None
    DOCKER_INSTALLATION_VERIFICATION_FAILED = None
    DOCKER_INSTALLATION_VERIFICATION_COMPLETE = None
    DOCKER_INSTALLATION_VERIFICATION = None
    DOCKER_INSTALLATION_SUCCESS = None
    DOCKER_INSTALLATION_ROUTINE_WSL_UBUNTU = None
    DOCKER_INSTALLATION_FAILED_FINAL = None
    DOCKER_INSTALLATION_FAILED = None
    DOCKER_INSTALLATION_COMPLETE_FINAL = None
    DOCKER_INSTALLATION_COMPLETE = None
    DOCKER_INSTALLATION = None
    DOCKER_GPG_KEY_ADDITION_FAILED = None
    DOCKER_GPG_KEY_ADDITION_COMPLETE = None
    DOCKER_GPG_KEY_ADDITION = None
    DOCKER_COMPOSE_INSTALLATION_VERIFICATION_FAILED = None
    DOCKER_COMPOSE_INSTALLATION_VERIFICATION_COMPLETE = None
    DOCKER_COMPOSE_INSTALLATION_VERIFICATION = None
    DOCKER_COMPOSE_INSTALLATION_FAILED = None
    DOCKER_COMPOSE_INSTALLATION_COMPLETE = None
    DOCKER_COMPOSE_INSTALLATION = None
    DISABLE_OTHER_DEVICES = None
    DIRECTORY_CREATION_FAILED = None
    DIRECTORY_CREATED = None
    DIRECT_DOWNLOAD_TEST = None
    DID_YOU_HEAR_SOUND = None
    DETECTED = None
    DEPRECATED_FUNCTION = None
    DELETE = None
    DEFAULT = None
    DEBUG_SEARCH = None
    DEBUG_OUTPUT_FILENAME = None
    DEBUG_OUTPUT = None
    DEBUG_NORMALIZED = None
    DEBUG_METADATA_EXT = None
    DEBUG_METADATA = None
    DEBUG_MESSAGE = None
    DEBUG_INFO = None
    DEBUG_ID = None
    DEBUG_FILE = None
    DEBUG_CALL = None
    DEBUG = None
    DEACTIVATE_VENV = None
    DB = None
    DATE_RESPONSE = None
    DATE = None
    DATA = None
    DAILY_LOCAL_BACKUP = None
    D_pk_UNEXPECTED_ERROR = None
    D_pk_DOCKER_INSTALLATION_SUCCESS = None
    D_pk_DOCKER_INSTALLATION_FAILED = None
    CURRENT_TIME = None
    CURRENT_SETTINGS = None
    CREATED = None
    COPIED = None
    COOKIES_LOADED = None
    COOKIE_FILE_TEST_START = None
    COOKIE_FILE_NOT_FOUND = None
    COOKIE_FILE_MISSING = None
    COOKIE_FILE_EXISTS = None
    CONVERSION_WORK_COMPLETE = None
    CONVERSION_FAILED = None
    CONVERSION_COMPLETE = None
    CONTENTS_PLAYED = None
    CONTAINER_USEFUL_COMMANDS = None
    CONTAINER_TEST_SUCCESS = None
    CONTAINER_TEST_FAILED = None
    CONTAINER_SERVICE_STARTING = None
    CONTAINER_SERVICE_BUILDING = None
    CONTAINER_PROJECT_PATH_CHECK = None
    CONTAINER_DOCKER_STATUS_CHECK = None
    CONTAINER_DATABASE_SERVICE_STARTING = None
    CONTAINER_BUILD_TEST_SUCCESS = None
    COMPRESSION_TARGET_SIZE_WARNING = None
    COMPRESSED = None
    COMPREHENSIVE_TTS_TEST = None
    COMPLETE = None
    COMMENTED_URL_SKIP = None
    COMMANDS = None
    COMMAND_EXECUTION_ALT = None
    COMMAND_EXECUTION = None
    COLORAMA_NOT_INSTALLED = None
    CLIPBOARD_COPY_FAILED = None
    CLEAR_RESPONSE = None
    CLEAR = None
    CLASSIFIED = None
    CHROME_BROWSER_STARTING = None
    CHECKED = None
    CHECK_WHICH_SPEED_BEST = None
    CHECK_ALL_TESTS_HEARD = None
    CHATGPT_UNEXPECTED_ERROR = None
    CHATGPT_RESPONSE_PARSE_FAILED = None
    CHATGPT_RESPONSE_COMPLETE = None
    CHATGPT_CONVERSATION_SAVE_FAILED = None
    CHATGPT_CONVERSATION_LOAD_FAILED = None
    CHATGPT_API_CALL_FAILED = None
    CASHE_USED = None
    CASE_SUCCESS = None
    CASE_FAILED = None
    CALLING_FUNCTION = None
    BROWSER_SCREEN_INITIAL_LOADING = None
    BROWSER_CLOSED = None
    BRANCH_PUSH_FAILED = None
    BRANCH_NOT_IN_REMOTE = None
    BLUETOOTH_HEADPHONE_SPECIALIZED_TEST = None
    BEEP_PLAYED = None
    BEEP_HEARD = None
    BEEP_FAILED = None
    BASIC_VS_FALLBACK_COMPARISON = None
    BASIC_VOICE_SETTING = None
    BASIC_TTS_SPEED_TEST_FAILED = None
    BASIC_TTS_SPEED_TEST_COMPLETE = None
    BASIC_TTS_SPEED_TEST = None
    BASIC_TTS_METHODS_TEST = None
    BASIC_OPTION_TEST = None
    BASIC_OPTION_SUCCESS = None
    BASIC_OPTION_FAILED = None
    BASIC_OPTION_EXCEPTION = None
    BASIC_ENSURE_SPOKEN = None
    BACKUPED = None
    BACKUP_TOTAL_COMPLETE = None
    BACKUP_OS_DETECTED = None
    BACKUP_NO_FILES = None
    BACKUP_FILE_NOT_FOUND = None
    BACKUP_FAILED = None
    BACKUP_DONE = None
    BACKUP_CREATED = None
    BACKUP_COMPLETE = None
    BACKUP = None
    AVAILABLE_VOICES = None
    AVAILABLE_SAPI_VOICES = None
    AVAILABLE_FORMATS_COUNT = None
    AVAILABLE_FORMATS_CHECK = None
    AUTO = None
    AUDIO_WAV_COMPONENTS_START = None
    AUDIO_TIME_EXPRESSION_FAILED = None
    AUDIO_TIME_EXPRESSION_CREATED = None
    AUDIO_TEST_SUCCESS = None
    AUDIO_TEST_FAILED = None
    AUDIO_TEST_ERROR = None
    AUDIO_TEST = None
    AUDIO_SPECIFIC_COMPONENTS_COMPLETE = None
    AUDIO_SOME_COMPONENTS_FAILED = None
    AUDIO_NORMALIZATION_COMPLETE = None
    AUDIO_MISSING_COMPONENTS = None
    AUDIO_ID_NOT_DOWNLOADABLE = None
    AUDIO_DEVICES = None
    AUDIO_DEVICE_SUCCESS = None
    AUDIO_DEVICE_FAILED = None
    AUDIO_DEVICE_CHECK_FAILED = None
    AUDIO_DEVICE_CHECK = None
    AUDIO_COMPONENTS_COMPLETE = None
    AUDIO_COMPONENT_FAILED = None
    AUDIO_COMPONENT_CREATED = None
    AUDIO_ALL_COMPONENTS_EXIST = None
    AUDIO_ALL_COMPONENTS_COMPLETE = None
    ASK = None
    ARE_YOU_SURE_EDIT_DONE = None
    ARCHIVE_CREATED = None
    API_KEY_INPUT = None
    API_ERROR = None
    ALTERNATIVE_TEST_START = None
    ALTERNATIVE_OPTIONS_TEST = None
    ALTERNATIVE_INSTALLATION = None
    ALREADY_EXIST = None
    ALL_TESTS_COMPLETE_ALT = None
    ALL_TESTS_COMPLETE = None
    ALL_STEPS_COMPLETED = None
    ALL_SELENIUM_TESTS_COMPLETE = None
    ALL_ALTERNATIVE_TESTS_COMPLETE = None
    ALIAS_SETUP = None
    ALERT_TIME = None
    ALERT_BLOCKS = None
    ALARM_SETTING_CANCELLED = None
    ALARM_BACKGROUND_RUNNING = None
    AGE_VERIFICATION_BUTTON_NOT_FOUND = None
    AGE_VERIFICATION_BUTTON_FOUND = None
    AGE_VERIFICATION_BUTTON_CLICKED = None
    AGE_RESTRICTED_CONTENT_DETECTED = None
    AGE_RESTRICTED = None
    AFTER_SERVICE = None
    ADD_USER_TO_DOCKER_GROUP_FAILED = None
    ADD_USER_TO_DOCKER_GROUP_COMPLETE = None
    ADD_USER_TO_DOCKER_GROUP = None
    ACTIVATE_VENV = None
    # 창 관리 관련 메시지들
    # 일반적인 메시지들
    # Wrapper import messages
    # Windows system messages
    # WAV playback messages
    # URL navigation messages
    # TTS voice change messages
    # TTS SAPI speed messages
    # TTS quick check messages
    # TTS headphone debug messages
    # TTS final settings messages
    # TTS final check messages
    # TTS and audio test messages
    # Try guide messages
    # System setup and installation messages
    # Step messages
    # Status messages
    # Register fix messages
    # Process and operation messages
    # PotPlayer messages
    # Performance and optimization messages
    # OS path messages
    # Log cleanup related messages
    # Linux system messages
    # Kiri 관련 메시지들
    # Import script messages
    # FZF diagnosis messages
    # Final Bluetooth test messages
    # File operation messages
    # File conversion messages
    # Docker WSL messages
    # Docker installation messages
    # Container build messages
    # Comprehensive TTS test messages
    # Colorama messages
    # ChatGPT messages
    # Backup messages
    # Audio and WAV messages
    # Alert messages
    # Alarm messages
    # Additional system messages

    _localized_texts = {
        # 추가 메시지들
        # 창 관리 관련 메시지들
        # 일반적인 메시지들
        # 예외 관련 메시지들
        # 새로 추가되는 메시지들
        # Wrapper import messages
        # Weekday related messages
        # WAV playback messages
        # TTS 관련 메시지들
        # TTS voice change messages
        # TTS SAPI speed messages
        # TTS quick check messages
        # TTS headphone debug messages
        # TTS final settings messages
        # TTS final check messages
        # TTS and audio test messages
        # Try guide messages
        # System setup and installation messages
        # Step messages
        # Status messages
        # Register fix messages
        # Process and operation messages
        # Performance and optimization messages
        # Log cleanup related messages
        # Final Bluetooth test messages
        # File conversion messages
        # Docker installation messages
        # Deprecation related messages
        # Debug messages
        # Comprehensive TTS test messages
        # Additional system messages

        "YOUTUBE_PAGE_REQUEST": {"korean": "YouTube 페이지 요청", "english": "YouTube page request"},
        "YOUTUBE_PAGE_MOVING": {"korean": "YouTube 페이지 이동", "english": "YouTube page moving"},
        "YOUTUBE_COOKIES_SETUP_FAILED_CONTINUE": {"korean": "YouTube 쿠키 설정 실패, 계속 진행", "english": "YouTube cookies setup failed, continuing"},
        "YOUTUBE_COOKIES_SET_SUCCESS": {"korean": "YouTube 쿠키가 성공적으로 설정되었습니다", "english": "YouTube cookies set successfully"},
        "YOUTUBE_COOKIES_SET_FAILED": {"korean": "YouTube 쿠키 설정에 실패했습니다", "english": "YouTube cookies setting failed"},
        "YOUTUBE_COOKIES_COUNT": {"korean": "YouTube 쿠키 개수", "english": "YouTube cookies count"},
        "WSL_RESTART_REQUIRED": {"korean": "WSL을 재시작한 후 docker 명령어를 사용할 수 있습니다", "english": "WSL restart required to use docker commands"},
        "WRITE": {"korean": "쓰기", "english": "WRITE"},
        "WRITE_DONE": {"korean": "파일 저장 완료", "english": "WRITE DONE"},
        "WRAPPER_IMPORT_SUCCESS": {"korean": "래퍼 import 성공", "english": "Wrapper import success"},
        "WRAPPER_IMPORT_FAILED": {"korean": "래퍼 import 실패", "english": "Wrapper import failed"},
        "WORK": {"korean": "작업", "english": "WORK"},
        "WINDOWS_SYSTEM_SOUND_TEST": {"korean": "Windows 시스템 사운드 테스트", "english": "Windows system sound test"},
        "WINDOWS_SOUND_SETTINGS_OPENED": {"korean": "Windows 소리 설정이 열렸습니다", "english": "Windows sound settings opened"},
        "WINDOWS_SAPI_TEST": {"korean": "Windows SAPI 테스트", "english": "Windows SAPI test"},
        "WINDOWS_SAPI_SUCCESS": {"korean": "Windows SAPI 성공", "english": "Windows SAPI success"},
        "WINDOWS_SAPI_FAILED": {"korean": "Windows SAPI 실패", "english": "Windows SAPI failed"},
        "WINDOWS_REGISTRY_SETUP_SUCCESS": {"korean": "Windows 레지스트리 설정 완료", "english": "Windows registry setup success"},
        "WINDOWS_REGISTRY_SETUP_FAILED": {"korean": "Windows 레지스트리 설정 실패", "english": "Windows registry setup failed"},
        "WINDOW_NOT_FOUND_OR_CANNOT_CLOSE": {"korean": "창을 찾을 수 없거나 닫을 수 없습니다", "english": "Window not found or cannot close"},
        "WINDOW_CLOSE_ATTEMPT": {"korean": "창 닫기 시도", "english": "Window close attempt"},
        "WILL_SAVE_AS": {"korean": "다음 이름으로 저장 예정", "english": "WILL SAVE AS"},
        "WIDE_RANGE_PROGRESS_LIMIT": {"korean": "광범위진행제한", "english": "Wide range progress limit"},
        "WHICH_VOICE_BEST": {"korean": "어떤 음성이 가장 마음에 드시는지 알려주세요", "english": "Please tell me which voice you like best"},
        "WHICH_TEST_HEARD_SOUND": {"korean": "어떤 테스트에서 소리가 들렸는지 알려주세요", "english": "Please tell me which test you heard sound"},
        "WHAT_CAN_I_HELP": {"korean": "무엇을 도와드릴까요?", "english": "What can I help you with?"},
        "WEDNESDAY": {"korean": "수요일", "english": "wednesday"},
        "WAV_TEST": {"korean": "WAV 테스트", "english": "WAV test"},
        "WAV_TEST_FAILED": {"korean": "WAV 테스트 실패", "english": "WAV test failed"},
        "WAV_TEST_COMPLETE": {"korean": "WAV 테스트 완료", "english": "WAV test complete"},
        "WAV_TEST_COMPLETE_FINAL": {"korean": "테스트 완료", "english": "Test complete"},
        "WAV_FILE_PLAYED": {"korean": "WAV 파일 재생됨", "english": "WAV file played"},
        "WAV_FILE_PLAYBACK_TEST": {"korean": "WAV 파일 재생 테스트", "english": "WAV file playback test"},
        "WAV_FILE_PLAYBACK_FAILED": {"korean": "WAV 파일 재생 실패", "english": "WAV file playback failed"},
        "WAV_FILE_HEARD": {"korean": "WAV 파일: 들림/안들림", "english": "WAV file: heard/not heard"},
        "WAITING": {"korean": "대기", "english": "WAITING"},
        "VPC_BIT_PROGRESS": {"korean": "vpc bit 가 진행이 가능합니다", "english": "vpc bit can proceed"},
        "VOLUME_TEST": {"korean": "볼륨 테스트", "english": "Volume test"},
        "VOLUME_TEST_TEXT": {"korean": "테스트", "english": "Test"},
        "VOLUME_SUCCESS": {"korean": "볼륨 성공", "english": "Volume Success"},
        "VOLUME_SETTINGS_TEST": {"korean": "볼륨 설정 테스트", "english": "Volume settings test"},
        "VOLUME_SETTING": {"korean": "볼륨 설정", "english": "Volume"},
        "VOLUME_SETTING_TEST": {"korean": "볼륨 설정 테스트", "english": "Volume setting test"},
        "VOLUME_FAILED": {"korean": "볼륨 실패", "english": "Volume Failed"},
        "VOLUME_BOOST_TEST": {"korean": "볼륨 부스트 테스트", "english": "Volume boost test"},
        "VOLUME_BOOST_TEST_FAILED": {"korean": "볼륨 부스트 테스트 실패", "english": "Volume boost test failed"},
        "VOLUME_BOOST_PLAYBACK_COMPLETE": {"korean": "볼륨 부스트 재생 완료", "english": "Volume boost playback complete"},
        "VOLUME_BOOST_HEARD": {"korean": "볼륨 부스트: 들림/안들림", "english": "Volume boost: heard/not heard"},
        "VOLUME_BOOST_APPLIED": {"korean": "볼륨 부스트 적용됨", "english": "Volume boost applied"},
        "VOLUME_AND_AUDIO_STATUS_CHECK": {"korean": "볼륨 및 오디오 상태 확인", "english": "Volume and audio status check"},
        "VOICE_VOLUME": {"korean": "볼륨", "english": "Volume"},
        "VOICE_TEST": {"korean": "음성 테스트", "english": "Voice test"},
        "VOICE_TEST_FINAL": {"korean": "테스트", "english": "Test"},
        "VOICE_SUCCESS": {"korean": "음성 성공", "english": "Voice success"},
        "VOICE_SPEED": {"korean": "속도", "english": "Speed"},
        "VOICE_SETTINGS": {"korean": "음성 설정", "english": "Voice settings"},
        "VOICE_SETTINGS_TEST": {"korean": "음성 설정 테스트", "english": "Voice settings test"},
        "VOICE_LIST_GET_FAILED": {"korean": "음성 목록 가져오기 실패", "english": "Voice list get failed"},
        "VOICE_LANGUAGE": {"korean": "언어", "english": "Language"},
        "VOICE_FAILED": {"korean": "음성 실패", "english": "Voice failed"},
        "VOICE_ERROR": {"korean": "음성 오류", "english": "Voice error"},
        "VOICE_CHANGE_TEST_START": {"korean": "목소리 변경 테스트 시작", "english": "Voice change test start"},
        "VOICE_CHANGE_TEST_COMPLETE": {"korean": "목소리 변경 테스트 완료", "english": "Voice change test complete"},
        "VIDEO_URL": {"korean": "비디오 URL", "english": "Video URL"},
        "VIDEO_URL_UNAVAILABLE": {"korean": "비디오 URL을 가져올 수 없습니다", "english": "Video URL unavailable"},
        "VIDEO_RELATED_CONTENT_FOUND": {"korean": "비디오 관련 콘텐츠 발견", "english": "Video related content found"},
        "VIDEO_PLAYER_NOT_FOUND": {"korean": "비디오 플레이어를 찾을 수 없습니다", "english": "Video player not found"},
        "VIDEO_PLAYER_FOUND": {"korean": "비디오 플레이어 발견", "english": "Video player found"},
        "VIDEO_ID_NOT_DOWNLOADABLE": {"korean": "다운로드 할 수 있는 video_id가 아닙니다", "english": "Not a downloadable video_id"},
        "VIA_HISTORICAL_FILE": {"korean": "파일 히스토리로 입력", "english": "INPUT VIA HISTORICAL FILE"},
        "VIA_FZF": {"korean": "FZF 로 입력", "english": "INPUT VIA FZF"},
        "VERSION": {"korean": "버전", "english": "Version"},
        "VERSION_TEST": {"korean": "버전 테스트", "english": "Version test"},
        "VERSION_OLD": {"korean": "구버전일 수 있습니다", "english": "May be old version"},
        "VERSION_LATEST": {"korean": "최신 버전입니다", "english": "Latest version"},
        "VERSION_INFO": {"korean": "버전정보", "english": "VERSION INFO"},
        "VERSION_CHECK_FAILED": {"korean": "버전 확인 실패", "english": "Version check failed"},
        "VENV_TEST_SUCCESS": {"korean": "테스트 성공", "english": "Test success"},
        "VENV_TEST_FAILED": {"korean": "테스트 실패", "english": "Test failed"},
        "VENV_SETUP": {"korean": "virtual environment 설정", "english": "Virtual environment setup"},
        "VENV_PYTHON_VERSION": {"korean": "virtual environment Python 버전", "english": "Virtual environment Python version"},
        "VENV_PYTHON_TEST": {"korean": "virtual environment Python 테스트", "english": "Virtual environment Python test"},
        "VENV_PYTHON_NOT_FOUND": {"korean": "virtual environment Python을 찾을 수 없음", "english": "Virtual environment Python not found"},
        "VENV_PYTHON_FOUND": {"korean": "virtual environment Python 사용", "english": "Virtual environment Python found"},
        "VENV_PACKAGE_INSTALL_COMPLETE": {"korean": "virtual environment 패키지 설치 완료", "english": "Virtual environment package install complete"},
        "VENV_MODULE_TEST": {"korean": "모듈 사용 가능", "english": "Module test"},
        "VARIOUS_VOICE_TEST": {"korean": "다양한 음성 테스트", "english": "Various voice test"},
        "VARIOUS_TEXT_TEST": {"korean": "다양한 텍스트 테스트", "english": "Various text test"},
        "UV_VS_PYTHON_PERFORMANCE_COMPARISON": {"korean": "uv vs python 성능 비교", "english": "uv vs python performance comparison"},
        "UV_VS_PYTHON_PERFORMANCE_COMPARISON_ALT": {"korean": "uv vs python 성능 비교", "english": "uv vs python performance comparison"},
        "UV_INSTALLATION": {"korean": "UV 설치", "english": "UV installation"},
        "USER_REQUESTED_EXIT": {"korean": "사용자 요청으로 종료합니다", "english": "Exit by user request"},
        "USER_INTERRUPTED": {"korean": "사용자가 Kiri를 중단했습니다", "english": "User interrupted Kiri"},
        "USER_CANCELLED_EMPTY_COMMIT": {"korean": "사용자가 빈 커밋 생성을 취소했습니다", "english": "User cancelled empty commit creation"},
        "USER_CANCELLED_BRANCH_CREATION": {"korean": "사용자가 브랜치 생성을 취소했습니다", "english": "User cancelled branch creation"},
        "USER_AGENT_TEST": {"korean": "User-Agent 테스트", "english": "User-Agent test"},
        "USER_AGENT_SUCCESS": {"korean": "User-Agent 테스트: 성공", "english": "User-Agent test: success"},
        "USER_AGENT_FAILED": {"korean": "User-Agent 테스트: 실패", "english": "User-Agent test: failed"},
        "USE_INSTEAD": {"korean": "대신 사용하세요", "english": "Use instead"},
        "URL_NOT_ENTERED": {"korean": "URL이 입력되지 않았습니다", "english": "URL not entered"},
        "URL_MOVEMENT_SUCCESS": {"korean": "URL 이동 성공", "english": "URL movement success"},
        "UNPROCESSABLE_EXTENSION": {"korean": "는 처리할 수 없는 확장자입니다", "english": "is an unprocessable extension"},
        "UNKNOWN_COMMAND": {"korean": "명령어를 이해하지 못했습니다", "english": "Unknown command"},
        "TUESDAY": {"korean": "화요일", "english": "tuesday"},
        "TTS_WORKING_NORMALLY": {"korean": "TTS가 정상 작동합니다", "english": "TTS is working normally"},
        "TTS_VOLUME": {"korean": "볼륨", "english": "Volume"},
        "TTS_TEST": {"korean": "테스트", "english": "Test"},
        "TTS_SPEED": {"korean": "속도", "english": "Speed"},
        "TTS_SPEED_TEST_COMPLETE": {"korean": "TTS 속도 테스트 완료", "english": "TTS speed test complete"},
        "TTS_SPEED_IMPROVEMENT_TEST": {"korean": "TTS 속도 개선 테스트", "english": "TTS speed improvement test"},
        "TTS_SETTINGS": {"korean": "설정", "english": "Settings"},
        "TTS_PRIORITY": {"korean": "우선순위", "english": "Priority"},
        "TTS_GENERATION_FAILED": {"korean": "TTS 생성 실패", "english": "TTS generation failed"},
        "TRY_GUIDE": {"korean": "시도 튜토리얼", "english": "Try guide"},
        "TRUE": {"korean": "설정", "english": "TRUE"},
        "TOTAL": {"korean": "총", "english": "TOTAL"},
        "TOTAL_EXECUTION_TIME": {"korean": "총 실행 시간", "english": "Total execution time"},
        "TOTAL_EXECUTION_TIME_SECONDS": {"korean": "총 실행 시간", "english": "Total execution time"},
        "TOTAL_EXECUTION_TIME_SECONDS_ALT": {"korean": "총 실행 시간", "english": "Total execution time"},
        "TOTAL_EXCUTION_TIME": {"korean": "프로그램 실행 시간", "english": "TOTAL EXECUTION TIME"},
        "TOTAL_DOWNLOAD_COMPLETED": {"korean": "전체 다운로드 작업 완료", "english": "Total download work completed"},
        "TIMEOUT_5_SECONDS": {"korean": "타임아웃: 5초 초과", "english": "Timeout: 5 seconds exceeded"},
        "TIMEOUT_5_SECONDS_ALT": {"korean": "타임아웃: 5초 초과", "english": "Timeout: 5 seconds exceeded"},
        "TIME": {"korean": "시간", "english": "Time"},
        "TIME_RESPONSE": {"korean": "현재 시간은", "english": "Current time is"},
        "TIME_LEFT": {"korean": "남은 시간", "english": "TIME LEFT"},
        "THURSDAY": {"korean": "목요일", "english": "thursday"},
        "TESTING": {"korean": "테스트 중", "english": "Testing"},
        "TESTING_WRAPPER_IMPORT": {"korean": "래퍼 import 테스트", "english": "Testing wrapper import"},
        "TEST": {"korean": "테스트", "english": "Test"},
        "test": {"korean": "테스트", "english": "Test"},
        "TEST_URL": {"korean": "테스트 URL", "english": "Test URL"},
        "TEST_TEXT": {"korean": "테스트 텍스트", "english": "Test text"},
        "TEST_SUCCESS": {"korean": "테스트 성공", "english": "Test success"},
        "TEST_START": {"korean": "테스트 시작", "english": "Test Start"},
        "TEST_PASS": {"korean": "테스트 성공", "english": "Test pass"},
        "TEST_FAILED": {"korean": "테스트 실패", "english": "Test failed"},
        "TEST_FAIL": {"korean": "테스트 실패", "english": "Test fail"},
        "TEST_DESCRIPTION": {"korean": "테스트", "english": "Test"},
        "TEST_DESCRIPTION_ALT": {"korean": "테스트", "english": "Test"},
        "TEST_COMPLETE": {"korean": "Kiri 테스트 완료", "english": "Kiri Test Complete"},
        "TEST_CASE": {"korean": "케이스", "english": "Case"},
        "TEMP_FILE_SAVED": {"korean": "임시 파일 저장", "english": "Temporary file saved"},
        "TEMP_FILE_DELETED": {"korean": "임시 파일 삭제됨", "english": "Temporary file deleted"},
        "TEMP_CLEANUP_FAILED": {"korean": "임시 파일 정리 실패", "english": "Temporary cleanup failed"},
        "SYSTEM_UPDATE": {"korean": "시스템 업데이트", "english": "System update"},
        "SYSTEM_UPDATE_FAILED": {"korean": "시스템 업데이트 실패", "english": "System update failed"},
        "SYSTEM_UPDATE_COMPLETE": {"korean": "시스템 업데이트 완료", "english": "System update complete"},
        "SYSTEM_START_SUCCESS": {"korean": "시스템 시작 성공", "english": "System start success"},
        "SYSTEM_START_FAILED": {"korean": "시스템 시작 실패", "english": "System start failed"},
        "SYSTEM_START_ERROR": {"korean": "시스템 시작 오류", "english": "System start error"},
        "SYSTEM_SOUND_PLAYED": {"korean": "시스템 사운드 재생됨", "english": "System sound played"},
        "SYSTEM_SOUND_HEARD": {"korean": "시스템 사운드: 들림/안들림", "english": "System sound: heard/not heard"},
        "SYSTEM_SOUND_FAILED": {"korean": "시스템 사운드 실패", "english": "System sound failed"},
        "SYSTEM_SETUP_START": {"korean": "시스템 설정 시작", "english": "System setup start"},
        "SUNDAY": {"korean": "일요일", "english": "sunday"},
        "SUMMARY": {"korean": "요약", "english": "SUMMARY"},
        "SUCCESSFULLY_IMPORTED": {"korean": "성공적으로 import됨", "english": "Successfully imported"},
        "SUCCESS": {"korean": "성공", "english": "Success"},
        "SUCCESS_TIME": {"korean": "성공", "english": "Success"},
        "SUCCESS_TIME_ALT": {"korean": "성공", "english": "Success"},
        "STOPPED": {"korean": "중지완료", "english": "STOPPED"},
        "STEP_FAILED": {"korean": "단계 실패", "english": "Step failed"},
        "STEP_COMPLETE": {"korean": "단계 완료", "english": "Step complete"},
        "STEP_6": {"korean": "6단계", "english": "Step 6"},
        "STEP_5": {"korean": "5단계", "english": "Step 5"},
        "STEP_4": {"korean": "4단계", "english": "Step 4"},
        "STEP_3": {"korean": "3단계", "english": "Step 3"},
        "STEP_2": {"korean": "2단계", "english": "Step 2"},
        "STEP_1": {"korean": "1단계", "english": "Step 1"},
        "STATUS_WARNING": {"korean": "상태 경고", "english": "Status warning"},
        "STATUS_VERIFIED": {"korean": "상태 확인됨", "english": "Status verified"},
        "STATUS_SUCCESS": {"korean": "상태 성공", "english": "Status success"},
        "STATUS_SKIPPED": {"korean": "상태 건너뜀", "english": "Status skipped"},
        "STATUS_INFO": {"korean": "상태 정보", "english": "Status info"},
        "STATUS_FAILED": {"korean": "상태 실패", "english": "Status failed"},
        "STATUS_ERROR": {"korean": "상태 오류", "english": "Status error"},
        "STATUS_CHECKING": {"korean": "상태 확인 중", "english": "Status checking"},
        "STATE": {"korean": "상태", "english": "STATE"},
        "STARTING": {"korean": "Kiri를 시작합니다", "english": "Starting Kiri"},
        "STARTED": {"korean": "시작", "english": "STARTED"},
        "START": {"korean": "Kiri 시작", "english": "Kiri Start"},
        "START_TEST": {"korean": "Kiri 시작 테스트", "english": "Kiri Start Test"},
        "SPLIT": {"korean": "분할", "english": "SPLIT"},
        "SPLIT_SUMMARY": {"korean": "함수 분할 요약", "english": "SPLIT SUMMARY"},
        "SPLIT_PLAN": {"korean": "분할 계획", "english": "SPLIT PLAN"},
        "SPEED_TEST": {"korean": "속도 테스트", "english": "Speed test"},
        "SPEED_SUCCESS": {"korean": "속도 성공", "english": "Speed success"},
        "SPEED_SETTINGS_TEST": {"korean": "속도 설정 테스트", "english": "Speed settings test"},
        "SPEED_SETTING": {"korean": "속도", "english": "Speed"},
        "SPEED_SETTING_TEST": {"korean": "속도 설정 테스트", "english": "Speed setting test"},
        "SPEED_FAILED": {"korean": "속도 실패", "english": "Speed failed"},
        "SPEED_ERROR": {"korean": "속도 오류", "english": "Speed error"},
        "SPEED_ADJUSTMENT": {"korean": "속도 조절", "english": "Speed adjustment"},
        "SPECIAL_KEYWORD_CANNOT_BE_EMPTY": {"korean": "special_keyword 는 \"\"일 수 없습니다", "english": "special_keyword cannot be empty"},
        "SOUND_SETTINGS": {"korean": "Windows 소리 설정 열기", "english": "Open Windows Sound Settings"},
        "SOUND_SETTINGS_OPENED": {"korean": "Windows 소리 설정이 열렸습니다", "english": "Windows Sound Settings Opened"},
        "SOUND_SETTINGS_OPEN_FAILED": {"korean": "소리 설정 열기 실패", "english": "Sound settings open failed"},
        "SOUND_SETTINGS_FAILED": {"korean": "소리 설정 열기 실패", "english": "Sound Settings Open Failed"},
        "SKIPPED": {"korean": "스킵", "english": "SKIPPED"},
        "SKIP": {"korean": "넘기기", "english": "SKIP"},
        "SIMPLE_BEEP_TEST": {"korean": "간단한 비프음 테스트", "english": "Simple beep test"},
        "SIGNATURE_FAILED": {"korean": "서명 실패", "english": "Signature failed"},
        "SHUTDOWN": {"korean": "종료", "english": "SHUTDOWN"},
        "SETTINGS_COMPLETE": {"korean": "설정 완료", "english": "Settings complete"},
        "SET_VOLUME_TO_100": {"korean": "볼륨을 100%로 설정", "english": "Set volume to 100%"},
        "SET_VOLUME_SPEED_VOICE_TEST": {"korean": "설정된 볼륨/속도로 음성 테스트", "english": "Voice test with set volume/speed"},
        "SET_VOLUME_SPEED_TEST": {"korean": "설정된 볼륨/속도 테스트", "english": "Set volume/speed test"},
        "SET_VOLUME_SPEED_SUCCESS": {"korean": "설정된 볼륨/속도 성공", "english": "Set volume/speed success"},
        "SET_VOLUME_SPEED_FAILED": {"korean": "설정된 볼륨/속도 실패", "english": "Set volume/speed failed"},
        "SET_VOLUME_SPEED_ERROR": {"korean": "설정된 볼륨/속도 오류", "english": "Set volume/speed error"},
        "SET_AS_DEFAULT_DEVICE": {"korean": "기본 장치로 설정", "english": "Set as default device"},
        "SET_AS_DEFAULT_COMMUNICATION_DEVICE": {"korean": "기본 통신 장치로 설정", "english": "Set as default communication device"},
        "SELENIUM_TEST_START": {"korean": "Selenium 테스트 시작", "english": "Selenium test start"},
        "SELENIUM_TEST_FAILED": {"korean": "Selenium 테스트 실패", "english": "Selenium test failed"},
        "SELENIUM_NOT_INSTALLED": {"korean": "Selenium이 설치되지 않았습니다", "english": "Selenium not installed"},
        "SELENIUM_DRIVER_DEBUG_MODE": {"korean": "get_selenium_driver(browser_debug_mode=True) 수행 중", "english": "get_selenium_driver(browser_debug_mode=True) in progress"},
        "SELENIUM_DIRECT_DOWNLOAD_TEST": {"korean": "Selenium 직접 다운로드 테스트", "english": "Selenium direct download test"},
        "SELECT_HEADPHONES": {"korean": "헤드폰 선택", "english": "Select headphones"},
        "SECONDS": {"korean": "초", "english": "SECONDS"},
        "SCROLL_TO_BOTTOM": {"korean": "스크롤 최하단으로 이동 중", "english": "Scroll to bottom"},
        "SCROLL_TO_BOTTOM_COMPLETE": {"korean": "스크롤 최하단으로 이동되었습니다", "english": "Scroll to bottom complete"},
        "SAVE_COMPLETE": {"korean": "저장 완료", "english": "Save complete"},
        "SATURDAY": {"korean": "토요일", "english": "saturday"},
        "SATISFIED": {"korean": "만족된", "english": "SATISFIED"},
        "SAPI_TEST": {"korean": "SAPI 테스트", "english": "SAPI test"},
        "SAPI_TEST_SUCCESS": {"korean": "SAPI 테스트 성공", "english": "SAPI test success"},
        "SAPI_TEST_FAILED": {"korean": "SAPI 테스트 실패", "english": "SAPI test failed"},
        "SAPI_TEST_ERROR": {"korean": "SAPI 테스트 오류", "english": "SAPI test error"},
        "SAPI_SUCCESS": {"korean": "SAPI 성공", "english": "SAPI success"},
        "SAPI_SPEED_TEST_START": {"korean": "SAPI 속도 테스트 시작", "english": "SAPI speed test start"},
        "SAPI_SPEED_TEST_COMPLETE": {"korean": "SAPI 속도 테스트 완료", "english": "SAPI speed test complete"},
        "SAPI_SPEED_COMPARISON_TEST": {"korean": "SAPI 속도 비교 테스트", "english": "SAPI speed comparison test"},
        "SAPI_SPEED_1_5_TEST": {"korean": "SAPI 속도 1.5 테스트", "english": "SAPI speed 1.5 test"},
        "SAPI_SPEED_1_5_TEST_SUCCESS": {"korean": "SAPI 속도 1.5 테스트 성공", "english": "SAPI speed 1.5 test success"},
        "SAPI_SPEED_1_5_TEST_FAILED": {"korean": "SAPI 속도 1.5 테스트 실패", "english": "SAPI speed 1.5 test failed"},
        "SAPI_SPEED_1_5_TEST_ERROR": {"korean": "SAPI 속도 1.5 테스트 오류", "english": "SAPI speed 1.5 test error"},
        "SAPI_SPEED_1_5_TEST_COMPLETE": {"korean": "SAPI 속도 1.5 테스트 완료", "english": "SAPI speed 1.5 test complete"},
        "SAPI_SPEED_1_0_TEST": {"korean": "SAPI 속도 1.0 테스트", "english": "SAPI speed 1.0 test"},
        "SAPI_SPEED_1_0_TEST_SUCCESS": {"korean": "SAPI 속도 1.0 테스트 성공", "english": "SAPI speed 1.0 test success"},
        "SAPI_SPEED_1_0_TEST_FAILED": {"korean": "SAPI 속도 1.0 테스트 실패", "english": "SAPI speed 1.0 test failed"},
        "SAPI_SPEED_1_0_TEST_ERROR": {"korean": "SAPI 속도 1.0 테스트 오류", "english": "SAPI speed 1.0 test error"},
        "SAPI_SPEED_1_0_TEST_COMPLETE": {"korean": "SAPI 속도 1.0 테스트 완료", "english": "SAPI speed 1.0 test complete"},
        "SAPI_FAILED": {"korean": "SAPI 실패", "english": "SAPI failed"},
        "SAPI_ERROR": {"korean": "SAPI 오류", "english": "SAPI error"},
        "SAPI_DIRECT_TEST": {"korean": "SAPI 직접 테스트", "english": "SAPI direct test"},
        "SAMPLE_TIME_INPUT": {"korean": "샘플 설정 시간을 입력해주세요", "english": "Please enter sample time settings"},
        "REVERTED": {"korean": "복구됨", "english": "Reverted"},
        "REVERT": {"korean": "복구(작업전으로)", "english": "REVERT"},
        "RETRY": {"korean": "재시도", "english": "Retry"},
        "RESPONSE_TIMEOUT": {"korean": "시간 초과: 응답이 없어 작업을 건너뜁니다", "english": "Timeout: No response, skipping task"},
        "RESPONSE_SIZE": {"korean": "응답 크기", "english": "Response size"},
        "REQUIRED_PACKAGES_INSTALLATION": {"korean": "필요한 패키지 설치", "english": "Required packages installation"},
        "REQUESTS_TEST_FAILED": {"korean": "requests 테스트 실패", "english": "requests test failed"},
        "REQUESTS_DIRECT_DOWNLOAD_TEST": {"korean": "requests 직접 다운로드 테스트", "english": "requests direct download test"},
        "REQUEST_FAILED": {"korean": "요청 실패", "english": "Request failed"},
        "REMOVED": {"korean": "삭제완료", "english": "REMOVED"},
        "REGISTRY_SETUP_SUCCESS": {"korean": "레지스트리 설정 완료", "english": "Registry setup success"},
        "REGISTRY_SETUP_FAILED": {"korean": "레지스트리 설정 실패", "english": "Registry setup failed"},
        "REFERER_TEST": {"korean": "Referer 테스트", "english": "Referer test"},
        "REFERER_SUCCESS": {"korean": "Referer 테스트: 성공", "english": "Referer test: success"},
        "REFERER_FAILED": {"korean": "Referer 테스트: 실패", "english": "Referer test: failed"},
        "QUOTA_EXCEEDED": {"korean": "한도 초과", "english": "Quota exceeded"},
        "QUITTING": {"korean": "Kiri 종료 중", "english": "Quitting Kiri"},
        "QUIT": {"korean": "종료", "english": "Quit"},
        "QUIT_MESSAGE": {"korean": "Kiri를 종료합니다. 안녕히 가세요", "english": "Shutting down Kiri. Goodbye"},
        "QUIET_VOICE_SETTING": {"korean": "조용한 음성 설정", "english": "Quiet voice setting"},
        "QUICK_VOLUME_CHECK": {"korean": "빠른 볼륨 체크", "english": "Quick volume check"},
        "QUICK_SAPI_TEST": {"korean": "빠른 SAPI 테스트", "english": "Quick SAPI test"},
        "QUICK_HYBRID_TEST": {"korean": "빠른 하이브리드 테스트", "english": "Quick hybrid test"},
        "PYTTSX3_TEST": {"korean": "pyttsx3 테스트", "english": "pyttsx3 test"},
        "PYTTSX3_SUCCESS": {"korean": "pyttsx3 성공", "english": "pyttsx3 success"},
        "PYTTSX3_FAILED": {"korean": "pyttsx3 실패", "english": "pyttsx3 failed"},
        "PYTTSX3_DIRECT_TEST": {"korean": "pyttsx3 직접 테스트", "english": "pyttsx3 direct test"},
        "PYTTSX3_DIRECT_TEST_COMPLETE": {"korean": "pyttsx3 직접 테스트 완료", "english": "pyttsx3 direct test complete"},
        "PROCESS": {"korean": "프로세스", "english": "PROCESS"},
        "PROCESS_START": {"korean": "프로세스 시작", "english": "Process start"},
        "PROCESS_FAILED": {"korean": "프로세스 실패", "english": "Process failed"},
        "PROCESS_COMPLETE": {"korean": "프로세스 완료", "english": "Process complete"},
        "PREVIEW": {"korean": "미리보기", "english": "PREVIEW"},
        "PREVIEW_SUMMARY": {"korean": "미리보기 요약", "english": "PREVIEW SUMMARY"},
        "PREVIEW_HEADER": {"korean": "미리보기 대상 파일", "english": "PREVIEW HEADER"},
        "PREVIEW_END": {"korean": "미리보기 종료", "english": "PREVIEW END"},
        "PRESS_ENTER_TO_PROCEED": {"korean": "진행하려면 Enter 를 누르세요", "english": "Press Enter to proceed"},
        "POTPLAYER_START_FAILED_CONTINUE": {"korean": "PotPlayer 시작 실패, 계속 진행", "english": "PotPlayer start failed, continuing"},
        "POTPLAYER_PLAYLIST_ADDED": {"korean": "PotPlayer 재생목록에 추가됨", "english": "PotPlayer playlist added"},
        "POTPLAYER_PLAYLIST_ADD_FAILED": {"korean": "PotPlayer 재생목록 추가 실패", "english": "PotPlayer playlist add failed"},
        "POTPLAYER_PLAYLIST_ADD_FAILED_EXCEPTION": {"korean": "PotPlayer 재생목록 추가 실패", "english": "PotPlayer playlist add failed"},
        "POTPLAYER_COMMAND_FAILED": {"korean": "PotPlayer 명령 실패", "english": "PotPlayer command failed"},
        "POSITIVE": {"korean": "네", "english": "Yes"},
        "PNX_NX_ONLY_ONE_SET": {"korean": "해당 함수는 pnx nx 둘 중 하나만 설정되어야합니다", "english": "This function should have only one of pnx or nx set"},
        "PLAYBACK_FAILED": {"korean": "재생 실패", "english": "Playback failed"},
        "play": {"korean": "재생", "english": "Play"},
        "PLAN": {"korean": "계획", "english": "PLAN"},
        "PERMISSION_ERROR": {"korean": "권한 오류", "english": "Permission error"},
        "PERFORMING_OPERATION": {"korean": "를 수행합니다", "english": "Performing operation"},
        "PERFORMANCE_OPTIMIZATION_TEST_SUCCESS": {"korean": "성능 최적화 테스트 성공", "english": "Performance optimization test success"},
        "PERFORMANCE_OPTIMIZATION_TEST_SUCCESS_ALT": {"korean": "성능 최적화 테스트 성공", "english": "Performance optimization test success"},
        "PERFORMANCE_OPTIMIZATION_TEST_START": {"korean": "성능 최적화 테스트 시작", "english": "Performance optimization test start"},
        "PERFORMANCE_OPTIMIZATION_TEST_START_ALT": {"korean": "성능 최적화 테스트 시작", "english": "Performance optimization test start"},
        "PERFORMANCE_OPTIMIZATION_TEST_FAILED": {"korean": "성능 최적화 테스트 실패", "english": "Performance optimization test failed"},
        "PERFORMANCE_OPTIMIZATION_TEST_FAILED_ALT": {"korean": "성능 최적화 테스트 실패", "english": "Performance optimization test failed"},
        "PERFORMANCE_OPTIMIZATION_TEST_ERROR": {"korean": "성능 최적화 테스트 오류", "english": "Performance optimization test error"},
        "PERFORMANCE_OPTIMIZATION_TEST_ERROR_ALT": {"korean": "성능 최적화 테스트 오류", "english": "Performance optimization test error"},
        "PERFORMANCE_OPTIMIZATION_TEST_ALT": {"korean": "성능 최적화 테스트", "english": "Performance optimization test"},
        "PERFORMANCE_COMPARISON_RESULTS": {"korean": "성능 비교 결과", "english": "Performance comparison results"},
        "PERFORMANCE_COMPARISON_RESULTS_ALT": {"korean": "성능 비교 결과", "english": "Performance comparison results"},
        "PAUSE": {"korean": "잠시 멈춤", "english": "Pause"},
        "PATH": {"korean": "경로", "english": "Path"},
        "PATH_SETUP": {"korean": "PATH 설정", "english": "PATH setup"},
        "PATH_NOT_FOUND": {"korean": "경로를 찾을 수 없음", "english": "PATH NOT FOUND"},
        "PAGE_TITLE": {"korean": "페이지 제목", "english": "Page title"},
        "PAGE_SIZE": {"korean": "페이지 크기", "english": "Page size"},
        "PAGE_REQUEST_SUCCESS": {"korean": "페이지 요청 성공", "english": "Page request success"},
        "PAGE_REQUEST_FAILED": {"korean": "페이지 요청 실패", "english": "Page request failed"},
        "PAGE_LOADING_FAILED": {"korean": "페이지 로딩에 실패", "english": "Page loading failed"},
        "PAGE_CONTENT_SAVED": {"korean": "페이지 내용 저장", "english": "Page content saved"},
        "PACKAGE_SYNC": {"korean": "패키지 동기화", "english": "Package sync"},
        "PACKAGE_LIST_UPDATE": {"korean": "패키지 목록 업데이트", "english": "Package list update"},
        "PACKAGE_LIST_UPDATE_FAILED": {"korean": "패키지 목록 업데이트 실패", "english": "Package list update failed"},
        "PACKAGE_LIST_UPDATE_COMPLETE": {"korean": "패키지 목록 업데이트 완료", "english": "Package list update complete"},
        "PACKAGE_INSTALLING": {"korean": "설치 중", "english": "Installing"},
        "PACKAGE_INSTALLATION_FAILED": {"korean": "패키지 설치 실패", "english": "Package installation failed"},
        "PACKAGE_INSTALLATION_COMPLETE": {"korean": "패키지 설치 완료", "english": "Package installation complete"},
        "PACKAGE_INSTALL_SUCCESS": {"korean": "설치 완료", "english": "Package install success"},
        "PACKAGE_INSTALL_FAILED": {"korean": "설치 실패", "english": "Package install failed"},
        "PACKAGE_INSTALL_ERROR": {"korean": "설치 오류", "english": "Package install error"},
        "OUTPUT_SETTING": {"korean": "출력", "english": "Output"},
        "ORIGINAL_AUDIO_LENGTH": {"korean": "원본 오디오 길이", "english": "Original audio length"},
        "ORIGIN": {"korean": "원본", "english": "ORIGIN"},
        "ORGANIZED": {"korean": "정돈완료", "english": "ORGANIZED"},
        "OPTIMIZED_FUNCTION_LOADED": {"korean": "최적화된 함수 로드 완료", "english": "Optimized function loaded"},
        "OPERATION_SUCCESS": {"korean": "작업 성공", "english": "Operation success"},
        "OPERATION_IN_PROGRESS": {"korean": "작업 진행 중", "english": "Operation in progress"},
        "OPERATION_FAILED": {"korean": "작업 실패", "english": "Operation failed"},
        "OPENING_WINDOWS_SOUND_SETTINGS": {"korean": "Windows 소리 설정을 열어드립니다", "english": "Opening Windows sound settings"},
        "OPENAI_API_KEY_SETUP": {"korean": "OpenAI API 키를 환경변수 OPENAI_API_KEY에 설정하세요", "english": "Set OpenAI API key in environment variable OPENAI_API_KEY"},
        "OLD_LOG_FILE_DELETED": {"korean": "오래된 로그 파일 삭제", "english": "Old log file deleted"},
        "OK_I_WILL_DO_IT_NOW": {"korean": "지금할게", "english": "I'll do it now"},
        "NOT_PREPARED_YET": {"korean": "아직 준비되지 않은 서비스입니다   :)", "english": "THIS SERVICE IS NOT READY YET :)"},
        "NORMAL_EXIT": {"korean": "정상 종료됨", "english": "Normal exit"},
        "NO_WAV_FILE_TO_PLAY": {"korean": "재생할 WAV 파일이 없음", "english": "No WAV file to play"},
        "NO_OLD_FILES_TO_DELETE": {"korean": "삭제할 오래된 파일 없음", "english": "No old files to delete"},
        "NEGATIVE": {"korean": "아니오", "english": "No"},
        "MOUSE_MOVEMENT": {"korean": "마우스 움직임", "english": "MOUSE MOVEMENT"},
        "MONDAY": {"korean": "월요일", "english": "monday"},
        "MODULE_NOT_FOUND": {"korean": "모듈을 찾을 수 없습니다", "english": "module not found"},
        "MODE": {"korean": "모드", "english": "MODE"},
        "MILLISECONDS": {"korean": "밀리세컨즈", "english": "MILLISECONDS"},
        "METADATA_SUCCESS": {"korean": "메타데이터 성공", "english": "Metadata success"},
        "METADATA_FAILED": {"korean": "메타데이터 실패", "english": "Metadata failed"},
        "METADATA_EXTRACTION_TEST": {"korean": "메타데이터 추출 테스트", "english": "Metadata extraction test"},
        "METADATA_EXTRACTION_FAILED_SKIP": {"korean": "메타데이터 추출 실패로 건너뜀", "english": "Metadata extraction failed, skipping"},
        "METADATA_EXCEPTION": {"korean": "메타데이터 예외", "english": "Metadata exception"},
        "MASSAGE": {"korean": "메시지", "english": "MASSAGE"},
        "LOOP_MODE_N_SECONDS_INTERVAL": {"korean": "n 초마다 반복되는 루프 모드", "english": "Loop mode triggered every n seconds"},
        "LOG_FILE_DELETE_FAILED": {"korean": "로그 파일 삭제 실패", "english": "Log file delete failed"},
        "LOG_CLEANUP_START": {"korean": "로그 정리 시작", "english": "Log cleanup start"},
        "LOG_CLEANUP_ERROR": {"korean": "로그 정리 중 오류 발생", "english": "Error occurred during log cleanup"},
        "LOG_CLEANUP_COMPLETE": {"korean": "로그 정리 완료", "english": "Log cleanup complete"},
        "LOCAL_BACKUP_15_DAYS": {"korean": "15일 전체 로컬백업", "english": "15-day full local backup"},
        "LISTED": {"korean": "나열된 목록", "english": "LISTED"},
        "LATEST_WORK_TRACKING": {"korean": "최신 업무트래킹 기준으로", "english": "Based on latest work tracking"},
        "LATEST_STATUS_CSV_SAVE_COMPLETE": {"korean": "최신 현황 CSV 저장 완료", "english": "Latest status CSV save complete"},
        "LANGUAGE_SETTING": {"korean": "언어", "english": "Language"},
        "KILL": {"korean": "죽이다", "english": "KILL"},
        "KEEPING_BROWSER_OPEN": {"korean": "브라우저를 열어둡니다", "english": "Keeping browser open"},
        "JUST": {"korean": "그냥", "english": "JUST"},
        "INTERNET_CONNECTION_REQUIRED": {"korean": "인터넷이 연결되어야", "english": "Internet connection required"},
        "INTERACTIVE": {"korean": "상호작용", "english": "INTERACTIVE"},
        "INSTALLATION_VERIFICATION": {"korean": "설치 확인", "english": "Installation verification"},
        "INSTALLATION_SUCCESS": {"korean": "설치 완료", "english": "Installation success"},
        "INSTALLATION_FAILED": {"korean": "설치 실패", "english": "Installation failed"},
        "INSTALL_SELENIUM": {"korean": "설치: pip install selenium", "english": "Install: pip install selenium"},
        "INSTALL_FAILED": {"korean": "설치 실패", "english": "Failed to install"},
        "INSERTED": {"korean": "삽입된", "english": "INSERTED"},
        "INPUT_D_SRC_NOT_EXISTS": {"korean": "입력된 d_src 가 존재하지 않습니다", "english": "Input d_src does not exist"},
        "INCOMPLETE_DOWNLOAD_COMMAND": {"korean": "불완전한 다운로드 명령어가 감지되었습니다", "english": "Incomplete download command detected"},
        "IMPORTS_SKIPPED": {"korean": "이미 import 문 존재하여 건너뜀", "english": "Skipped (imports already exist)"},
        "IMPORTS_INSERTED": {"korean": "import 문 삽입 완료", "english": "Imports inserted"},
        "IMPORTANT_COOKIES_FOUND": {"korean": "찾은 중요 쿠키", "english": "Important cookies found"},
        "IMAGE_FIND": {"korean": "이미지찾기", "english": "Image find"},
        "IMAGE_CENTER_CLICK": {"korean": "이미지중앙좌표클릭", "english": "Image center click"},
        "CONTINUE": {"korean": "계속진행:ENTER", "english": "continue:ENTER"},
        "I_WANT_TO_DO_NEXT_TIME": {"korean": "다음에 할게", "english": "I'll do it next time"},
        "HYBRID_TTS_TEST": {"korean": "하이브리드 TTS 테스트", "english": "Hybrid TTS test"},
        "HYBRID_TTS_TEST_COMPLETE": {"korean": "하이브리드 TTS 테스트 완료", "english": "Hybrid TTS test complete"},
        "HYBRID_TTS_FAILED": {"korean": "하이브리드 TTS 실패", "english": "Hybrid TTS failed"},
        "HYBRID_TTS_DIRECT_CALL": {"korean": "하이브리드 TTS 직접 호출", "english": "Hybrid TTS direct call"},
        "HYBRID_TTS_COMPONENTS_TEST": {"korean": "하이브리드 TTS 구성 요소 테스트", "english": "Hybrid TTS components test"},
        "HYBRID_TEST_FAILED": {"korean": "하이브리드 테스트 실패", "english": "Hybrid test failed"},
        "HIGH_SPEED_TTS_TEST": {"korean": "고속 TTS 테스트", "english": "High speed TTS test"},
        "HIGH_SPEED_TTS_TEST_FAILED": {"korean": "고속 TTS 테스트 실패", "english": "High speed TTS test failed"},
        "HIGH_SPEED_TTS_TEST_COMPLETE": {"korean": "고속 TTS 테스트 완료", "english": "High speed TTS test complete"},
        "HIGH_SPEED_PLAYBACK_FAILED": {"korean": "고속 재생 실패", "english": "High speed playback failed"},
        "HIGH_SPEED_PLAYBACK_COMPLETE": {"korean": "고속 재생 완료", "english": "High speed playback complete"},
        "HIGH_SPEED_AUDIO_PLAYBACK_START": {"korean": "고속 오디오 재생 시작", "english": "High speed audio playback start"},
        "HELP": {"korean": "도움말", "english": "Help"},
        "HELP_RESPONSE": {"korean": "tab을 눌러 명령어 자동완성하고 선택하세요", "english": "Press tab to autocomplete and select commands"},
        "HELP_COMMANDS": {"korean": "Kiri 명령어:", "english": "Kiri Commands:"},
        "HELLO": {"korean": "안녕", "english": "Hello"},
        "HELLO_RESPONSE": {"korean": "안녕하세요!", "english": "Hello!"},
        "HELLO_GREETING": {"korean": "무엇을 도와드릴까요?", "english": "How can I help you?"},
        "HEADPHONE_TTS_FINAL_TEST_COMPLETE": {"korean": "헤드폰 TTS 최종 테스트 완료", "english": "Headphone TTS final test complete"},
        "HEADPHONE_TTS_FINAL_CONFIRMATION": {"korean": "헤드폰 TTS 최종 확인", "english": "Headphone TTS final confirmation"},
        "HEADPHONE_SOUND_HEARD_NORMAL": {"korean": "헤드폰에서 소리가 들렸다면 정상 작동입니다", "english": "If you heard sound from headphones, it's working normally"},
        "HEADPHONE_DEBUGGING_START": {"korean": "헤드폰 디버깅 시작", "english": "Headphone debugging start"},
        "HEADPHONE_DEBUGGING_COMPLETE": {"korean": "헤드폰 디버깅 완료", "english": "Headphone debugging complete"},
        "HEADPHONE_CHECK": {"korean": "헤드폰에서 음성이 들리는지 확인하세요", "english": "Check if you can hear voice from headphones"},
        "HEADPHONE_10_PERCENT_VOLUME_TTS_FINAL_TEST": {"korean": "헤드폰에서 10% 볼륨 TTS 최종 테스트", "english": "Headphone 10% volume TTS final test"},
        "HEADER": {"korean": "헤더", "english": "HEADER"},
        "GTTS_TEST": {"korean": "gTTS 테스트", "english": "gTTS test"},
        "GTTS_SUCCESS": {"korean": "gTTS 성공", "english": "gTTS success"},
        "GTTS_FAILED": {"korean": "gTTS 실패", "english": "gTTS failed"},
        "GOOD_MORNING": {"korean": "좋은 아침입니다", "english": "Good morning, sir"},
        "GOOD_EVENING": {"korean": "좋은 저녁입니다", "english": "Good evening, sir"},
        "GIT_WORK_COMPLETE": {"korean": "Git 작업 완료", "english": "Git work complete"},
        "GIT_PULL_FAILED": {"korean": "Git pull 실패", "english": "Git pull failed"},
        "GIT_CLONE_FAILED": {"korean": "Git clone 실패", "english": "Git clone failed"},
        "FZF_INSTALLATION": {"korean": "FZF 설치", "english": "FZF installation"},
        "FUNCTION_TEST_START": {"korean": "기능 테스트 시작", "english": "Function test start"},
        "FUNCTION_COMPLETED": {"korean": "함수 완료", "english": "Function completed"},
        "FULL_EQUIPMENT_STATUS_CSV_SAVE_COMPLETE": {"korean": "전체 장비현황 CSV 저장 완료", "english": "Full equipment status CSV save complete"},
        "FRIDAY": {"korean": "금요일", "english": "friday"},
        "FOUND_WINDOWS": {"korean": "발견된 창들", "english": "Found windows"},
        "FORMAT_UNAVAILABLE": {"korean": "형식 불가", "english": "Format unavailable"},
        "FORMAT_LIST_CHECK_FAILED": {"korean": "형식 목록 확인 실패", "english": "Format list check failed"},
        "FORMAT_INFO_UNAVAILABLE": {"korean": "형식 정보를 가져올 수 없습니다", "english": "Format info unavailable"},
        "FORCE_DOWNLOAD_TEST": {"korean": "강제 다운로드 테스트", "english": "Force download test"},
        "FORCE_DOWNLOAD_START": {"korean": "강제 다운로드 시작", "english": "Force download start"},
        "FORCE_DOWNLOAD_FAILED": {"korean": "강제 다운로드 실패", "english": "Force download failed"},
        "FORCE_DOWNLOAD_COMPLETE": {"korean": "강제 다운로드 완료", "english": "Force download complete"},
        "FOLLOW_THESE_STEPS": {"korean": "다음 단계를 따라해주세요", "english": "Please follow these steps"},
        "FINISHED": {"korean": "완료됨", "english": "Finished"},
        "FINAL_TTS_CHECK": {"korean": "최종 TTS 확인", "english": "Final TTS check"},
        "FINAL_SETTINGS_TEST_START": {"korean": "최종 설정 테스트 시작", "english": "Final settings test start"},
        "FINAL_SETTINGS_TEST_COMPLETE": {"korean": "최종 설정 테스트 완료", "english": "Final settings test complete"},
        "FINAL_SETTINGS_APPLIED_TEST": {"korean": "최종 설정이 적용된 테스트", "english": "Final settings applied test"},
        "FINAL_FILE_NOT_FOUND": {"korean": "병합된 최종 파일이 존재하지 않음", "english": "Final merged file not found"},
        "FINAL_CHECK_COMPLETE": {"korean": "최종 확인 완료", "english": "Final check complete"},
        "FILES_KEPT": {"korean": "개 파일 보관", "english": "files kept"},
        "FILES_DELETED": {"korean": "개 파일 삭제", "english": "files deleted"},
        "FILE_SIZE": {"korean": "파일 크기", "english": "File size"},
        "FILE_OPEN_FAILED_WSL": {"korean": "파일 열기 실패(WSL)", "english": "File open failed (WSL)"},
        "FILE_NOT_FOUND": {"korean": "파일을 찾을 수 없음", "english": "File not found"},
        "FILE_GEN_TIME_STABLE_MODE": {"korean": "파일 생성 시간이 안정된 경우에만 작동하는 모드", "english": "Mode that activates only when the file's generation time is stable"},
        "FILE_COPY_SUCCESS": {"korean": "파일 복사 성공", "english": "File copy success"},
        "FILE_COPY_FAILED": {"korean": "파일 복사 실패", "english": "File copy failed"},
        "FAST_VOICE_SETTING": {"korean": "빠른 음성 설정", "english": "Fast voice setting"},
        "FALSE": {"korean": "미설정", "english": "FALSE"},
        "FALLBACK_SYSTEM_TEST_START": {"korean": "Fallback 시스템 테스트 시작", "english": "Fallback system test start"},
        "FALLBACK_OPTION_TEST": {"korean": "Fallback 옵션 테스트", "english": "Fallback option test"},
        "FALLBACK_OPTION_SUCCESS": {"korean": "Fallback 옵션: 성공", "english": "Fallback option: success"},
        "FALLBACK_OPTION_FAILED": {"korean": "Fallback 옵션: 실패", "english": "Fallback option: failed"},
        "FALLBACK_OPTION_EXCEPTION": {"korean": "Fallback 옵션: 예외", "english": "Fallback option: exception"},
        "FALLBACK_NEEDED": {"korean": "Fallback 필요", "english": "Fallback needed"},
        "FAILURE": {"korean": "실패", "english": "Failure"},
        "FAILURE_STDERR": {"korean": "실패", "english": "Failure"},
        "FAILURE_STDERR_ALT": {"korean": "실패", "english": "Failure"},
        "FAILED": {"korean": "실패된", "english": "FAILED"},
        "fail": {"korean": "실패", "english": "Fail"},
        "EXTENSION": {"korean": "확장자", "english": "Extension"},
        "EXISTING_WAV_FILE_PLAYBACK": {"korean": "기존 WAV 파일 재생", "english": "Existing WAV file playback"},
        "EXECUTION": {"korean": "실행", "english": "EXECUTION"},
        "EXECUTION_TIME": {"korean": "실행 시간", "english": "Execution time"},
        "EXCEPTION_OCCURRED": {"korean": "예외 발생", "english": "Exception occurred"},
        "EXCEPTION_OCCURRED_S": {"korean": "예외발생 s", "english": "Exception occurred s"},
        "EXCEPTION_OCCURRED_E": {"korean": "예외발생 e", "english": "Exception occurred e"},
        "ERROR_PATTERN_DETECTION_TEST": {"korean": "오류 패턴 감지 테스트", "english": "Error pattern detection test"},
        "ERROR_OCCURRED": {"korean": "오류 발생", "english": "Error occurred"},
        "ERROR_OCCURRED_FINAL": {"korean": "오류 발생", "english": "Error occurred"},
        "ERROR_OCCURRED_ALT": {"korean": "오류", "english": "Error occurred"},
        "ERROR_MASSAGE": {"korean": "에러 메시지", "english": "ERROR MASSAGE"},
        "EQUIPMENT_QUERIED": {"korean": "개 장비 조회됨", "english": "equipment queried"},
        "ENGINE_SETTING": {"korean": "엔진", "english": "Engine"},
        "END": {"korean": "종료", "english": "END"},
        "EMPTY_COMMIT_PUSH_FAILED": {"korean": "빈 커밋 후 푸시도 실패했습니다", "english": "Empty commit push also failed"},
        "EMERGENCY_BACKUP": {"korean": "응급 백업", "english": "EMERGENCY BACKUP"},
        "DUPLICATE_FUNCTION": {"korean": "중복 함수 이름", "english": "DUPLICATE FUNCTION"},
        "DRY_RUN": {"korean": "예행연습", "english": "Dry run"},
        "DRIVER_GET_TARGET_URL": {"korean": "driver.get(target_url) 수행 중", "english": "driver.get(target_url) in progress"},
        "DOWNLOAD_TEST": {"korean": "다운로드 테스트", "english": "Download test"},
        "DOWNLOAD_SUCCESS": {"korean": "다운로드 성공", "english": "Download success"},
        "DOWNLOAD_START": {"korean": "다운로드 시작", "english": "Download start"},
        "DOWNLOAD_RESULT_CHECK": {"korean": "다운로드 결과 확인 중", "english": "Download result check"},
        "DOWNLOAD_FILE_MOVE_ATTEMPT": {"korean": "다운로드 f 이동 시도 중", "english": "Download file move attempt"},
        "DOWNLOAD_FAILED": {"korean": "다운로드 실패", "english": "Download failed"},
        "DOWNLOAD_FAILED_ALT": {"korean": "다운로드 실패", "english": "Download failed"},
        "DOWNLOAD_EXCEPTION": {"korean": "다운로드 예외", "english": "Download exception"},
        "DOWNLOAD_COMPLETE": {"korean": "다운로드 완료", "english": "Download complete"},
        "DONE": {"korean": "완료", "english": "DONE"},
        "DOCKER_SERVICE_START": {"korean": "Docker 서비스 시작", "english": "Docker service start"},
        "DOCKER_SERVICE_START_FAILED": {"korean": "Docker 서비스 시작 실패", "english": "Docker service start failed"},
        "DOCKER_SERVICE_START_COMPLETE": {"korean": "Docker 서비스 시작 완료", "english": "Docker service start complete"},
        "DOCKER_REPOSITORY_ADDITION": {"korean": "Docker 저장소 추가", "english": "Docker repository addition"},
        "DOCKER_REPOSITORY_ADDITION_FAILED": {"korean": "Docker 저장소 추가 실패", "english": "Docker repository addition failed"},
        "DOCKER_REPOSITORY_ADDITION_COMPLETE": {"korean": "Docker 저장소 추가 완료", "english": "Docker repository addition complete"},
        "DOCKER_INSTALLATION": {"korean": "Docker 설치", "english": "Docker installation"},
        "DOCKER_INSTALLATION_WSL_UBUNTU": {"korean": "WSL Ubuntu에 Docker 설치 중", "english": "Installing Docker in WSL Ubuntu"},
        "DOCKER_INSTALLATION_VERIFICATION": {"korean": "Docker 설치 확인", "english": "Docker installation verification"},
        "DOCKER_INSTALLATION_VERIFICATION_FAILED": {"korean": "Docker 설치 확인 실패", "english": "Docker installation verification failed"},
        "DOCKER_INSTALLATION_VERIFICATION_COMPLETE": {"korean": "Docker 설치 확인 완료", "english": "Docker installation verification complete"},
        "DOCKER_INSTALLATION_SUCCESS": {"korean": "Docker 설치 성공", "english": "Docker installation success"},
        "DOCKER_INSTALLATION_FAILED": {"korean": "Docker 설치 실패", "english": "Docker installation failed"},
        "DOCKER_INSTALLATION_FAILED_FINAL": {"korean": "Docker 설치 실패", "english": "Docker installation failed"},
        "DOCKER_INSTALLATION_COMPLETE": {"korean": "Docker 설치 완료", "english": "Docker installation complete"},
        "DOCKER_INSTALLATION_COMPLETE_FINAL": {"korean": "Docker 설치가 완료되었습니다", "english": "Docker installation complete"},
        "DOCKER_GPG_KEY_ADDITION": {"korean": "Docker GPG 키 추가", "english": "Docker GPG key addition"},
        "DOCKER_GPG_KEY_ADDITION_FAILED": {"korean": "Docker GPG 키 추가 실패", "english": "Docker GPG key addition failed"},
        "DOCKER_GPG_KEY_ADDITION_COMPLETE": {"korean": "Docker GPG 키 추가 완료", "english": "Docker GPG key addition complete"},
        "DOCKER_COMPOSE_INSTALLATION": {"korean": "Docker Compose 설치", "english": "Docker Compose installation"},
        "DOCKER_COMPOSE_INSTALLATION_VERIFICATION": {"korean": "Docker Compose 설치 확인", "english": "Docker Compose installation verification"},
        "DOCKER_COMPOSE_INSTALLATION_VERIFICATION_FAILED": {"korean": "Docker Compose 설치 확인 실패", "english": "Docker Compose installation verification failed"},
        "DOCKER_COMPOSE_INSTALLATION_VERIFICATION_COMPLETE": {"korean": "Docker Compose 설치 확인 완료", "english": "Docker Compose installation verification complete"},
        "DOCKER_COMPOSE_INSTALLATION_FAILED": {"korean": "Docker Compose 설치 실패", "english": "Docker Compose installation failed"},
        "DOCKER_COMPOSE_INSTALLATION_COMPLETE": {"korean": "Docker Compose 설치 완료", "english": "Docker Compose installation complete"},
        "DISABLE_OTHER_DEVICES": {"korean": "다른 장치들 비활성화", "english": "Disable other devices"},
        "DIRECTORY_CREATION_FAILED": {"korean": "디렉토리 생성 실패", "english": "Directory creation failed"},
        "DIRECTORY_CREATED": {"korean": "디렉토리 생성됨", "english": "Directory created"},
        "DIRECT_DOWNLOAD_TEST": {"korean": "직접 다운로드 테스트", "english": "Direct download test"},
        "DID_YOU_HEAR_SOUND": {"korean": "위의 테스트에서 소리가 들렸나요?", "english": "Did you hear sound in the above tests?"},
        "DETECTED": {"korean": "감지", "english": "DETECTED"},
        "DEPRECATED_FUNCTION": {"korean": "더 이상 사용되지 않는 함수", "english": "Deprecated function"},
        "DELETE": {"korean": "삭제", "english": "DELETE"},
        "DEFAULT": {"korean": "기본", "english": "DEFAULT"},
        "DEBUGGING_NOTE_S": {"korean": "[Debugging Note] s", "english": "[Debugging Note] s"},
        "DEBUGGING_NOTE_E": {"korean": "[Debugging Note] e", "english": "[Debugging Note] e"},
        "DEBUG_SEARCH": {"korean": "디버그 검색", "english": "Debug search"},
        "DEBUG_OUTPUT": {"korean": "디버그 출력", "english": "Debug output"},
        "DEBUG_OUTPUT_FILENAME": {"korean": "DEBUG: 생성된 output_filename", "english": "DEBUG: Generated output_filename"},
        "DEBUG_NORMALIZED": {"korean": "디버그 정규화", "english": "Debug normalized"},
        "DEBUG_METADATA": {"korean": "디버그 메타데이터", "english": "Debug metadata"},
        "DEBUG_METADATA_EXT": {"korean": "DEBUG: 메타데이터에서 받은 ext", "english": "DEBUG: ext received from metadata"},
        "DEBUG_INFO": {"korean": "디버그 정보", "english": "Debug info"},
        "DEBUG_ID": {"korean": "디버그 ID", "english": "Debug ID"},
        "DEBUG_FILE": {"korean": "디버그 파일", "english": "Debug file"},
        "DEBUG_CALL": {"korean": "디버그 호출", "english": "Debug call"},
        "DEACTIVATE_VENV": {"korean": "virtual environment 비활성화", "english": "Deactivate virtual environment"},
        "DATE": {"korean": "날짜", "english": "Date"},
        "DATE_RESPONSE": {"korean": "오늘은", "english": "Today is"},
        "DATA": {"korean": "데이터", "english": "DATA"},
        "DAILY_LOCAL_BACKUP": {"korean": "데일리 로컬백업", "english": "Daily local backup"},
        "CURRENT_TIME": {"korean": "현재 시간은", "english": "Current time is"},
        "CURRENT_SETTINGS": {"korean": "현재 설정", "english": "Current settings"},
        "CREATED": {"korean": "생성", "english": "CREATED"},
        "COPIED": {"korean": "복사된", "english": "COPIED"},
        "COOKIES_LOADED": {"korean": "쿠키 로드됨", "english": "Cookies loaded"},
        "COOKIE_FILE_TEST_START": {"korean": "쿠키 파일 테스트 시작", "english": "Cookie file test start"},
        "COOKIE_FILE_NOT_FOUND": {"korean": "쿠키 파일이 없습니다", "english": "Cookie file not found"},
        "COOKIE_FILE_MISSING": {"korean": "쿠키 파일이 없습니다", "english": "Cookie file missing"},
        "COOKIE_FILE_EXISTS": {"korean": "쿠키 파일 존재", "english": "Cookie file exists"},
        "CONVERSION_WORK_COMPLETE": {"korean": "변환 작업 완료", "english": "Conversion work complete"},
        "CONVERSION_FAILED": {"korean": "변환 실패", "english": "Conversion failed"},
        "CONVERSION_COMPLETE": {"korean": "변환 완료", "english": "Conversion complete"},
        "CONTENTS_PLAYED": {"korean": "콘텐츠 재생", "english": "Contents played"},
        "COMPRESSION_TARGET_SIZE_WARNING": {"korean": "압축대상의 용량이 1GB 이상이면 1분 이상 걸릴 수 있습니다", "english": "If compression target size is over 1GB, it may take more than 1 minute"},
        "COMPRESSED": {"korean": "압축됨", "english": "COMPRESSED"},
        "COMPREHENSIVE_TTS_TEST": {"korean": "종합 TTS 테스트", "english": "Comprehensive TTS test"},
        "COMPLETE": {"korean": "완료", "english": "COMPLETE"},
        "COMMENTED_URL_SKIP": {"korean": "주석 처리된 URL, 건너뜀", "english": "Commented URL, skipping"},
        "COMMANDS": {"korean": "명령어", "english": "Commands"},
        "COMMAND_EXECUTION": {"korean": "명령 실행", "english": "Command execution"},
        "COMMAND_EXECUTION_ALT": {"korean": "명령어", "english": "Command"},
        "COLORAMA_NOT_INSTALLED": {"korean": "colorama 라이브러리가 설치되어 있지 않습니다", "english": "colorama library not installed"},
        "CLIPBOARD_COPY_FAILED": {"korean": "클립보드 복사 실패", "english": "Clipboard copy failed"},
        "CLEAR": {"korean": "클리어", "english": "Clear"},
        "CLEAR_RESPONSE": {"korean": "화면을 정리했습니다", "english": "Screen cleared"},
        "CLASSIFIED": {"korean": "분류완료", "english": "CLASSIFIED"},
        "CHROME_BROWSER_STARTING": {"korean": "Chrome 브라우저 시작 중", "english": "Chrome browser starting"},
        "CHECKED": {"korean": "확인", "english": "CHECKED"},
        "CHECK_WHICH_SPEED_BEST": {"korean": "어떤 속도가 가장 적당한지 확인해주세요", "english": "Please check which speed is best"},
        "CHECK_ALL_TESTS_HEARD": {"korean": "모든 테스트가 정상적으로 들렸는지 확인해주세요", "english": "Please check if all tests were heard normally"},
        "CASHE_USED": {"korean": "캐시 사용된", "english": "CASHE_USED".replace("_", "")},
        "CASE_SUCCESS": {"korean": "케이스 성공", "english": "Case success"},
        "CASE_FAILED": {"korean": "케이스 실패", "english": "Case failed"},
        "CALLING_FUNCTION": {"korean": "함수 호출 중", "english": "Calling function"},
        "BROWSER_SCREEN_INITIAL_LOADING": {"korean": "자동제어 브라우저 화면 초기 로딩 중", "english": "Auto-control browser screen initial loading"},
        "BROWSER_CLOSED": {"korean": "브라우저 종료", "english": "Browser closed"},
        "BRANCH_PUSH_FAILED": {"korean": "브랜치 푸시 실패", "english": "Branch push failed"},
        "BRANCH_NOT_IN_REMOTE": {"korean": "브랜치가 원격 레포지토리에 없습니다", "english": "Branch not in remote repository"},
        "BLUETOOTH_HEADPHONE_SPECIALIZED_TEST": {"korean": "블루투스 헤드폰 특화 테스트", "english": "Bluetooth headphone specialized test"},
        "BEEP_PLAYED": {"korean": "비프음 재생됨", "english": "Beep played"},
        "BEEP_HEARD": {"korean": "비프음: 들림/안들림", "english": "Beep: heard/not heard"},
        "BEEP_FAILED": {"korean": "비프음 실패", "english": "Beep failed"},
        "BASIC_VS_FALLBACK_COMPARISON": {"korean": "기본 vs Fallback 비교", "english": "Basic vs Fallback comparison"},
        "BASIC_VOICE_SETTING": {"korean": "기본 음성 설정", "english": "Basic voice setting"},
        "BASIC_TTS_SPEED_TEST": {"korean": "기본 TTS 속도 테스트", "english": "Basic TTS speed test"},
        "BASIC_TTS_SPEED_TEST_FAILED": {"korean": "기본 TTS 속도 테스트 실패", "english": "Basic TTS speed test failed"},
        "BASIC_TTS_SPEED_TEST_COMPLETE": {"korean": "기본 TTS 속도 테스트 완료", "english": "Basic TTS speed test complete"},
        "BASIC_TTS_METHODS_TEST": {"korean": "기본 TTS 방법들 테스트", "english": "Basic TTS methods test"},
        "BASIC_OPTION_TEST": {"korean": "기본 옵션 테스트", "english": "Basic option test"},
        "BASIC_OPTION_SUCCESS": {"korean": "기본 옵션: 성공", "english": "Basic option: success"},
        "BASIC_OPTION_FAILED": {"korean": "기본 옵션: 실패", "english": "Basic option: failed"},
        "BASIC_OPTION_EXCEPTION": {"korean": "기본 옵션: 예외", "english": "Basic option: exception"},
        "BASIC_ENSURE_SPOKEN": {"korean": "기본 ensure_spoken", "english": "Basic ensure_spoken"},
        "BACKUPED": {"korean": "백업완료", "english": "BACKUPED"},
        "BACKUP": {"korean": "백업", "english": "BACKUP"},
        "BACKUP_FAILED": {"korean": "백업 실패", "english": "Backup failed"},
        "BACKUP_DONE": {"korean": "백업 완료", "english": "BACKUP DONE"},
        "BACKUP_CREATED": {"korean": "백업 생성됨", "english": "Backup created"},
        "AVAILABLE_VOICES": {"korean": "사용 가능한 음성", "english": "Available voices"},
        "AVAILABLE_SAPI_VOICES": {"korean": "사용 가능한 SAPI 음성 목록", "english": "Available SAPI voices"},
        "AVAILABLE_FORMATS_COUNT": {"korean": "사용 가능한 형식 개수", "english": "Available formats count"},
        "AVAILABLE_FORMATS_CHECK": {"korean": "사용 가능한 형식 목록 확인", "english": "Available formats check"},
        "AUTO": {"korean": "자동", "english": "Auto"},
        "AUDIO_TEST": {"korean": "Kiri 음성 테스트", "english": "Kiri Audio Test"},
        "AUDIO_TEST_SUCCESS": {"korean": "Kiri 음성 테스트 성공", "english": "Kiri Audio Test Success"},
        "AUDIO_TEST_FAILED": {"korean": "Kiri 음성 테스트 실패", "english": "Kiri Audio Test Failed"},
        "AUDIO_TEST_ERROR": {"korean": "Kiri 음성 테스트 오류", "english": "Kiri Audio Test Error"},
        "AUDIO_NORMALIZATION_COMPLETE": {"korean": "오디오 정규화 완료", "english": "Audio normalization complete"},
        "AUDIO_ID_NOT_DOWNLOADABLE": {"korean": "다운로드 할 수 있는 audio_id가 아닙니다", "english": "Not a downloadable audio_id"},
        "AUDIO_DEVICES": {"korean": "오디오 장치", "english": "Audio devices"},
        "AUDIO_DEVICE_SUCCESS": {"korean": "오디오 디바이스", "english": "Audio Device"},
        "AUDIO_DEVICE_FAILED": {"korean": "오디오 디바이스 확인 실패", "english": "Audio Device Check Failed"},
        "AUDIO_DEVICE_CHECK": {"korean": "오디오 장치 확인", "english": "Audio device check"},
        "AUDIO_DEVICE_CHECK_FAILED": {"korean": "오디오 장치 확인 실패", "english": "Audio device check failed"},
        "ASK": {"korean": "질문", "english": "QUESTION"},
        "ARCHIVE_CREATED": {"korean": "압축 파일 생성 완료", "english": "Archive created"},
        "API_KEY_INPUT": {"korean": "API 키 입력", "english": "API key input"},
        "API_ERROR": {"korean": "API 오류", "english": "API error"},
        "ALTERNATIVE_TEST_START": {"korean": "대안 테스트 시작", "english": "Alternative test start"},
        "ALTERNATIVE_OPTIONS_TEST": {"korean": "대안 옵션 테스트", "english": "Alternative options test"},
        "ALTERNATIVE_INSTALLATION": {"korean": "대안 설치", "english": "Alternative installation"},
        "ALREADY_EXIST": {"korean": "응급 백업", "english": "ALREADY EXIST"},
        "ALL_TESTS_COMPLETE": {"korean": "모든 테스트 완료", "english": "All tests complete"},
        "ALL_TESTS_COMPLETE_ALT": {"korean": "모든 테스트 완료", "english": "All tests complete"},
        "ALL_STEPS_COMPLETED": {"korean": "모든 단계 완료", "english": "All steps completed"},
        "ALL_SELENIUM_TESTS_COMPLETE": {"korean": "모든 Selenium 테스트 완료", "english": "All Selenium tests complete"},
        "ALL_ALTERNATIVE_TESTS_COMPLETE": {"korean": "모든 대안 테스트 완료", "english": "All alternative tests complete"},
        "ALIAS_SETUP": {"korean": "별칭 설정", "english": "Alias setup"},
        "ALERT_TIME": {"korean": "현재 시간은", "english": "Current time is"},
        "ALERT_BLOCKS": {"korean": "알림 블록", "english": "Alert Blocks"},
        "ALARM_SETTING_CANCELLED": {"korean": "알람 설정을 취소합니다", "english": "Alarm setting cancelled"},
        "AGE_VERIFICATION_BUTTON_NOT_FOUND": {"korean": "나이 확인 버튼이 없습니다", "english": "Age verification button not found"},
        "AGE_VERIFICATION_BUTTON_FOUND": {"korean": "나이 확인 버튼 발견", "english": "Age verification button found"},
        "AGE_VERIFICATION_BUTTON_CLICKED": {"korean": "나이 확인 버튼 클릭", "english": "Age verification button clicked"},
        "AGE_RESTRICTED": {"korean": "나이 제한", "english": "Age restricted"},
        "AGE_RESTRICTED_CONTENT_DETECTED": {"korean": "나이 제한 콘텐츠 감지", "english": "Age restricted content detected"},
        "AFTER_SERVICE": {"korean": "사후처리", "english": "AFTER SERVICE"},
        "ADD_USER_TO_DOCKER_GROUP": {"korean": "현재 사용자를 docker 그룹에 추가", "english": "Add current user to docker group"},
        "ADD_USER_TO_DOCKER_GROUP_FAILED": {"korean": "사용자를 docker 그룹에 추가 실패", "english": "Add user to docker group failed"},
        "ADD_USER_TO_DOCKER_GROUP_COMPLETE": {"korean": "사용자를 docker 그룹에 추가 완료", "english": "Add user to docker group complete"},
        "ACTIVATE_VENV": {"korean": "virtual environment 활성화", "english": "Activate virtual environment"},

        # 앞으로는 가능하다면 todo/done/question 아래의 샘플 패턴으로만 작성
        "YES": {"korean": "예", "english": "Yes"},
        "NO": {"korean": "아니오", "english": "No"},
        "DB": {"korean": "데이터베이스", "english": "DB"},

        # "DEBUG": {"korean": "🦋디버그", "english": "🦋DEBUG"},
        # "DEBUG": {"korean": "⚡", "english": "🔍DEBUG"},
        # "DEBUG": {"korean": "✅", "english": "🔍DEBUG"},
        # "DEBUG": {"korean": "🔍️개발자관심정보", "english": "🔍DEBUG"},
        # "DEBUG": {"korean": "🔍", "english": "🔍DEBUG"},
        "DEBUG": {"korean": "🔍", "english": "🔍DEBUG"},

        # "WARNING": {"korean": "🧩", "english": "⚠️WARNING"},
        # "WARNING": {"korean": "⚠️주의", "english": "⚠️WARNING"},
        # "WARNING": {"korean": "⚠️에러발생가능성발견", "english": "⚠️WARNING"},
        "WARNING": {"korean": "⚠️", "english": "⚠️WARNING"},


        # "INFO": {"korean": "ℹ️사용자관심정보", "english": "ℹ️INFO"},
        "INFO": {"korean": "ℹ️", "english": "ℹ️INFO"},

        # 🔑 패스워드 password

        # "ERROR": {"korean": "❌오류", "english": "Error"},
        # "ERROR": {"korean": "❌오류발생원인분석자료", "english": "Error"},
        "ERROR": {"korean": "❌", "english": "❌Error"},

        "DOCKER_INSTALLATION_ROUTINE_WSL_UBUNTU": {"korean": "WSL Ubuntu에 Docker 설치 튜토리얼 실행", "english": "Docker installation routine in WSL Ubuntu"},
        "D_pk_DOCKER_INSTALLATION_SUCCESS": {"korean": "D_PK_SYSTEM: Docker 설치 성공적으로 완료", "english": "D_PK_SYSTEM: Docker installation completed successfully"},
        "D_pk_DOCKER_INSTALLATION_FAILED": {"korean": "D_PK_SYSTEM: Docker 설치 실패", "english": "D_PK_SYSTEM: Docker installation failed"},
        "D_pk_UNEXPECTED_ERROR": {"korean": "D_PK_SYSTEM: 예상치 못한 오류 발생", "english": "D_PK_SYSTEM: Unexpected error occurred"},

        "PLAN_TO_MOVE": {"korean": "이동계획", "english": "PLAN_TO_MOVE"},
        "GUIDE": {"korean": "튜토리얼", "english": "GUIDE"},

        # done pattern
        "MOVED": {"korean": "이동완료", "english": "MOVED"},
        "SUCCEEDED": {"korean": "✅성공", "english": "✅SUCCEEDED"},
        "NOT_FOUND": {"korean": "찾을 수 없었습니다", "english": "NOT_FOUND".replace("_", PK_BLANK)},
        "RESULT": {"korean": "결과", "english": "RESULT".replace("_", PK_BLANK)},
        "RENAME": {"korean": "이름변경", "english": "RENAME".replace("_", PK_BLANK)},
        "ANSWER": {"korean": "답변", "english": "ANSWER".replace("_", PK_BLANK)},
        "FOUND": {"korean": "찾았 습니다", "english": "FOUND".replace("_", PK_BLANK)},

        # question pattern
        "ARE_YOU_SURE_EDIT_DONE": {"korean": "편집완료 했니 ?", "english": "ARE YOU SURE EDIT DONE?"},
        "ARE_YOU_WANT_TO_KEEP_GOING": {"korean": "계속 진행할까요?", "english": "ARE_YOU_WANT_TO_KEEP_GOING".replace("_", PK_BLANK)},
    }

    @classmethod
    def set_lang(cls, lang: str):
        if lang not in ("korean", "english"):
            raise ValueError(f"[ STATE ] Unsupported language: {lang}")
        for key, val in cls._localized_texts.items():
            setattr(cls, key, val.get(lang, f"[{key}]"))

    @classmethod
    def get_value_via_attr(cls, key: str) -> str:  # 이게 빠른경우가 있음.
        """Return a tag like: [PkTexts.KEY] <localized-value>"""
        if not hasattr(cls, key):
            return f"PkTexts.{key}"
        value = getattr(cls, key, "")
        return f"PkTexts.{key} {value}"


# 모듈 로드 시 기본값으로 초기화 (circular import 방지를 위해 lazy initialization 사용)
# 언어 설정은 ensure_pk_log_initialized() 또는 ensure_pk_language_initialized()에서 수행
PkTexts.set_lang("english")
