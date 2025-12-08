import logging
import os
from pathlib import Path

# 현재 파일의 부모 디렉토리 (pk_objects)
D_PK_OBJECTS_PATH = Path(__file__).parent
# 프로젝트 루트 디렉토리 (pk_objects -> pk_internal_tools -> auto_flow)
D_PROJECT_ROOT_PATH = D_PK_OBJECTS_PATH.parent.parent

# .venv/Scripts/python.exe 경로
F_VENV_PYTHON_EXE = D_PROJECT_ROOT_PATH / ".venv" / "Scripts" / "python.exe"
logging.debug(f"D_PROJECT_ROOT_PATH: {D_PROJECT_ROOT_PATH}")
logging.debug(f"F_VENV_PYTHON_EXE (computed): {F_VENV_PYTHON_EXE}")

from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
from pk_internal_tools.pk_objects.pk_directories import (
    D_DOWNLOADS, D_PK_SOUND, D_PK_VIDEO, D_C_DRIVE, D_ETC,
    d_pk_root_hidden, d_pk_logs, d_pk_root, D_PK_FUNCTIONS, d_pk_wrappers, D_PK_MEMO_REPO, D_PK_RECYCLE_BIN, D_DESKTOP,
    D_USERPROFILE, d_losslesscut, d_pk_external_tools, D_YOUTUBE_DB_CACHE, d_pk_root, D_PK_PARENT
)
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


F_UV_ACTIVATE_BAT = D_PROJECT_ROOT_PATH / ".venv" / "Scripts" / "activate.bat"
# F_UV_PYTHON = D_PROJECT_ROOT_PATH / ".venv" / "Scripts" / "python3" # Removed
# F_UV_ACTIVATE = D_PROJECT_ROOT_PATH / ".venv" / "Scripts" / "activate" # Removed

F_WSL_SSHD_CONFIG = D_ETC / "ssh" / "sshd_config"  # WSL 내부 경로
F_SSHD_CONFIG_TEMPLATE = d_pk_root_hidden / "etcsshsshd_config"  # SSH 설정 템플릿 파일 (백업/참조용)
# .pk_system 구조화된 경로 import
from pk_internal_tools.pk_objects.pk_directories import (
    d_pk_databases, d_pk_cache, d_pk_history,
    d_pk_config, d_pk_cookies,
    d_pk_sessions
)
F_ENV = D_PK_PARENT / ".env"
F_PK_MEMO_SQLITE = D_PK_MEMO_REPO / "pk_memo.sqlite"
F_MEMO_RAW = D_PK_MEMO_REPO / "pk_memo_working.md"

# F_ENSURE_PK_DOSKEY_ENABLED_BAT = D_PK_RECYCLE_BIN / "pk_doskey.bat"
F_TEMP_PS1 = D_PK_RECYCLE_BIN / "temp.ps1"
F_TEMP_BAT = D_PK_RECYCLE_BIN / "temp.bat"
F_TEMP_CMD = D_PK_RECYCLE_BIN / "temp.cmd"
F_TEMP_PY = D_PK_RECYCLE_BIN / "temp.py"

if QC_MODE:
    F_PK_LOG = d_pk_logs / f"pk_system.log"
    F_PK_TEMP_LOG = d_pk_logs / f"pk_temp.log"
else:
    F_PK_LOG = d_pk_logs / f"pk_{get_pk_time_2025_10_20_1159('now')}.log"
    F_PK_TEMP_LOG = d_pk_logs / f"pk_temp_via_{get_nx(__file__)}_{get_pk_time_2025_10_20_1159('now')}.log"

F_pk_ERROR_ISOLATED_LOG_LATEST = d_pk_logs / f"pk_error_isolated_log_latest.log"

F_SUCCESS_LOG = d_pk_logs / 'success.log'
F_MACRO_LOG = d_pk_logs / 'macro.log'
# F_PK_TEST_RESULTS_LOG = d_pk_logs / "pk_test_results.log"


