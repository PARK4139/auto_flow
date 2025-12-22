from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
import logging
from pk_internal_tools.pk_objects.pk_directories import (
    D_DOWNLOADS, D_PK_SOUND, D_PK_VIDEO, D_C_DRIVE, D_ETC,
    D_PK_ROOT_HIDDEN, D_PK_LOGS, D_PK_FUNCTIONS, D_PK_WRAPPERS, D_PK_MEMO_REPO, D_PK_RECYCLE_BIN, D_DESKTOP,
    D_USERPROFILE, D_VENV, D_LOSSLESSCUT, D_PK_EXTERNAL_TOOLS, D_YOUTUBE_DOWNLOADS_CACHE, D_PK_ROOT, D_PK_PARENT, D_PK_INTERNAL_TOOLS, D_PK_WEB_SERVER_ROOT, D_INSTAGRAM_DOWNLOADS_CACHE
)
from pk_internal_tools.pk_objects.pk_directories import (
    D_PK_DATABASES, D_PK_CACHE, D_PK_HISTORY,
    D_PK_CONFIG, D_PK_COOKIES,
    D_PK_TELEGRAM_SESSIONS
)
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

F_ENV = D_PK_PARENT / ".env"
F_UV_PYTHON_EXE = D_VENV / "Scripts" / "python.exe"
F_UV_ACTIVATE_BAT = D_VENV / "Scripts" / "activate.bat"
F_UV_PYTHON = D_VENV / "Scripts" / "python3"
F_UV_ACTIVATE = D_VENV / "Scripts" / "activate"
F_RUN_CMD = D_PK_ROOT / "run.cmd"

F_LOCAL_SSH_PUBLIC_KEY = D_USERPROFILE / ".ssh" / "id_ed25519.pub"
F_LOCAL_SSH_PRIVATE_KEY = D_USERPROFILE / ".ssh" / "id_ed25519"
F_WSL_SSHD_CONFIG = D_ETC / "ssh" / "sshd_config"  # WSL 내부 경로
F_SSHD_CONFIG_TEMPLATE = D_PK_ROOT_HIDDEN / "etcsshsshd_config"  # SSH 설정 템플릿 파일 (백업/참조용)

F_PK_MEMO_SQLITE = D_PK_MEMO_REPO / "pk_memo.sqlite"
F_MEMO_RAW = D_PK_MEMO_REPO / "pk_memo_working.md"

# F_ENSURE_PK_DOSKEY_ENABLED_BAT = D_PK_RECYCLE_BIN / "pk_doskey.bat"
F_TEMP_PS1 = D_PK_RECYCLE_BIN / "temp.ps1"
F_TEMP_BAT = D_PK_RECYCLE_BIN / "temp.bat"
F_TEMP_CMD = D_PK_RECYCLE_BIN / "temp.cmd"
F_TEMP_PY = D_PK_RECYCLE_BIN / "temp.py"

if QC_MODE:
    F_PK_LOG = D_PK_LOGS / f"pk_system.log"
else:
    F_PK_LOG = D_PK_LOGS / f"pk_system_{get_pk_time_2025_10_20_1159('now')}.log"
F_PK_TEMP_LOG = D_PK_RECYCLE_BIN / f"pk_temp.log"

F_PK_ERROR_ISOLATED_LOG_LATEST = D_PK_LOGS / f"pk_isolated_error_log_latest.log"

F_SUCCESS_LOG = D_PK_LOGS / 'success.log'
F_MACRO_LOG = D_PK_LOGS / 'macro.log'
# F_PK_TEST_RESULTS_LOG = D_PK_LOGS / "pk_test_results.log"


F_PK_DOSKEY_BAT = D_PK_EXTERNAL_TOOLS / "pk_doskey.bat"
# F_RUN_CMD = D_PK_EXTERNAL_TOOLS / "run.cmd"
F_FZF = D_PK_EXTERNAL_TOOLS / "pk_windows_tools" / "fzf.exe"
F_ENSURE_CMD_EXE_RAN_AS_ADMIN_CMD = D_PK_EXTERNAL_TOOLS / "ensure_cmd_exe_ran_as_admin.cmd"
F_ENSURE_pk_LNK_PINNED_PS1 = D_PK_EXTERNAL_TOOLS / "pk_windows_tools" / "ensure_pk_lnk_pinned.ps1"
F_ENSURE_CMD_EXE_RAN_AS_ADMIN = D_PK_EXTERNAL_TOOLS / "ensure_cmd_exe_ran_as_admin.cmd"
F_UV_EXE = D_PK_EXTERNAL_TOOLS / "uv.exe"  # this path is deprecated, TODO 동적으로 uv.exe 찾아야함.
F_ENSURE_pk_ENABLED_CMD = D_PK_EXTERNAL_TOOLS / "pk_windows_tools" / 'ensure_pk_enabled.cmd'
F_ENSURE_pk_ENABLED_SH = D_PK_EXTERNAL_TOOLS / 'ensure_pk_enabled.sh'

