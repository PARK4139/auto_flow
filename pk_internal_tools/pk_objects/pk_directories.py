import platform
from os import environ
from pathlib import Path

from pk_internal_tools.pk_functions.get_pk_root import get_pk_root

d_pk_root = get_pk_root()
D_PK_PARENT = d_pk_root.parent
D_PK_WORKING = D_PK_PARENT / "pk_working"
d_pk_root_hidden = d_pk_root / '.pk_system'

if platform.system().lower() == "windows":
    D_USERPROFILE = Path(environ.get('USERPROFILE'))
    D_C_DRIVE = Path('C:/')
    D_D_DRIVE = Path('D:/')
    D_F_DRIVE = Path('F:/')
    D_G_DRIVE = Path('G:/')
    D_H_DRIVE = Path('H:/')
    D_I_DRIVE = Path('I:/')
    D_J_DRIVE = Path('J:/')

    D_PK_CLONE = D_PK_WORKING / "pk_clone"
    D_G_DRIVE_PK_WORKING = D_G_DRIVE / "pk_working"
    D_VENV = d_pk_root / '.venv'
    D_DOWNLOADS = D_USERPROFILE / 'Downloads'
    D_DESKTOP = D_USERPROFILE / 'Desktop'
    D_PK_RECYCLE_BIN = D_DESKTOP / "휴지통"  # pk_option
    D_TEMP = D_PK_RECYCLE_BIN / "temp"
    D_TEST = D_TEMP / "test"
    D_TEST_RESULT = D_TEMP / "test_result"
    D_PK_DOWNLOADING = D_PK_RECYCLE_BIN
    d_pk_tests = d_pk_root / "pk_tests"  # pk_system/pk_tests
    d_pk_databases = d_pk_root_hidden / "pk_databases"
    d_pk_cache = d_pk_root_hidden / "pk_cache"
    d_pk_history = d_pk_root_hidden / "pk_history"
    d_pk_config = d_pk_root_hidden / "pk_config"
    d_pk_tokens = d_pk_root_hidden / "pk_tokens"
    d_pk_cookies = d_pk_root_hidden / "pk_cookies"
    d_pk_sessions = d_pk_root_hidden / "pk_sessions"
    d_pk_backups = d_pk_root_hidden / "pk_backups"
    d_macros = d_pk_root_hidden / "pk_macros"
    d_pk_logs = d_pk_root / "pk_logs"
    d_pk_docs = d_pk_root / "pk_docs"

    d_pk_external_tools = d_pk_root / 'pk_external_tools'
    d_pk_internal_tools = d_pk_root / 'pk_internal_tools'
    d_pk_remote_scripts = d_pk_internal_tools / 'pk_remote_scripts'
    d_pk_external_tools_lager_than_4MB = d_pk_root / "pk_external_tools_lager_than_4MB"
    d_pk_info = d_pk_internal_tools / 'pk_info'
    D_TTL_CACHE = d_pk_cache / 'pk_ttl_cache'
    D_YOUTUBE_DB_CACHE = d_pk_cache / 'pk_youtube_downloads_db'
    D_HISTORY_CACHE = d_pk_cache / "pk_history_cache"
    # D_PK_SOUND = D_F_DRIVE / 'pk_working' / 'pk_sound'
    D_PK_SOUND = d_pk_external_tools
    D_DONE = D_PK_WORKING / "완료일정"
    D_TODO = D_PK_WORKING / "오전일정"
    D_TODO_EMERGENCY = D_TODO / "todo_emergency"
    D_DOWNLOADED_FROM_TORRENT = D_PK_WORKING / "downloaded_from_torrent"
    D_PK_WORKING_S = D_G_DRIVE_PK_WORKING / "pk_working_s"
    D_PKG_ARCHIVED = D_PK_WORKING / 'pk_archived'
    D_XLS_TO_MERGE = d_pk_root_hidden / 'xls_files_to_merge'  # d_pk_root_hidden에서 d_pk_root_hidden로 변경
    D_XLS_MERGED = d_pk_root_hidden / 'xls_files'  # d_pk_root_hidden에서 d_pk_root_hidden로 변경

    D_PK_FUNCTIONS = d_pk_internal_tools / "pk_functions"
    D_PK_OBJECTS = d_pk_internal_tools / "pk_objects"
    D_PK_wrappers = d_pk_internal_tools / "pk_wrappers"
    d_pk_wrappers = d_pk_internal_tools / "pk_wrappers"
    d_pk_linux_tools = d_pk_external_tools
    D_PK_VIDEO = d_pk_external_tools
    D_PKG_VIDEO = d_pk_external_tools
    D_PK_VSTEST = d_pk_root / 'project_vstest'
    D_PK_FASTAPI = d_pk_root / 'project_fastapi'
    D_PK_CMAKE = d_pk_root / 'project_cmake'
    D_PKG_CLOUD = D_PK_FASTAPI / 'pkg_cloud'
    D_VIDEO_MERGED = D_PK_WORKING / "pk_video_merged"
    # D_PK_DOWNLOADING = D_PK_WORKING / "pk_downloading"
    D_HOW = D_PK_WORKING / "pk_how"
    D_ARCHIVED = D_PK_WORKING / "pk_archived"

    # external_repo
    D_PK_MEMO_REPO = D_DOWNLOADS / "pk_memo"  # TODO : DEPRECATE
    D_BUSINESS_FLOW_REPO = D_DOWNLOADS / "business_flow"

    D_ETC = Path("/etc")  # WINDOWS 에서 WSL 경로 추론 시 필요.

    D_MOUSE_CLICK_HISTORY = d_pk_root_hidden / "pk_mouse_click_history"  # d_pk_root_hidden에서 d_pk_root_hidden로 변경
    D_SLEEP_DURATION_HISTORY = d_pk_root_hidden / "pk_sleep_duration_history"  # d_pk_root_hidden에서 d_pk_root_hidden로 변경

    d_pk_windows_tools = d_pk_external_tools_lager_than_4MB / "pk_windows_tools"
    d_losslesscut = d_pk_windows_tools / "LosslessCut-win-x64_3.64.0"
    D_ROOT = Path("/")
else:
    D_HOME = Path(environ.get('HOME'))  # /home
    D_DOWNLOADS = D_HOME / 'Downloads'
    D_VENV = d_pk_root / '.venv'