F_PK_DOSKEY_BAT = d_pk_external_tools / "pk_doskey.bat"
# F_RUN_CMD = d_pk_external_tools / "run.cmd"
F_FZF = d_pk_external_tools / "pk_windows_tools" / "fzf.exe"
F_ENSURE_CMD_EXE_RAN_AS_ADMIN_CMD = d_pk_external_tools / "ensure_cmd_exe_ran_as_admin.cmd"
F_ENSURE_pk_LNK_PINNED_PS1 = d_pk_external_tools / "pk_windows_tools" / "ensure_pk_lnk_pinned.ps1"
F_ENSURE_CMD_EXE_RAN_AS_ADMIN = d_pk_external_tools / "ensure_cmd_exe_ran_as_admin.cmd"
F_UV_EXE = d_pk_external_tools / "uv.exe"  # this path is deprecated, TODO 동적으로 uv.exe 찾아야함.
F_ENSURE_pk_ENABLED_CMD = d_pk_external_tools / "pk_windows_tools" / 'ensure_pk_enabled.cmd'
F_ENSURE_pk_ENABLED_SH = d_pk_external_tools / 'ensure_pk_enabled.sh'

F_PK_ENSURE_PK_WRAPPER_STARTED_PY = d_pk_wrappers / "pk_ensure_pk_wrapper_starter_executed.py"
F_PK_ENSURE_pk_STARTED_PY = d_pk_wrappers / "pk_ensure_pk_wrapper_starter_executed.py"
F_PK_ENSURE_PK_COMMANDER_EXECUTED_PY = d_pk_wrappers / "pk_ensure_pk_terminal_executed.py"
F_PK_ENSURE_pk_ENABLED_PY = d_pk_wrappers / "pk_ensure_pk_enabled.py"
F_PK_ENSURE_STARTUP_ROUTINE_ENABLED_PY = d_pk_wrappers / "pk_ensure_routine_startup_enabled.py"
F_PK_ENSURE_PK_SCHEDULER_ENABLED_PY = d_pk_wrappers / "pk_ensure_pk_flow_executed.py"
F_PK_ENSURE_TEST_SCENARIO_EXECUTED_PY = d_pk_wrappers / "pk_ensure_routine_test_executed.py"
F_TEST_PY = d_pk_wrappers / "pk_test.py"
F_TEST_BAT = d_pk_wrappers / "pk_test.bat"
F_TEST_PS1 = d_pk_wrappers / "pk_test.ps1"
F_PK_ENSURE_TARGET_CONTROLLABLE_BASED_ON_FZF = d_pk_wrappers / "pk_ensure_target_file_controller_executed.py"

F_PYPROJECT_TOML = d_pk_root / 'pyproject.toml'
# F_QC_MODE_TOML = d_pk_system / "pk_qc_mode.toml" # deprecated


# 프로젝트 루트 파일들
F_GITIGNORE = d_pk_root / ".gitignore"
F_GEMINI_MD = d_pk_root / "GEMINI.md"
F_GEMINIIGNORE = d_pk_root / ".geminiignore"
F_GITATTRIBUTES = d_pk_root / ".gitattributes"

# 스크립트 파일들 (scripts 디렉토리)
f_ensure_pk_wrapper_executed_cmd = d_pk_external_tools / "ensure_pk_wrapper_executed.cmd"

# 환경 파일
F_LOCAL_PKG_CACHE_PRIVATE = d_pk_root / '__pycache__' / '__init__.cpython-312.pyc'
f_yt_dlp_exe = d_pk_external_tools / "yt-dlp.exe"
f_jq_win64_exe = d_pk_external_tools / "jq-win64.exe"
# F_WORKING = d_pk_system / "tests" / "pk_working.py"