F_PK_ENSURE_PK_WRAPPER_STARTED_PY = D_PK_WRAPPERS / "pk_ensure_pk_system_cli_executed.py"
F_PK_ENSURE_pk_STARTED_PY = D_PK_WRAPPERS / "pk_ensure_pk_system_cli_executed.py"
F_PK_ENSURE_PK_COMMANDER_EXECUTED_PY = D_PK_WRAPPERS / "pk_ensure_pk_terminal_executed.py"
F_PK_ENSURE_pk_ENABLED_PY = D_PK_WRAPPERS / "pk_ensure_pk_enabled.py"
F_PK_ENSURE_STARTUP_ROUTINE_ENABLED_PY = D_PK_WRAPPERS / "pk_ensure_routine_startup_enabled.py"
F_PK_ENSURE_PK_SCHEDULER_ENABLED_PY = D_PK_WRAPPERS / "pk_ensure_pk_flow_executed.py"
F_PK_ENSURE_TEST_SCENARIO_EXECUTED_PY = D_PK_WRAPPERS / "pk_ensure_routine_test_executed.py"
F_TEST_PY = D_PK_WRAPPERS / "pk_test.py"
F_TEST_BAT = D_PK_WRAPPERS / "pk_test.bat"
F_TEST_PS1 = D_PK_WRAPPERS / "pk_test.ps1"
F_PK_ENSURE_TARGET_CONTROLLABLE_BASED_ON_FZF = D_PK_WRAPPERS / "pk_ensure_target_file_controlled.py"

F_PYPROJECT_TOML = D_PK_ROOT / 'pyproject.toml'
# F_QC_MODE_TOML = d_pk_system / "pk_deprecated.toml" # deprecated


# 프로젝트 루트 파일들
F_GITIGNORE = D_PK_ROOT / ".gitignore"
F_GEMINI_MD = D_PK_ROOT / "GEMINI.md"
F_GEMINIIGNORE = D_PK_ROOT / ".geminiignore"
F_GITATTRIBUTES = D_PK_ROOT / ".gitattributes"

# 스크립트 파일들 (scripts 디렉토리)
F_ENSURE_PK_WRAPPER_EXECUTED_CMD = D_PK_EXTERNAL_TOOLS / "ensure_pk_wrapper_executed.cmd"

# 환경 파일
F_LOCAL_PKG_CACHE_PRIVATE = D_PK_ROOT / '__pycache__' / '__init__.cpython-312.pyc'
F_YT_DLP_EXE = D_PK_EXTERNAL_TOOLS / "yt-dlp.exe"
F_JQ_WIN64_EXE = D_PK_EXTERNAL_TOOLS / "jq-win64.exe"


# F_WORKING = d_pk_system / "tests" / "pk_working.py"

# installed external tools in local
def _find_pycharm_exe_path():
    from pathlib import Path
    import os

    # 일반적으로 PyCharm이 설치되는 경로들
    possible_paths = [
        Path(os.environ.get('LOCALAPPDATA', '')) / "JetBrains",
        Path(os.environ.get('PROGRAMFILES', '')) / "JetBrains"
    ]

    for base_path in possible_paths:
        if base_path.exists():
            # PyCharm Community, Professional 등 여러 버전 포함
            for pycharm_path in base_path.glob("PyCharm*/bin/pycharm64.exe"):
                if pycharm_path.exists():
                    return pycharm_path
    return None


_pycharm_exe = _find_pycharm_exe_path()
if _pycharm_exe:
    F_PYCHARM_EXE = _pycharm_exe
else:
    # PyCharm 실행 파일 경로를 동적으로 찾지 못한 경우 경고 로깅
    logging.warning("PyCharm 실행 파일 (pycharm64.exe)을 시스템에서 찾을 수 없습니다. 경로가 올바르게 설정되어 있는지 확인해주세요.")
    F_PYCHARM_EXE = None # PyCharm 경로를 찾지 못했음을 명시적으로 표시

