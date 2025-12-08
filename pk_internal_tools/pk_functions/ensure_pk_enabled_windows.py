import logging

try:
    from pk_internal_tools.pk_objects.pk_map_colors import pk_ANSI_COLOR_MAP
except ImportError as e:
    import platform

    logging.debug(f"모듈을 찾을 수 없음: {e}")
    logging.debug("Windows 환경에서 안전한 색상 코드 사용합니다")
    if platform.system().lower() == "windows":
        try:
            import colorama
            colorama.init(autoreset=True, convert=True)
            pk_ANSI_COLOR_MAP = {
                'GREEN': '\033[32m', 'RED': '\033[31m', 'YELLOW': '\033[33m',
                'BLUE': '\033[34m', 'MAGENTA': '\033[35m', 'CYAN': '\033[36m',
                'RESET': '\033[0m'
            }
        except (ImportError, Exception):
            # colorama 실패 시 색상 없이
            pk_ANSI_COLOR_MAP = {
                'GREEN': '', 'RED': '', 'YELLOW': '', 'BLUE': '',
                'MAGENTA': '', 'CYAN': '', 'RESET': ''
            }
    else:
        # Linux/Mac에서는 기본 ANSI 색상 코드
        pk_ANSI_COLOR_MAP = {
            'GREEN': '\033[32m', 'RED': '\033[31m', 'YELLOW': '\033[33m',
            'BLUE': '\033[34m', 'MAGENTA': '\033[35m', 'CYAN': '\033[36m',
            'RESET': '\033[0m'
        }
try:
    from pk_internal_tools.pk_objects.pk_directories import *
    from pk_internal_tools.pk_objects.pk_files import *
    from pk_internal_tools.pk_objects.pk_urls import URL_FZF_API, URL_CHATGPT_PK_WORKING
except ImportError as e:
    import os

    logging.debug(f"모듈을 찾을 수 없음: {e}")
    logging.debug("기본 경로를 사용합니다.")

    # 기본 경로 설정 (USERPROFILE 동적 사용)

    userprofile = os.environ.get('USERPROFILE', os.path.expanduser('~'))

    d_pk_system = Path(userprofile) / "Downloads" / "pk_system"
    d_pk_external_tools = Path(userprofile) / "Downloads" / "pk_system" / "pk_external_tools"
    d_pk_external_tools = d_pk_external_tools  # 하위 호환성
    d_pk_external_tools = d_pk_external_tools  # 통합됨
    D_pk_HIDDEN = Path(userprofile) / "Downloads" / "pk_system" / ".pk_system"
    D_PK_WORKING = Path(userprofile) / "Downloads" / "pk_working"
    D_PK_MEMO = Path(userprofile) / "Downloads" / "pk_memo"
    D_BUSINESS_FLOW = Path(userprofile) / "Downloads" / "business_flow"
    D_DOWNLOADS = Path(userprofile) / "Downloads"

    # 기본 파일 경로
    F_UV = None
    F_FZF = None
    F_UV_ZIP = None
    F_FZF_ZIP = None
    F_VSCODE = None
    F_CURSOR = None
    F_CLAUDE = None
    F_PYCHARM = None

    # 기본 URL
    URL_FZF_API = "https://api.github.com/repos/junegunn/fzf/releases/latest"
    URL_CHATGPT_PK_WORKING = "https://chat.openai.com"

if platform.system().lower() == "windows":
    import winreg

print = None

PkTextsFallBack = type('PkTexts', (), {
    'VENV_PYTHON_TEST': 'virtual environment Python 테스트',
    'VENV_PYTHON_NOT_FOUND': 'virtual environment Python을 찾을 수 없음',
    'VENV_PYTHON_VERSION': 'virtual environment Python 버전',
    'VENV_MODULE_TEST': '모듈 사용 가능',
    'VENV_TEST_SUCCESS': '테스트 성공',
    'UV_INSTALLATION': 'UV 설치',
    'PERMISSION_ERROR': '권한 오류',
    'BACKUP_CREATED': '백업 생성됨',
    'BACKUP_FAILED': '백업 실패',
    'FILE_NOT_FOUND': '파일을 찾을 수 없음',
    'DIRECTORY_CREATED': '디렉토리 생성됨',
    'DIRECTORY_CREATION_FAILED': '디렉토리 생성 실패',
    'FILE_COPY_SUCCESS': '파일 복사 성공',
    'FILE_COPY_FAILED': '파일 복사 실패',
    'ALTERNATIVE_INSTALLATION': '대안 설치',
    'TEMP_CLEANUP_FAILED': '임시 파일 정리 실패',
    'INSTALLATION_SUCCESS': '설치 완료',
    'INSTALLATION_FAILED': '설치 실패',
    'PATH_SETUP': 'Windows PATH 설정',
    'ALIAS_SETUP': 'Windows 별칭 설정',
    'REGISTRY_SETUP_SUCCESS': '레지스트리 설정 완료',
    'REGISTRY_SETUP_FAILED': '레지스트리 설정 실패',
    'WINDOWS_REGISTRY_SETUP_SUCCESS': 'Windows 레지스트리 설정 완료',
    'WINDOWS_REGISTRY_SETUP_FAILED': 'Windows 레지스트리 설정 실패',
    'PACKAGE_SYNC': 'uv 패키지 동기화',
    'VENV_SETUP': 'virtual environment Python으로 패키지 설치',
    'VENV_PYTHON_FOUND': 'virtual environment Python 사용',
    'PACKAGE_INSTALLING': '설치 중',
    'PACKAGE_INSTALL_SUCCESS': '설치 완료',
    'PACKAGE_INSTALL_FAILED': '설치 실패',
    'PACKAGE_INSTALL_ERROR': '설치 오류',
    'VENV_PACKAGE_INSTALL_COMPLETE': 'virtual environment 패키지 설치 완료',
    'FZF_INSTALLATION': 'FZF 설치',
    'OPERATION_SUCCESS': '동기화 완료',
    'OPERATION_FAILED': '동기화 실패',
    'VENV_TEST_FAILED': '테스트 실패'
})()
# Lazy import to avoid circular dependency
try:
    import logging
    from pk_internal_tools.pk_objects.pk_map_texts import PkTexts

    print = logging.debug