# installed external tools in local
f_pycharm64_exe = D_C_DRIVE / "Program Files" / "JetBrains" / "PyCharm 2025.2.1" / "bin" / "pycharm64.exe"
# F_POT_PLAYER_EXE = D_C_DRIVE / "Program Files" / "DAUM" / "PotPlayer" / "PotPlayerMini64.exe"
F_POT_PLAYER_EXE = D_C_DRIVE / "Program Files" / "DAUM" / "PotPlayer" / "PotPlayer64.exe"
F_EVERYTHING = D_C_DRIVE / "Program Files" / "Everything" / "Everything.exe"
# F_SNIPPING_TOOL = D_C_DRIVE / "Program Files" / "WindowsApps" / "Microsoft.ScreenSketch_11.2507.14.0_x64__8wekyb3d8bbwe" / "SnippingTool" / "SnippingTool.exe"

F_LOSSLESSCUT_EXE = d_losslesscut / "LosslessCut.exe"
F_FFMPEG_EXE = d_losslesscut / "resources" / "ffmpeg.exe"
F_PK_LAUNCHER_LNK = D_DESKTOP / "pk_launcher.lnk"
# F_VSCODE = D_USERPROFILE / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "Code.exe"
F_VSCODE_LNK = D_USERPROFILE / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Visual Studio Code" / "Visual Studio Code.lnk"
F_BIT_TORRENT_EXE = D_USERPROFILE / "AppData" / "Roaming" / "bit_torrent.exe"
# F_CURSOR = D_USERPROFILE / "AppData" / "Local" / "Programs" / "cursor" / "Cursor.exe"
F_CURSOR_LNK = D_USERPROFILE / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Cursor" / "Cursor.lnk"
F_CLAUDE_LNK = D_USERPROFILE / "AppData" / "Local" / "AnthropicClaude" / "claude.exe"

F_UV_ZIP = D_DOWNLOADS / "uv.zip"
F_FZF_ZIP = D_DOWNLOADS / "fzf.zip"

F_MERGED_EXCEL_FILE = d_pk_cache / 'merged.xlsx'
F_NYAA_MAGNETS_SQLITE = d_pk_cache / "pk_magnets" / "nyaa_magnets.sqlite"
F_MEDIA_FILES_SQLITE = d_pk_cache / "pk_pnxs_scanned" / "pk_media_files.sqlite"
F_YOUTUBE_DB = D_YOUTUBE_DB_CACHE / 'youtube_downloads.sqlite'
F_YOUTUBE_URLS_TO_DOWNLOAD_TXT = d_pk_cache / "youtube_urls_to_download.txt"
F_INSTAGRAM_DB = d_pk_cache / "pk_instagram_downloads" / 'pk_instagram_downloads.sqlite'
F_INSTAGRAM_URLS_TO_DOWNLOAD_TXT = d_pk_cache / "pk_instagram_downloads" / "instagram_urls_to_download.txt"

F_VIDEO_POTPLAYER64_DPL = D_PK_VIDEO / "PotPlayer64.dpl"

# 데이터베이스 파일들
F_pk_SQLITE = d_pk_databases / 'pk_system.sqlite'
F_DB_JSON = d_pk_databases / "db.json"
F_DB_YAML = d_pk_databases / "db.yaml"
F_BOOKS_JSON = d_pk_databases / "books.json"
F_USERS_JSON = d_pk_databases / "users.json"
F_NAV_ITEMS_JSON = d_pk_databases / "nav_items.json"
F_VOLUME_REGISTRY_SQLITE = d_pk_databases / "volume_registry.sqlite"
F_PK_MEMO_BACKUP_SQLITE = d_pk_databases / "pk_memo_backup_before_dedup_ensure_memo_deduplication.sqlite"
F_ENSURE_FUNCTION_RETURN_TTL_CACHED_SQLITE = d_pk_databases / "ensure_pk_ttl_cached.sqlite"

# 캐시 파일들 (.pkl)
F_CACHE_VIDEO_FILTERED_LIST_V5 = d_pk_cache / "cache_of_get_video_filtered_list_v5.pkl"
F_STATE_ABOUT_PK_PRINT_ONCE = d_pk_cache / "state_about_pk_print_once.pkl"