# F_POTPLAYER_EXE = D_C_DRIVE / "Program Files" / "DAUM" / "PotPlayer" / "PotPlayerMini64.exe"
F_POTPLAYER_EXE = D_C_DRIVE / "Program Files" / "DAUM" / "PotPlayer" / "PotPlayer64.exe"
F_EVERYTHING = D_C_DRIVE / "Program Files" / "Everything" / "Everything.exe"
# F_SNIPPING_TOOL = D_C_DRIVE / "Program Files" / "WindowsApps" / "Microsoft.ScreenSketch_11.2507.14.0_x64__8wekyb3d8bbwe" / "SnippingTool" / "SnippingTool.exe"


F_LOSSLESSCUT_EXE = D_LOSSLESSCUT / "LosslessCut.exe"
F_FFMPEG_EXE = D_LOSSLESSCUT / "resources" / "ffmpeg.exe"
F_PK_LAUNCHER_LNK = D_DESKTOP / "pk_launcher.lnk"
# F_VSCODE = D_USERPROFILE / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "Code.exe"
F_VSCODE_LNK = D_USERPROFILE / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Visual Studio Code" / "Visual Studio Code.lnk"
F_BIT_TORRENT_EXE = D_USERPROFILE / "AppData" / "Roaming" / "bit_torrent.exe"
# F_CURSOR = D_USERPROFILE / "AppData" / "Local" / "Programs" / "cursor" / "Cursor.exe"
F_CURSOR_LNK = D_USERPROFILE / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Cursor" / "Cursor.lnk"
F_CLAUDE_LNK = D_USERPROFILE / "AppData" / "Local" / "AnthropicClaude" / "claude.exe"

F_UV_ZIP = D_DOWNLOADS / "uv.zip"
F_FZF_ZIP = D_DOWNLOADS / "fzf.zip"

F_MERGED_EXCEL_FILE = D_PK_CACHE / 'merged.xlsx'
F_NYAA_MAGNETS_SQLITE = D_PK_CACHE / "pk_magnets" / "nyaa_magnets.sqlite"
F_NYAA_ANIMATION_TITLES_SQLITE = D_PK_CACHE / "pk_magnets" / "nyaa_animation_titles.sqlite"
F_MEDIA_FILES_SQLITE = D_PK_CACHE / "pk_pnxs_scanned" / "pk_media_files.sqlite"
F_YOUTUBE_DB = D_YOUTUBE_DOWNLOADS_CACHE / 'youtube_downloads.sqlite'
F_YOUTUBE_URLS_TO_DOWNLOAD_TXT = D_YOUTUBE_DOWNLOADS_CACHE / "pk_youtube_urls_to_download.txt"
F_INSTAGRAM_DB = D_PK_CACHE / "pk_instagram_downloads" / 'pk_instagram_downloads.sqlite'
F_INSTAGRAM_URLS_TO_DOWNLOAD_TXT = D_INSTAGRAM_DOWNLOADS_CACHE / "pk_instagram_urls_to_download.txt"

F_VIDEO_POTPLAYER64_DPL = D_PK_VIDEO / "PotPlayer64.dpl"

# 데이터베이스 파일들
F_pk_SQLITE = D_PK_DATABASES / 'pk_system.sqlite'
F_DB_JSON = D_PK_DATABASES / "db.json"
F_DB_YAML = D_PK_DATABASES / "db.yaml"
F_BOOKS_JSON = D_PK_DATABASES / "books.json"
F_USERS_JSON = D_PK_DATABASES / "users.json"
F_NAV_ITEMS_JSON = D_PK_DATABASES / "nav_items.json"
F_VOLUME_REGISTRY_SQLITE = D_PK_DATABASES / "volume_registry.sqlite"
F_PK_MEMO_BACKUP_SQLITE = D_PK_DATABASES / "pk_memo_backup_before_dedup_ensure_pk_memo_deduplication.sqlite"
F_ENSURE_FUNCTION_RETURN_TTL_CACHED_SQLITE = D_PK_DATABASES / "ensure_pk_ttl_cached.sqlite"

# 캐시 파일들 (.pkl)
F_STATE_ABOUT_PK_PRINT_ONCE = D_PK_CACHE / "state_about_pk_print_once.pkl"