except ImportError:
    import builtins

    print = builtins.print
    PkTexts = PkTextsFallBack


def ensure_pk_doskey_bat_created_with_selected_doskeys(selected_doskey_commands: list[str], uv_exe_path: str = None) -> Path:
    """
    선택된 doskey 명령어 목록을 받아서 pk_doskey.bat 파일을 생성합니다.
    
    Args:
        selected_doskey_commands: 등록할 doskey 명령어 목록 (예: ['doskey pk=...', 'doskey pkc=...'])
        uv_exe_path: uv.exe 경로 (None이면 F_UV_EXE 사용)
    
    Returns:
        Path: 생성된 bat 파일 경로
    """
    try:
        import textwrap
        f_ensure_pk_doskey_enabled_bat = F_ENSURE_PK_DOSKEY_ENABLED_BAT
        
        if uv_exe_path is None:
            uv_exe_path = F_UV_EXE
        
        # bat 파일 내용 생성
        batch_content = textwrap.dedent(f'''
            @echo off
            chcp 65001 >NUL
        ''').lstrip()
        
        # 선택된 doskey 명령어들 추가
        for doskey_command in selected_doskey_commands:
            batch_content += f"\n    {doskey_command}"
        
        batch_content += "\n"
        
        # 디렉토리 생성 및 파일 쓰기
        f_ensure_pk_doskey_enabled_bat.parent.mkdir(parents=True, exist_ok=True)
        with open(f_ensure_pk_doskey_enabled_bat, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        if f_ensure_pk_doskey_enabled_bat.exists():
            logging.debug(f'''{f_ensure_pk_doskey_enabled_bat} 생성완료 ''')
            return f_ensure_pk_doskey_enabled_bat
        else:
            logging.debug(f'''{f_ensure_pk_doskey_enabled_bat} 생성실패 ''')
            raise FileNotFoundError(f"bat 파일 생성 실패: {f_ensure_pk_doskey_enabled_bat}")

    except Exception as e:
        logging.error(f"파일 생성/실행 실패: {e}")
        raise


def ensure_pk_autorun_registered():
    """
    pk_doskey.bat 파일을 Windows CMD AutoRun에 등록합니다.
    """
    import subprocess
    f_pk_doskey_bat = F_ENSURE_PK_DOSKEY_ENABLED_BAT
    
    if not f_pk_doskey_bat.exists():
        logging.error(f"bat 파일이 존재하지 않습니다: {f_pk_doskey_bat}")
        raise FileNotFoundError(f"bat 파일이 존재하지 않습니다: {f_pk_doskey_bat}")
    
    # 레지스트리 AutoRun 설정
    try:
        # AutoRun 등록 (REG_EXPAND_SZ 로 환경변수 확장 허용 + call 사용)
        autorun_value = rf'call "{f_pk_doskey_bat}"'
        subprocess.run([
            "reg", "add", r"HKCU\Software\Microsoft\Command Processor",
            "/v", "AutoRun", "/t", "REG_EXPAND_SZ", "/d", autorun_value, "/f"
        ], check=True, text=True, capture_output=True)
        logging.debug(f"AutoRun 등록:{autorun_value}")

        # 확인
        subprocess.run([
            "reg", "query", r"HKCU\Software\Microsoft\Command Processor", "/v", "AutoRun"
        ], check=True)
        logging.debug(f"AutoRun 설정완료")
    except Exception as e:
        logging.error(f"레지스트리 설정 실패: {e}")
        raise