# 히스토리 파일들
F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY = d_pk_history / "ensure_youtube_videos_downloaded_v3.history"
F_HISTORICAL_PNX = d_pk_history / 'historical_pnx.txt'
F_HISTORICAL_SEARCH_KEYWORD = d_pk_history / 'historical_search_keyword.txt'

# 설정 파일들
F_SCHEDULER_STATE = d_pk_config / "scheduler_state.json"
F_VIDEO_LIST_ALLOWED_TO_LOAD_TXT = d_pk_config / 'media_files_allowed_to_load.txt'
F_MEMO_TRASH_BIN_TOML = d_pk_config / 'memo_trash_bin.toml'
F_USELESS_FILE_NAMES_TXT = d_pk_config / "useless_file_names.txt"
F_PK_DOSKEY_MACROS_TXT = d_pk_config / "pk_doskey_macros.txt"
F_QC_MODE_TOML = d_pk_config / "pk_qc_mode.toml"
F_WSL_CMD_MAP_TOML = d_pk_config / "wsl_cmd_map.toml"
F_RENAME_RULES_TOML = d_pk_config / "rename_rules_for_ensure_filenames_and_directory_names_replaced.toml"

# 쿠키 파일들
F_CHORME_YOUTUBE_COOKIE = d_pk_cookies / "chrome_youtube.cookies"
F_YOUTUBE_COOKIES_TXT = d_pk_cookies / "youtube_cookies.txt"
F_YOUTUBE_COOKIES_BACKUP_TXT = d_pk_cookies / "youtube_cookies_backup.txt"
F_CHROME_YOUTUBE_COOKIES_BACKUP_TXT = d_pk_cookies / "chrome_youtube_cookies_backup_1755191166.txt"
F_INSTAGRAM_COOKIES_TXT = d_pk_cookies / "instagram_cookies.txt"
F_INSTAGRAM_COOKIES_JSON = d_pk_cookies / "instagram_cookies.json"

# 세션 파일들
F_PK_TELEGRAM_BOT_SESSION = d_pk_sessions / "pk_telegram_bot_session.session"
F_PK4139_TELEGRAM_BOT_SESSION = d_pk_sessions / "pk4139_telegram_bot_session.session"

F_SILENT_MP3 = D_PK_SOUND / "silent.mp3"
F_SILENT_WAV = D_PK_SOUND / "silent.wav"
F_POP_SOUND_POP_SOUND_WAV = D_PK_SOUND / "pop_sound.wav"
F_SOUND_POTPLAYER64_DPL = D_PK_SOUND / "PotPlayer64.dpl"

F_PK_ENSURE_GEMINI_CLI_INITIAL_PROMPT_LOADED_PY = d_pk_wrappers / 'pk_ensure_gemini_cli_initial_prompt_loaded.py'
F_PK_ENSURE_GEMINI_CLI_LOCATED_TO_FRONT = d_pk_wrappers / f'pk_ensure_gemini_cli_window_to_front.py'
F_ENSURE_ARG_RECIEVED = d_pk_wrappers / 'pk_ensure_arg_recieved.py'
F_USBPIPD_MSI = d_pk_external_tools / 'usbipd-win_5.2.0_x64.msi'