# 히스토리 파일들
F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY = D_PK_HISTORY / "pk_ensure_youtube_videos_downloaded.history"
F_HISTORICAL_PNX = D_PK_HISTORY / 'pk_historical_pnx.txt'
F_HISTORICAL_SEARCH_KEYWORD = D_PK_HISTORY / 'historical_search_keyword.txt'

# 설정 파일들
F_SCHEDULER_STATE = D_PK_CONFIG / "scheduler_state.json"
F_VIDEO_LIST_ALLOWED_TO_LOAD_TXT = D_PK_CONFIG / 'media_files_allowed_to_load.txt'
F_MEMO_TRASH_BIN_TOML = D_PK_CONFIG / 'memo_trash_bin.toml'
F_USELESS_FILE_NAMES_TXT = D_PK_CONFIG / "pk_useless_file_names.txt"
F_PK_DOSKEY_MACROS_TXT = D_PK_CONFIG / "pk_doskey_macros.txt"
F_WSL_CMD_MAP_TOML = D_PK_CONFIG / "wsl_cmd_map.toml"
F_RENAME_RULES_TOML = D_PK_CONFIG / "rename_rules_for_ensure_file_names_and_directory_names_replaced.toml"

# 쿠키 파일들
F_CHORME_YOUTUBE_COOKIE = D_PK_COOKIES / "chrome_youtube.cookies"
F_YOUTUBE_COOKIES_TXT = D_PK_COOKIES / "youtube_cookies.txt"
F_YOUTUBE_COOKIES_BACKUP_TXT = D_PK_COOKIES / "youtube_cookies_backup.txt"
F_CHROME_YOUTUBE_COOKIES_BACKUP_TXT = D_PK_COOKIES / "chrome_youtube_cookies_backup_1755191166.txt"
F_INSTAGRAM_COOKIES_TXT = D_PK_COOKIES / "instagram_cookies.txt"
F_INSTAGRAM_COOKIES_JSON = D_PK_COOKIES / "instagram_cookies.json"

# 세션 파일들
F_PK_TELEGRAM_BOT_SESSION = D_PK_TELEGRAM_SESSIONS / "pk_telegram_bot_session.session"
F_PK4139_TELEGRAM_BOT_SESSION = D_PK_TELEGRAM_SESSIONS / "pk4139_telegram_bot_session.session"

F_SILENT_MP3 = D_PK_SOUND / "silent.mp3"
F_SILENT_WAV = D_PK_SOUND / "silent.wav"
F_POP_SOUND_POP_SOUND_WAV = D_PK_SOUND / "pop_sound.wav"
F_SOUND_POTPLAYER64_DPL = D_PK_SOUND / "PotPlayer64.dpl"

F_PK_ENSURE_GEMINI_CLI_INITIAL_PROMPT_LOADED_PY = D_PK_WRAPPERS / 'pk_ensure_gemini_cli_initial_prompt_loaded.py'
F_PK_ENSURE_GEMINI_CLI_LOCATED_TO_FRONT = D_PK_WRAPPERS / f'pk_ensure_gemini_cli_window_to_front.py'
F_ENSURE_ARG_RECIEVED = D_PK_WRAPPERS / 'pk_ensure_arg_recieved.py'
F_USBPIPD_MSI = D_PK_EXTERNAL_TOOLS / 'usbipd-win_5.2.0_x64.msi'

