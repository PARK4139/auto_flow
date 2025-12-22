import platform
from os import environ
from pathlib import Path

from pk_internal_tools.pk_functions.get_d_pk_root_by_env import get_d_pk_root_by_env
from pk_internal_tools.pk_functions.get_pk_root import get_pk_root
from pk_internal_tools.pk_functions.get_user_sid import get_user_sid

D_PK_ROOT = get_d_pk_root_by_env(key_name="D_PK_ROOT")
if D_PK_ROOT is None:
    D_PK_ROOT = get_pk_root()  # 불완전한 코드

D_PK_PARENT = D_PK_ROOT.parent
D_PK_WORKING = D_PK_PARENT / "pk_working"
D_PK_ROOT_HIDDEN = D_PK_ROOT / '.pk_system'
D_VENV = D_PK_ROOT / '.venv'
D_IDEA = D_PK_ROOT / '.idea'
D_GIT = D_PK_ROOT / '.git'

if platform.system().lower() == "windows":
    D_USERPROFILE = Path(environ.get('USERPROFILE'))
    D_C_DRIVE = Path('C:/')
    D_D_DRIVE = Path('D:/')
    D_F_DRIVE = Path('F:/')
    D_G_DRIVE = Path('G:/')
    D_H_DRIVE = Path('H:/')
    D_I_DRIVE = Path('I:/')
    D_J_DRIVE = Path('J:/')

    # D_PK_CLONE = D_PK_WORKING / "pk_clone"
    D_G_DRIVE_PK_WORKING = D_G_DRIVE / "pk_working"
    D_DOWNLOADS = D_USERPROFILE / 'Downloads'
    D_DESKTOP = D_USERPROFILE / 'Desktop'
    D_PK_RECYCLE_BIN = D_DESKTOP / "휴지통"
    D_USER_SID = get_user_sid()
    D_RECYCLE_BIN_C = D_C_DRIVE / "$Recycle.Bin" / D_USER_SID
    D_RECYCLE_BIN_D = D_D_DRIVE / "$Recycle.Bin" / D_USER_SID
    D_RECYCLE_BIN_G = D_G_DRIVE / "$Recycle.Bin" / D_USER_SID
    D_RECYCLE_BIN = D_RECYCLE_BIN_C
    D_TEMP = D_PK_RECYCLE_BIN / "temp"
    D_TEST = D_TEMP / "test"
    D_TEST_RESULT = D_TEMP / "test_result"
    D_PK_TESTS = D_PK_ROOT / "pk_tests"  # pk_system/pk_tests
    D_PK_DATABASES = D_PK_ROOT_HIDDEN / "pk_databases"
    D_PK_CACHE = D_PK_ROOT_HIDDEN / "pk_cache"
    D_PK_HISTORY = D_PK_ROOT_HIDDEN / "pk_history"
    D_PK_CONFIG = D_PK_ROOT_HIDDEN / "pk_config"
    D_PK_TOKENS = D_PK_ROOT_HIDDEN / "pk_tokens"
    D_PK_COOKIES = D_PK_ROOT_HIDDEN / "pk_cookies"
    D_PK_TELEGRAM_SESSIONS = D_PK_ROOT_HIDDEN / "pk_telegram_sessions"
    D_PK_BACKUPS = D_PK_ROOT_HIDDEN / "pk_backups"
    D_MACROS = D_PK_ROOT_HIDDEN / "pk_macros"
    D_PK_LOGS = D_PK_ROOT / "pk_logs"
    D_TTS_CACHE = D_PK_LOGS / "tts_cache"
    D_PK_TODO = D_PK_ROOT / "pk_todo"
    D_PK_DOCS = D_PK_ROOT / "pk_docs"

    D_PK_EXTERNAL_TOOLS = D_PK_ROOT / 'pk_external_tools'
    D_PK_INTERNAL_TOOLS = D_PK_ROOT / 'pk_internal_tools'
    D_PK_WEB_SERVER = D_PK_INTERNAL_TOOLS / "pk_web_server"
    D_PK_P110m_TO_DEPLOY = D_PK_INTERNAL_TOOLS / 'pk_p110m_script'
    D_PK_WEB_SERVER_TO_DEPLOY = D_PK_INTERNAL_TOOLS / 'pk_web_server'
    D_PK_KIRIA_TO_DEPLOY = D_PK_INTERNAL_TOOLS / 'pk_kiria'
    D_PK_EXTERNAL_TOOLS_lager_than_4MB = D_PK_ROOT / "pk_external_tools_lager_than_4MB"
    D_PK_INFO = D_PK_INTERNAL_TOOLS / 'pk_info'
    D_PK_KIRIA = D_PK_INTERNAL_TOOLS / "pk_kiria"
    D_TTL_CACHE = D_PK_CACHE / 'pk_ttl_cache'
    D_YOUTUBE_DOWNLOADS_CACHE = D_PK_CACHE / 'pk_youtube_downloads'
    D_INSTAGRAM_DOWNLOADS_CACHE = D_PK_CACHE / "pk_instagram_downloads"
    D_HISTORY_CACHE = D_PK_CACHE / "pk_history_cache"
    D_PK_SOUND = D_PK_EXTERNAL_TOOLS
    D_DONE = D_PK_WORKING / "완료일정"
    D_TODO = D_PK_WORKING / "오전일정"
    D_TODO_EMERGENCY = D_TODO / "todo_emergency"
    D_DOWNLOADED_FROM_TORRENT = D_PK_WORKING / "downloaded_from_torrent"
    D_PK_WORKING_S = D_G_DRIVE_PK_WORKING / "pk_working_s"
    D_XLS_TO_MERGE = D_PK_ROOT_HIDDEN / 'xls_files_to_merge'  # D_PK_ROOT_HIDDEN에서 D_PK_ROOT_HIDDEN로 변경
    D_XLS_MERGED = D_PK_ROOT_HIDDEN / 'xls_files'  # D_PK_ROOT_HIDDEN에서 D_PK_ROOT_HIDDEN로 변경

    D_PK_FUNCTIONS = D_PK_INTERNAL_TOOLS / "pk_functions"
    D_PK_OBJECTS = D_PK_INTERNAL_TOOLS / "pk_objects"
    D_PK_wrappers = D_PK_INTERNAL_TOOLS / "pk_wrappers"
    D_PK_WRAPPERS = D_PK_INTERNAL_TOOLS / "pk_wrappers"
    D_PK_LINUX_TOOLS = D_PK_EXTERNAL_TOOLS
    D_PK_VIDEO = D_PK_EXTERNAL_TOOLS
    D_PKG_VIDEO = D_PK_EXTERNAL_TOOLS
    D_PK_VSTEST = D_PK_ROOT / 'project_vstest'
    D_PK_FASTAPI = D_PK_ROOT / 'project_fastapi'
    D_PK_CMAKE = D_PK_ROOT / 'project_cmake'
    D_PKG_CLOUD = D_PK_FASTAPI / 'pkg_cloud'
    D_VIDEO_MERGED = D_PK_WORKING / "pk_video_merged"
    # D_PK_DOWNLOADING = D_PK_WORKING / "pk_downloading"
    D_HOW = D_PK_WORKING / "pk_how"
    D_PK_ARCHIVED = D_PK_WORKING / "pk_archived"

    # external_repo
    D_AUTO_FLOW_REPO = D_PK_PARENT / "auto_flow"
    D_PK_MEMO_REPO = D_PK_PARENT / "pk_memo"
    D_BUSINESS_FLOW_REPO = D_PK_PARENT / "demo"

    D_ETC = Path("/etc")  # WINDOWS 에서 WSL 경로 추론 시 필요.
    # D_ETC = Path("etc")

    D_MOUSE_CLICK_COORDINATION_HISTORY = D_PK_ROOT_HIDDEN / "pk_mouse_click_coordination_history"  # D_PK_ROOT_HIDDEN에서 D_PK_ROOT_HIDDEN로 변경
    D_SLEEP_DURATION_HISTORY = D_PK_ROOT_HIDDEN / "pk_sleep_duration_history"  # D_PK_ROOT_HIDDEN에서 D_PK_ROOT_HIDDEN로 변경
    D_PK_WINDOWS_TOOLS = D_PK_EXTERNAL_TOOLS / "pk_windows_tools"
    D_LOSSLESSCUT = D_PK_EXTERNAL_TOOLS_lager_than_4MB / "pk_windows_tools" / "LosslessCut-win-x64_3.64.0"
    D_BITTORRENT_APPDATA = D_USERPROFILE / 'AppData' / 'Roaming' / 'bittorrent'
else:
    D_HOME = Path(environ.get('HOME'))  # /home
    D_DOWNLOADS = D_HOME / 'Downloads'

D_PK_WEB_SERVER_ROOT = D_PK_ROOT / "pk_web_server"

# remote_target_destination
D_REMOTE_PK_SYSTEM_ROOT = Path("opt") / 'pk_system'
D_REMOTE_WEB_SERVER_ROOT = D_REMOTE_PK_SYSTEM_ROOT / "pk_web_server"

# remote_target_destination templates
D_REMOTE_PK_SYSTEM_ROOT_TEMPLATE = "/home/{user_name}/pk_system"
D_REMOTE_PK_WEB_SERVER_ROOT_TEMPLATE = "/home/{user_name}/pk_system/pk_web_server"
D_REMOTE_PK_FUNCTIONS_TEMPLATE = "/home/{user_name}/pk_system/pk_functions"
D_REMOTE_PK_OBJECTS_TEMPLATE = "/home/{user_name}/pk_system/pk_objects"