# F_LOSSLESSCUT_EXE = d_pk_external_tools / "LosslessCut-win-x64_3.65.0"/"LosslessCut.exe" # 3.60.0 pre release video 간헐적 끊김 issue discovered
F_LOSSLESSCUT = d_losslesscut / "LosslessCut.exe"
F_ICON_PNG = d_pk_external_tools / "pk_icon" / "icon.PNG"
F_MONTSERRAT_THIN_TTF = d_pk_external_tools / "Montserrat-Thin.ttf"
F_NOTOSANSKR_VARIABLEFONT_WGHT_TTF = d_pk_external_tools / "Noto_Sans_KR" / "NotoSansKR-VariableFont_wght.ttf"
F_NOTOSANSKR_BLACK_TTF = d_pk_external_tools / "NotoSansKR-Black.ttf"
F_NOTOSANSKR_BOLD_TTF = d_pk_external_tools / "NotoSansKR-Bold.ttf"
F_NOTOSANSKR_EXTRABOLD_TTF = d_pk_external_tools / "NotoSansKR-ExtraBold.ttf"
F_NOTOSANSKR_EXTRALIGHT_TTF = d_pk_external_tools / "NotoSansKR-ExtraLight.ttf"
F_NOTOSANSKR_LIGHT_TTF = d_pk_external_tools / "NotoSansKR-Light.ttf"
F_NOTOSANSKR_MEDIUM_TTF = d_pk_external_tools / "NotoSansKR-Medium.ttf"
F_NOTOSANSKR_REGULAR_TTF = d_pk_external_tools / "NotoSansKR-Regular.ttf"
F_NOTOSANSKR_SEMIBOLD_TTF = d_pk_external_tools / "NotoSansKR-SemiBold.ttf"
F_NOTOSANSKR_THIN_TTF = d_pk_external_tools / "NotoSansKR-Thin.ttf"
F_GMARKETSANSTTFBOLD_TTF = d_pk_external_tools / "GmarketSansTTFBold.ttf"
F_GMARKETSANSTTFLIGHT_TTF = d_pk_external_tools / "GmarketSansTTFLight.ttf"
F_GMARKETSANSTTFMEDIUM_TTF = d_pk_external_tools / "GmarketSansTTFMedium.ttf"
F_ITALIC_VARIABLEFONT_WGHT_TTF = d_pk_external_tools / "Montserrat" / "Montserrat-Italic-VariableFont_wght.ttf"
F_MONTSERRAT_VARIABLEFONT_WGHT_TTF = d_pk_external_tools / "Montserrat" / "Montserrat-VariableFont_wght.ttf"
F_MONTSERRAT_BLACK_TTF = d_pk_external_tools / "Montserrat-Black.ttf"
F_MONTSERRAT_BLACKITALIC_TTF = d_pk_external_tools / "Montserrat-BlackItalic.ttf"
F_MONTSERRAT_BOLD_TTF = d_pk_external_tools / "Montserrat-Bold.ttf"
F_MONTSERRAT_BOLDITALIC_TTF = d_pk_external_tools / "Montserrat-BoldItalic.ttf"
F_MONTSERRAT_EXTRABOLD_TTF = d_pk_external_tools / "Montserrat-ExtraBold.ttf"
F_MONTSERRAT_EXTRABOLDITALIC_TTF = d_pk_external_tools / "Montserrat-ExtraBoldItalic.ttf"
F_MONTSERRAT_EXTRALIGHT_TTF = d_pk_external_tools / "Montserrat-ExtraLight.ttf"
F_MONTSERRAT_EXTRALIGHTITALIC_TTF = d_pk_external_tools / "Montserrat-ExtraLightItalic.ttf"
F_MONTSERRAT_ITALIC_TTF = d_pk_external_tools / "Montserrat-Italic.ttf"
F_MONTSERRAT_LIGHT_TTF = d_pk_external_tools / "Montserrat-Light.ttf"
F_MONTSERRAT_LIGHTITALIC_TTF = d_pk_external_tools / "Montserrat-LightItalic.ttf"
F_MONTSERRAT_MEDIUM_TTF = d_pk_external_tools / "Montserrat-Medium.ttf"
F_MONTSERRAT_MEDIUMITALIC_TTF = d_pk_external_tools / "Montserrat-MediumItalic.ttf"
F_MONTSERRAT_REGULAR_TTF = d_pk_external_tools / "Montserrat-Regular.ttf"
F_MONTSERRAT_SEMIBOLD_TTF = d_pk_external_tools / "Montserrat-SemiBold.ttf"
F_MONTSERRAT_SEMIBOLDITALIC_TTF = d_pk_external_tools / "Montserrat-SemiBoldItalic.ttf"
F_MONTSERRAT_THINITALIC_TTF = d_pk_external_tools / "Montserrat-ThinItalic.ttf"
F_POPPINS_BLACK_TTF = d_pk_external_tools / "Poppins-Black.ttf"
F_POPPINS_BLACKITALIC_TTF = d_pk_external_tools / "Poppins-BlackItalic.ttf"
F_POPPINS_BOLD_TTF = d_pk_external_tools / "Poppins-Bold.ttf"
F_POPPINS_BOLDITALIC_TTF = d_pk_external_tools / "Poppins-BoldItalic.ttf"
F_POPPINS_EXTRABOLD_TTF = d_pk_external_tools / "Poppins-ExtraBold.ttf"
F_POPPINS_EXTRABOLDITALIC_TTF = d_pk_external_tools / "Poppins-ExtraBoldItalic.ttf"
F_POPPINS_EXTRALIGHT_TTF = d_pk_external_tools / "Poppins-ExtraLight.ttf"
F_POPPINS_EXTRALIGHTITALIC_TTF = d_pk_external_tools / "Poppins-ExtraLightItalic.ttf"
F_POPPINS_ITALIC_TTF = d_pk_external_tools / "Poppins-Italic.ttf"
F_POPPINS_LIGHT_TTF = d_pk_external_tools / "Poppins-Light.ttf"
F_POPPINS_LIGHTITALIC_TTF = d_pk_external_tools / "Poppins-LightItalic.ttf"
F_POPPINS_MEDIUM_TTF = d_pk_external_tools / "Poppins-Medium.ttf"
F_POPPINS_MEDIUMITALIC_TTF = d_pk_external_tools / "Poppins-MediumItalic.ttf"
F_POPPINS_REGULAR_TTF = d_pk_external_tools / "Poppins-Regular.ttf"
F_POPPINS_SEMIBOLD_TTF = d_pk_external_tools / "Poppins-SemiBold.ttf"
F_POPPINS_SEMIBOLDITALIC_TTF = d_pk_external_tools / "Poppins-SemiBoldItalic.ttf"
F_POPPINS_THIN_TTF = d_pk_external_tools / "Poppins-Thin.ttf"
F_POPPINS_THINITALIC_TTF = d_pk_external_tools / "Poppins-ThinItalic.ttf"
F_RUBIKDOODLESHADOW_REGULAR_TTF = d_pk_external_tools / "RubikDoodleShadow-Regular.ttf"  # 너무 귀여운 입체감 있는 영어 폰트 # Special cute font

F_TEST_PK_PYTHON_PROGRAM_STRUCTURE_PY = D_PK_FUNCTIONS / "test_pk_process_structure.py"

F_SNIPPING_TOOL_EXE = "snippingtool.exe"
F_VSCODE = "code"
F_FFMPEG = "ffmpeg"
F_YT_DLP = "yt-dlp"
F_JQ = "jq"
F_GNOME_SCREENSHOT = "gnome-screenshot"  # Linux 스크린샷 도구
F_TRANSMISSION_GTK = "transmission-gtk"  # Linux 토렌트 클라이언트
F_CURSOR = "cursor"  # Linux Cursor 실행 파일
F_CLAUDE = rf"claude"
F_UV = "uv"  # 시스템에 설치된 uv 사용
F_PYCHARM = "pycharm-community"  # 시스템 PATH에 있는 경우
PK_GLOBAL_LOG_LEVEL = "DEBUG" # TRACE | DEBUG | INFO | SUCCESS | WARNING | ERROR | CRITICAL
PK_SILENCE_AUDIOS = False # pk_option

PK_UNDERSCORE = "__"
PK_UNDERLINE = "―" * 60
PK_UNDERLINE_SHORT = "―" * 3
PK_UNDERLINE_HALF = "―" * 20