# F_LOSSLESSCUT_EXE = D_PK_EXTERNAL_TOOLS / "LosslessCut-win-x64_3.65.0"/"LosslessCut.exe" # 3.60.0 pre release video 간헐적 끊김 issue discovered
F_LOSSLESSCUT = D_LOSSLESSCUT / "LosslessCut.exe"
F_ICON_PNG = D_PK_EXTERNAL_TOOLS / "pk_icon" / "icon.PNG"
F_MONTSERRAT_THIN_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Thin.ttf"
F_NOTOSANSKR_VARIABLEFONT_WGHT_TTF = D_PK_EXTERNAL_TOOLS / "Noto_Sans_KR" / "NotoSansKR-VariableFont_wght.ttf"
F_NOTOSANSKR_BLACK_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-Black.ttf"
F_NOTOSANSKR_BOLD_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-Bold.ttf"
F_NOTOSANSKR_EXTRABOLD_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-ExtraBold.ttf"
F_NOTOSANSKR_EXTRALIGHT_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-ExtraLight.ttf"
F_NOTOSANSKR_LIGHT_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-Light.ttf"
F_NOTOSANSKR_MEDIUM_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-Medium.ttf"
F_NOTOSANSKR_REGULAR_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-Regular.ttf"
F_NOTOSANSKR_SEMIBOLD_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-SemiBold.ttf"
F_NOTOSANSKR_THIN_TTF = D_PK_EXTERNAL_TOOLS / "NotoSansKR-Thin.ttf"
F_GMARKETSANSTTFBOLD_TTF = D_PK_EXTERNAL_TOOLS / "GmarketSansTTFBold.ttf"
F_GMARKETSANSTTFLIGHT_TTF = D_PK_EXTERNAL_TOOLS / "GmarketSansTTFLight.ttf"
F_GMARKETSANSTTFMEDIUM_TTF = D_PK_EXTERNAL_TOOLS / "GmarketSansTTFMedium.ttf"
F_ITALIC_VARIABLEFONT_WGHT_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat" / "Montserrat-Italic-VariableFont_wght.ttf"
F_MONTSERRAT_VARIABLEFONT_WGHT_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat" / "Montserrat-VariableFont_wght.ttf"
F_MONTSERRAT_BLACK_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Black.ttf"
F_MONTSERRAT_BLACKITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-BlackItalic.ttf"
F_MONTSERRAT_BOLD_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Bold.ttf"
F_MONTSERRAT_BOLDITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-BoldItalic.ttf"
F_MONTSERRAT_EXTRABOLD_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-ExtraBold.ttf"
F_MONTSERRAT_EXTRABOLDITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-ExtraBoldItalic.ttf"
F_MONTSERRAT_EXTRALIGHT_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-ExtraLight.ttf"
F_MONTSERRAT_EXTRALIGHTITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-ExtraLightItalic.ttf"
F_MONTSERRAT_ITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Italic.ttf"
F_MONTSERRAT_LIGHT_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Light.ttf"
F_MONTSERRAT_LIGHTITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-LightItalic.ttf"
F_MONTSERRAT_MEDIUM_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Medium.ttf"
F_MONTSERRAT_MEDIUMITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-MediumItalic.ttf"
F_MONTSERRAT_REGULAR_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-Regular.ttf"
F_MONTSERRAT_SEMIBOLD_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-SemiBold.ttf"
F_MONTSERRAT_SEMIBOLDITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-SemiBoldItalic.ttf"
F_MONTSERRAT_THINITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Montserrat-ThinItalic.ttf"
F_POPPINS_BLACK_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Black.ttf"
F_POPPINS_BLACKITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-BlackItalic.ttf"
F_POPPINS_BOLD_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Bold.ttf"
F_POPPINS_BOLDITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-BoldItalic.ttf"
F_POPPINS_EXTRABOLD_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-ExtraBold.ttf"
F_POPPINS_EXTRABOLDITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-ExtraBoldItalic.ttf"
F_POPPINS_EXTRALIGHT_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-ExtraLight.ttf"
F_POPPINS_EXTRALIGHTITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-ExtraLightItalic.ttf"
F_POPPINS_ITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Italic.ttf"
F_POPPINS_LIGHT_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Light.ttf"
F_POPPINS_LIGHTITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-LightItalic.ttf"
F_POPPINS_MEDIUM_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Medium.ttf"
F_POPPINS_MEDIUMITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-MediumItalic.ttf"
F_POPPINS_REGULAR_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Regular.ttf"
F_POPPINS_SEMIBOLD_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-SemiBold.ttf"
F_POPPINS_SEMIBOLDITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-SemiBoldItalic.ttf"
F_POPPINS_THIN_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-Thin.ttf"
F_POPPINS_THINITALIC_TTF = D_PK_EXTERNAL_TOOLS / "Poppins-ThinItalic.ttf"
F_RUBIKDOODLESHADOW_REGULAR_TTF = D_PK_EXTERNAL_TOOLS / "RubikDoodleShadow-Regular.ttf"  # 너무 귀여운 입체감 있는 영어 폰트 # Special cute font

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

F_PK_P110m_MAIN_SCRIPT = D_PK_INTERNAL_TOOLS / 'pk_p110m_script' / "main.py"
F_PK_WEB_SERVER_MAIN_SCRIPT = D_PK_WEB_SERVER_ROOT / "main.py"
